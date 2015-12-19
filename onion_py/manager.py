"""
Onion-Py Manager

Logic for interacting with OnionOO
"""
import requests
import json
import onion_py.objects as o

class OnionPyError(Exception):
  pass

class InvalidDocumentTypeError(OnionPyError):
    """ Raised when document type requested is not supported by Onionoo """
    def __init__(self, doc_type):
        self.doc_type = doc_type

    def __str__(self):
        return 'Invalid document type ' + repr(self.doc_type)


class InvalidParameterError(OnionPyError):
    """ Raised when a request parameter is not supported by Onionoo """
    def __init__(self, param):
        self.param = param

    def __str__(self):
        return 'Invalid parameter ' + repr(self.param)


class OnionooError(OnionPyError):
    """ Raised when Onionoo responds with an error code """
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return str(self.code) + ' - ' + self.msg


class DataError(OnionPyError):
    """ Raised due to insufficient/inconsistent data """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class MajorVersionMismatchError(OnionPyError):
    """ Raised when OnionOO response major version is higher than supported major version """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

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
  OOO_VERSION_MAJOR = 3
  OOO_VERSION_MINOR = 0

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
    if query not in self.OOO_QUERIES:
      raise InvalidDocumentTypeError(query)

    # Check if request parameters are valid
    for param in kwargs.keys():
      if param not in self.OOO_QUERYPARAMS:
         raise InvalidParameterError(param)

    params = kwargs

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
        raise BadRequestError("OnionPy did not accept our query: {} ({})".\
            format(r.reason, r.url))
      elif r.status_code in [500, 503]:
        raise ServiceUnavailableError('OnionPy is down: {}'.format(r.reason))

    if result is None:
      # Make full request
      r = requests.get(url, params=params)
      if r.status_code == 200:
        result = r.json()
        # Save to cache
        if self.cache_client is not None:
          cache_entry = { 'timestamp': r.headers['Last-Modified'],
              'record': result }
          self.cache_client.set(query, params, cache_entry)
      elif r.status_code == 400:
        raise BadRequestError("OnionPy did not accept our query: {} ({})".\
            format(r.reason, r.url))
      elif r.status_code in [500, 503]:
        raise ServiceUnavailableError('OnionPy is down: {}'.format(r.reason))

    if result is not None:
      document = self.OOO_QUERIES[query](result)

      versions = document.version.split('.')
      if int(versions[0]) > self.OOO_VERSION_MAJOR:
        raise MajorVersionMismatchError("Received OnionOO Document with version {}, this library only supports up to version {}".format(versions[0],self.OOO_VERSION_MAJOR))
      return document
    else:
      return None
