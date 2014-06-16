"""
Onion-Py Manager

Logic for interacting with OnionOO
"""
import requests
import json
import onion_py.objects as o

class OnionPyError(Exception):
  pass

class BadRequestError(OnionPyError):
  pass

class ServiceUnavailableError(OnionPyError):
  pass

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
  def __init__(self, cache = None, onionoo_host = None):
    self.cache_client = cache
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
    if self.cache_client is not None:
      cache_entry = self.cache_client.get(query, params)

    result = None

    if cache_entry is not None:
      since = cache_entry['timestamp']
      headers = {'If-Modified-Since': since}
      r = requests.head(url, params=params, headers=headers)
      if r.status_code == 304:
        result = cache_entry['record']
      elif r.status_code == 400:
        raise BadRequestError("OnionPy did not accept our query: {} ({})".format(r.reason, r.url))
      elif r.status_code in [500, 503]:
        raise ServiceUnavailableError('OnionPy is down: {}'.format(r.reason))

    if result is None:
      # Make full request
      r = requests.get(url, params=params)
      if r.status_code == 200:
        result = r.json()
        # Save to cache
        if self.cache_client is not None:
          cache_entry = { 'timestamp': r.headers['Last-Modified'], 'record': result }
          self.cache_client.set(query, params, cache_entry)
      elif r.status_code == 400:
        raise BadRequestError("OnionPy did not accept our query: {} ({})".format(r.reason, r.url))
      elif r.status_code in [500, 503]:
        raise ServiceUnavailableError('OnionPy is down: {}'.format(r.reason))

    if result is not None:
      return self.OOO_QUERIES[query](result)
    else:
      return None
