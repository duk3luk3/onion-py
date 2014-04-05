#!/usr/bin/env python3

import sys
import time
import onion_py.manager as om
from onion_py.objects import *
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
  fields = 'nickname,fingerprint,family,exit_probability'
  for s in n:
    d = m.query('details', search=s, limit=1, type='relay', fields=fields)
    if len(d.relays) < 1:
      print("No relay found for search term '{}'".format(s))
      continue

    check_relay = d.relays[0]
    valid_relays = [check_relay]
    invalid_relays = []
    for f in check_relay.family:
      d = m.query('details', search=f, limit=1, type='relay', fields=fields)
      if len(d.relays) > 0:
        if family_check(d.relays[0].family, check_relay):
          valid_relays.append(d.relays[0])
        else:
          invalid_relays.append(d.relays[0])
      else:
        invalid_relays.append(RelayDetails({'nickname': f}))
    print("Finished aggregation for {}".format(s))
    print("Valid family members  : {}".format(", ".join([x.nickname or x.fingerprint for x in valid_relays])))
    if len(invalid_relays) > 0:
      print("Invalid family members: {}".format(", ".join([str(x) for x in invalid_relays])))
    p = 0.0
    for r in valid_relays:
      p = p + r.exit_probability or 0.0
    print("Aggregate exit probability: {}".format(p))



def family_check(family_strings, relay):
  for f in family_strings:
   if (relay.nickname == f or '$'+relay.fingerprint == f):
     return True
  return False

def test(m,n):
  d = m.query('summary', limit=4)
  print("Summary limited to 4: >>%s<<" % (d,))
  while True:
    num = random.randint(0,150)
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
    'family-members': [family_members, 'pass relay nicknames or fingerprints and the relay\'s families will be enumerated and an aggregate exit probability calculated'],
    'test': [test, 'a short test making a couple of calls']
    }

if __name__ == "__main__":
  main(sys.argv)
