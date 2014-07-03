OnionPy
========

A comprehensive pure-Python wrapper for the OnionOO Tor status API, with memcached support to cache queried data.

Installing OnionPy
===================

You can install onion-py manually by doing the following (requires setuptools!)::

    git clone https://github.com/duk3luk3/onion-py.git
    cd onion-py
    #run tests if desired
    PYTHONPATH=. python bin/onion.py test
    sudo python setup.py install

For the optional memcached support, install pymemcache and six::

    sudo pip install six
    sudo pip install https://github.com/pinterest/pymemcache.git

The package is also on [Pypi](https://pypi.python.org/pypi/OnionPy).

**Beware**: <del>OnionPy has been developed and tested exclusively with Python 3. Please let Python 2 rest in peace forevermore.</del> OnionPy is compatible with Python 2.7 upwards.

Usage
=====

    >>> from onion_py.manager import Manager
    >>> from onion_py.caching import OnionSimpleCache
    >>> manager = Manager(OnionSimpleCache())
    >>> s = manager.query('summary', limit=4)
    >>> s.relays[0].fingerprint
    '695D027F728A3B95D0D7F6464D63F82229BFA361'
    >>> s.relays[0].nickname
    'GREATWHITENORTH'

Accepted Queries
=====
    Summary, details, bandwidth, weights, clients, uptime

    >>> s = manager.query('summary', limit=4)
    >>> s = manager.query('details', limit=4)
    >>> s = manager.query('bandwidth', limit=4)
    >>> s = manager.query('weights', limit=4)
    >>> s = manager.query('clients', limit=4)
    >>> s = manager.query('uptime', limit=4)

License
=======

BSD 3-clause. See LICENSE.  
Portions of this work obviously belong to to OnionOO and therefore the Tor Project. See ONIONOO-LICENSE.
