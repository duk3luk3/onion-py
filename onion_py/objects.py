"""
Class wrappers for the OnionOO objects
"""

"""
Relay summary field

The relay summary contains:
  - nickname
  - fingerprint
  - addresses
  - running
"""
class RelaySummary:
  def __init__(self, document):
    self.nickname = document.get('n')
    self.fingerprint = document.get('f')
    self.addresses = document.get('a')
    self.running = document.get('r')

  def __str__(self):
    return "Relay summary for %s (%s) " % (self.nickname or "<Not named>", self.fingerprint or "<No fingerprint>")

"""
Bridge summary field

The bridge summary contains:
  - nickname
  - hash
  - running
"""
class BridgeSummary:
  def __init__(self, document):
    self.nickname = document.get('n')
    self.hash = document.get('h')
    self.running = document.get('r')

  def __str__(self):
    return "Bridge summary for %s (%s) " % (self.nickname or "<Not named>", self.fingerprint or "<No fingerprint>")

"""
Summary document

https://onionoo.torproject.org/#summary

The summary document contains:
  - relays_published: timestamp of relay publication
  - relays: relay summaries
  - bridges_published: timestamp of bridge publication
  - bridges: bridge summaries

"""
class Summary:
  def __init__(self, document):
    self.relays_published = document.get('relays_published')
    self.bridges_published = document.get('bridges_published')
    self.relays = [RelaySummary(d) for d in document.get('relays')]
    self.bridges = [BridgeSummary(d) for d in document.get('bridges')]

  def __str__(self):
    return "Summary document (%d bridges, %d relays)" % (len(self.bridges or []),len(self.relays or []))


"""
Relay Details field

The relay detail contains:
  - nickname
  - fingerprint
  - or_addresses
  - exit_addresses
  - dir_address
  - last_seen
  - last_changed_address_or_port
  - first_seen
  - running
  - hibernating
  - flags
  - geo (country, country_name, region_name, city_name, latitude, longitude)
  - as (number, name)
  - consensus_weight
  - host_name
  - last_restarted
  - bandwidth (rate, burst, observed, advertised)
  - exit_policy
  - exit_policy_summary
  - exit_policy_v6_summary
  - contact
  - platform
  - recommended_version
  - family
  - advertised_bandwidth_fraction
  - consensus_weight_fraction
  - guard_probability
  - middle_probability
  - exit_probability
"""
class RelayDetails:
  def __init__(self, document):
    g = document.get
    self.nickname = g('nickname')
    self.fingerprint = g('fingerprint')
    self.or_addresses = g('or_addresses')
    self.exit_addresses = g('exit_addresses')
    self.dir_address = g('dir_address')
    self.last_seen = g('last_seen')
    self.last_changed_address_or_port = g('last_changed_address_or_port')
    self.first_seen = g('first_seen')
    self.running = g('running')
    self.hibernating = g('hibernating')
    self.flags = g('flags')
    self.geo = (g('country'),g('country_name'),g('region_name'),g('city_name'),g('latitude'),g('longitude'))
    self.as_number = g('as_number')
    self.as_name = g('as_name')
    self.consensus_weight = g('consensus_weight')
    self.host_name = g('host_name')
    self.last_restarted = g('last_restarted')
    self.bandwidth = (g('bandwidth_rate'),g('bandwidth_burst'),g('bandwidth_observed'),g('bandwidth_advertised'))
    self.exit_policy = g('exit_policy')
    self.exit_policy_summary = g('exit_summary_policy')
    self.exit_policy_v6_summary = g('exit_policy_v6_policy')
    self.contact = g('contact')
    self.platform = g('platform')
    self.recommended_version = g('recommended_version')
    self.family = g('family')
    self.advertised_bandwidth_fraction = g('advertised_bandwidth_fraction')
    self.consensus_weight_fraction = g('consensus_weight_fraction')
    self.guard_probability = g('guard_probability')
    self.middle_probability = g('middle_probability')
    self.exit_probability = g('exit_probability')

  def __str__(self):
    return "Detailed relay descriptor for %s (%s)" % (self.nickname or "<Not named>", self.fingerprint or "<No fingerprint>")

"""
Bridge Details field

The bridge detail contains:
  - nickname
  - hashed_fingerprint
  - or_addresses
  - last_seen
  - first_seen
  - running
  - flags
  - last_restarted
  - advertised_bandwidth
  - platform
  - pool_assignment
"""
class BridgeDetails:
  def __init__(self, document):
    g = document.get
    self.nickname = g('nickname')
    self.hashed_fingerprint = g('hashed_fingerprint')
    self.or_address = g('or_address')
    self.last_seen = g('last_seen')
    self.first_seen = g('first_seen')
    self.running = g('running')
    self.flags = g('flags')
    self.last_restarted = g('last_restarted')
    self.advertised_bandwidth = g('advertised_bandwidth')
    self.platform = g('platform')
    self.pool_assignment = g('pool_assignment')

  def __str__(self):
    return "Detailed bridge descriptor for %s (%s)" % (self.nickname or "<Not named>", self.hashed_fingerprint or "<No fingerprint>")


