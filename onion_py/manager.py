import requests
import json as j
import onion_py.objects as o

UseDefault = object()

def json_serializer(key, value):
  if type(value) == str:
    return value, 1
  return json.dumps(value), 2

def json_deserializer(key, value, flags):
  if flags == 1:
    return value
  if flags == 2:
    return json.loads(value)
  raise Exception("Unknown serialization format")

def key_serializer(query, params):
  s = query + ';';
  for key in Manager.OOO_QUERYPARAMS:
    s = s + str(params.get(key))+';'
  return s

"""
The main OnionOO api wrapper class.
"""
class Manager:
  OOO_URL = 'https://onionoo.torproject.org/'
  OOO_SLUG = 'ONIONOO'
  OOO_VERSION = '0.0.0'

  OOO_QUERIES = {
      'summary':    o.Summary,
      'details':    o.Details,
      'bandwidth':  o.Bandwidth,
      'weights':    o.Weights,
      'clients':    o.Clients,
      'uptime':     o.Uptime
      }
  OOO_QUERYPARAMS = [
      'type',
      'running',
      'search',
      'lookup',
      'country',
      'as',
      'flag',
      'first_seen_days',
      'last_seen_says',
      'contact',
      'fields',
      'order',
      'offset',
      'limit'
      ]

  """
  The OnionOO constructor.

  Args:
    memcached_host: tuple (hostname, port) - if set to None, caching of responses in memcached will be disabled.
    onionoo_host: hostname for the onionoo api endpoint - defaults to canonical onionoo.torproject.org
  """
  def __init__(self, memcached_host = ('localhost', 11211), onionoo_host = None):
    self.memcached_host = memcached_host
    if self.memcached_host is not None:
      from pymemcache.client import Client
      self.memcached_client = Client(self.memcached_host, serializer=json_serializer, deserializer=json_deserializer)
    else:
      self.memcached_client = None

    self.onionoo_host = onionoo_host or self.OOO_URL

  def query(self, query, **kwargs):
    #TODO: Proper validation of parameters

    params = dict((k,v) for k,v in kwargs.items() if k in self.OOO_QUERYPARAMS)
    if len(params) < len(kwargs):
      #TODO: Handle this properly by logging or raising
      pass

    # turn list params into comma-separated strings
    for param in ['fields','order']:
      if param in params and type(params[param]) is list:
        params[param] = ",".join(params[param])

    # build request
    url = self.onionoo_host + query

    # check for cache entry
    cache_entry = None
    cache_key = key_serializer(query, params)
    if self.memcached_client is not None:
      cache_entry = self.memcached_client.get(cache_key)

    result = None

    if cache_entry is not None:
      since = cache_entry['timestamp']
      headers = {'If-Modified-Since': since}
      r = requests.head(url, params=params, headers=headers)
      if r.status_code == 304:
        result = cache_entry['record']

    if result is None:
      # Make full request
      r = requests.get(url, params=params)
      if r.status_code == 200:
        result = r.json()
        # Save to cache
        if self.memcached_client is not None:
          cache_entry = { 'timestamp': r.headers['Last-Modified'], 'record': result }
          self.memcached_client.set(cache_key, cache_entry)

    if result is not None:
      return self.OOO_QUERIES[query](result)
    else:
      return None
