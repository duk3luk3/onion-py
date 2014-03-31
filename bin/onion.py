#!/usr/bin/env python3

import sys
import time
import onion_py.manager as om
import random
from functools import *

def main(argv):
  manager = om.Manager(None)

  if argv[1] == "family-members":
    family_members(manager, argv[2])
    
  elif argv[1] == "test":
    test(manager)

def family_members(m, n):
  d = m.query('details', search=n, limit=1, type='relay')
  if len(d.relays) < 1:
    print("No relay found")
    return
  f = d.relays[0].family

def test(m):
  d = m.query('summary', limit=4)
  print("Summary limited to 4: >>%s<<" % (d,))
  while True:
    num = random.randint(0,1500)
    d = m.query('details', limit=1, offset=num)
    print("Details for one relay: >>%s<<" % (d.relays[0],))
    d = m.query('bandwidth', limit=1, offset=num).relays[0].write_history.get('3_days')
    if d is not None:
      write_avg = reduce(lambda x,y: (x or 0) + (y or 0), d.values) / d.count * d.factor
      print("Average write bandwidth of that relay for the last 3 days: %f bytes per second" % (write_avg,))
      break
    else:
      print("That relay had no history.")

if __name__ == "__main__":
  if len(sys.argv) > 1:
    main(sys.argv)
  else:
    print("this program needs arguments.")
