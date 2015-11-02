"""
Onion-Py caching backends
"""

from onion_py.manager import Manager
import json
import abc


"""
OnionCache class

Abstract base class showing the prototype for OnionOO Cache
"""
class OnionCache(object):

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def __init__(self, **kwargs):
      pass
  
  @abc.abstractmethod
  def get(self, query, params):
      pass

  @abc.abstractmethod
  def set(self, query, params, document):
      pass

def json_serializer(key, value):
  if type(value) == str:
    return value, 1
  return json.dumps(value).encode('utf-8'), 2

def json_deserializer(key, value, flags):
  if flags == 1:
    return value
  if flags == 2:
    return json.loads(value.decode('utf-8'))
  raise Exception("Unknown serialization format")

def key_serializer(query, params):
  s = query + ';';
  for key in Manager.OOO_QUERYPARAMS:
    s = s + str(params.get(key))+';'
  return s

class OnionSimpleCache(OnionCache):
  def __init__(self):
    self.dict = {}

  def get(self, query, params):
    return self.dict.get(key_serializer(query,params))

  def set(self, query, params, document):
    self.dict[key_serializer(query, params)] = document


class OnionMemcached(OnionCache):
  def __init__(self, host=('localhost', 11211)):
      from pymemcache.client import Client
      self.memcached_client = Client(host, serializer=json_serializer, deserializer=json_deserializer)

  def get(self, query, params):
    return self.memcached_client.get(key_serializer(query,params))

  def set(self, query, params, document):
    return self.memcached_client.set(key_serializer(query,params),document)






