#!/usr/bin/env python3

import sys
import time
import onion_py.manager as om
import random
from functools import *


def main(argv):
  manager = om.Manager(None)

  if len(argv) > 1 and argv[1] in handlers:
    handlers[argv[1]][0](manager, argv[2:])
  else:
    print("Usage:")
    print(argv[0] + " <command>")
    print("Commands:")
    for k,v in handlers.items():
      print("{:<20}{:}".format(k, v[1]))
    
def family_members(m, n):
  d = m.query('details', search=n[0], limit=1, type='relay')
  if len(d.relays) < 1:
    print("No relay found")
    return
  print("Found relay: %s" % (d.relays[0].nickname,))
  closed = [d.relays[0]]
  blacklist = []
  open = d.relays[0].family
  while len(open) > 0:
    print(".")
    cur = open
    open = []
    for c in cur:
      print("Closed: %s" % ("; ".join(["%s (%s)" % (x.fingerprint, x.nickname) for x in closed]),))
      if c in ["$"+x.fingerprint for x in closed] or c in [x.nickname for x in closed] or c in blacklist:
        continue
      print("Looking up %s" % (c,))
      d = m.query('details', search=c, limit=1, type='relay')
      if len(d.relays) > 0:
        d = d.relays[0]
        print("Looking up family of %s" % (d.nickname,))
        if len(d.family) > 0:
          open = open + d.family
        if not d.fingerprint in [x.fingerprint for x in closed]:
          closed.append(d)
      else:
        blacklist.append(c)
  print([x.nickname for x in closed])
  print("not found: %s" % (blacklist,))

def test(m,n):
  d = m.query('summary', limit=4)
  print("Summary limited to 4: >>%s<<" % (d,))
  while True:
    num = random.randint(0,1500)
    d = m.query('details', limit=1, offset=num)
    print("Details for one relay: >>%s<<" % (d.relays[0],))
    d = m.query('bandwidth', limit=1, offset=num)
    if len(d.relays) > 0:
      d = d.relays[0].write_history.get('3_days')
    else:
      d = None
    if d is not None:
      write_avg = reduce(lambda x,y: (x or 0) + (y or 0), d.values) / d.count * d.factor
      print("Average write bandwidth of that relay for the last 3 days: %f bytes per second" % (write_avg,))
      break
    else:
      print("That relay had no history.")

handlers = {
    'family-members': [family_members, 'pass a relay nickname or fingerprint and the relay\'s family will be enumerated'],
    'test': [test, 'a short test making a couple of calls']
    }

if __name__ == "__main__":
  main(sys.argv)