"""
Details document

https://onionoo.torproject.org/#details

The details document contains:
  - relays_published: timestamp of relay publication
  - relays: relay details
  - bridges_published: timestamp of bridge publication
  - bridges: bridge details
"""
class Details:
  def __init__(self, document):
    self.relays_published = document.get('relays_published')
    self.bridges_published = document.get('bridges_published')
    self.relays = [RelayDetails(d) for d in document.get('relays')]
    self.bridges = [BridgeDetails(d) for d in document.get('bridges')]

  def __str__(self):
    return "Details document (%d bridges, %d relays)" % (len(self.bridges or []),len(self.relays or []))

"""
Graph history object

Graph history contains:
  - first
  - last
  - interval
  - factor
  - count
  - values
"""
class GraphHistory:
  def __init__(self, document):
    g = document.get
    self.first = g('first')
    self.last = g('last')
    self.interval = g('interval')
    self.factor = g('factor')
    self.count = g('count')
    self.values = g('values')
    #TODO: support additional statistic fields carried in history objects (countries, transports, versions)

  def __str__(self):
    return "Graph history object"

"""
Bandwidth object

The bandwidth object contains:
  - fingerprint
  - write_history
  - read_history
"""
class BandwidthDetail:
  def __init__(self, document):
    g = document.get
    self.finger_print = g('fingerprint')
    self.write_history = dict([(k, GraphHistory(v)) for k,v in g('write_history').items()]) if g('write_history') is not None else None
    self.read_history = dict([(k, GraphHistory(v)) for k,v in g('read_history').items()]) if g('read_history') is not None else None


  def __str__(self):
    return "Bandwidth object"

"""
Bandwidth document

https://onionoo.torproject.org/#bandwidth

The bandwidth document contains:
  - relays_published
  - relays
  - bridges_published
  - bridges
"""
class Bandwidth:
  def __init__(self,document):
    g = document.get
    self.relays_published = g('relays_published')
    self.bridges_published = g('bridges_published')
    self.relays = [BandwidthDetail(d) for d in g('relays')]
    self.bridges = [BandwidthDetail(d) for d in g('bridges')]

  def __str__(self):
    return "Bandwidth document (Containing bandwidth histories for %d bridges and %d relays)" % (len(self.bridges or []),len(self.relays or []))

"""
Relay weight object

The relay weight object contains:
  - fingerprint
  - advertised_bandwidth_fraction
  - consensus_weight_fraction
  - guard_probability
  - middle_probability
  - exit_probability
"""
class RelayWeight:
  def __init__(self, document):
    g = document.get
    self.fingerprint = g('fingerprint')
    self.advertised_bandwidth_fraction = dict([(k, GraphHistory(v)) for k,v in g('advertised_bandwidth_fraction').items()])
    self.consensus_weight_fraction = dict([(k, GraphHistory(v)) for k,v in g('consensus_weight_fraction').items()])
    self.guard_probability = dict([(k, GraphHistory(v)) for k,v in g('guard_probability').items()])
    self.middle_probability = dict([(k, GraphHistory(v)) for k,v in g('middle_probability').items()])
    self.exit_probability = dict([(k, GraphHistory(v)) for k,v in g('exit_probability').items()])

  def __str__(self):
    return "relay weight object for %s" % (self.fingerprint or '<no fingerprint>')

"""
Weights document

https://onionoo.torproject.org/#weights

The weights document contains:
  - relays_published
  - relays
  - bridges_published
  - bridges
"""
class Weights:
  def __init__(self,document):
    g = document.get
    self.relays_published = g('relays_published')
    self.bridges_published = g('bridges_published')
    self.relays = [RelayWeight(d) for d in g('relays')]
    self.bridges = []

  def __str__(self):
    return "Weights document containing weight history for %d relays)" % (len(self.relays or []))

"""
Bridge client object

The bridge client object contains:
  - fingerprint
  - average_clients
"""
class BridgeClient:
  def __init__(self, document):
    g = document.get
    self.fingerprint = g('fingerprint')
    self.average_clients = dict([(k, GraphHistory(v)) for k,v in g('average_clients').items()])

  def __str__(self):
    return "Bridge client history object for %s" % (self.fingerprint or '<no fingerprint>')


"""
Clients document

https://onionoo.torproject.org/#clients

The clients document contains:
  - relays_published
  - relays
  - bridges_published
  - bridges
"""
class Clients:
  def __init__(self, document):
    g = document.get
    self.relays_published = g('relays_published')
    self.bridges_published = g('bridges_published')
    self.relays = []
    self.bridges = [BridgeClient(d) for d in g('bridges')]

  def __str__(self):
    return "Clients document containing client histories for %d bridges" % (len(self.bridges or []))

"""
Relay Uptime object

The relay uptime object contains:
  - fingerprint
  - uptime
"""
class RelayUptime:
  def __init__(self, document):
    g = document.get
    self.fingerprint = g('fingerprint')
    self.uptime = dict([(k, GraphHistory(v)) for k,v in g('uptime').items()])

  def __str__(self):
    return "Relay uptime history object for %s" % (self.fingerprint or '<no fingerprint>')


"""
Uptime document

https://onionoo.torproject.org/#uptime

The uptime document contains:
  - relays_published
  - relays
  - bridges_published
  - bridges
"""
class Uptime:
  def __init__(self, document):
    g = document.get
    self.relays_published = g('relays_published')
    self.bridges_published = g('bridges_published')
    self.relays = [RelayUptime(d) for d in g('relays')]
    self.bridges = [RelayUptime(d) for d in g('bridges')]
  
  def __str__(self):
    return "Uptime document (Containing uptime histories for %d bridges and %d relays)" % (len(self.bridges or []),len(self.relays or []))
