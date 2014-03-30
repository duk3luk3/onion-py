Beware
-------
This is version 0.1.1 of OnionPy. It is mostly untested, has no useful error handling, is not as comprehensive as claimed below, and may pull down megabytes of data from random places on the internet and then use that to overwrite random locations on your hard drive.

OnionPy
========

A comprehensive pure-Python wrapper for the OnionOO Tor status API, with memcached support to cache queried data.

Installing OnionPy
===================

You can install onion-py manually by doing the following:

    git clone https://github.com/duk3luk3/onion-py.git
    cd onion-py
    sudo python setup.py install

Getting it into pip is planned.

**Beware**: OnionPy has been developed and tested exclusively with Python 3. Please let Python 2 rest in peace forevermore.

Usage
=====

    >>> import onion_py.manager as m
    >>> manager = m.Manager(None)
    >>> s = manager.query('summary', limit=4)
    >>> s.relays[0].fingerprint
    '695D027F728A3B95D0D7F6464D63F82229BFA361'
    >>> s.relays[0].nickname
    'GREATWHITENORTH'

License
=======

BSD 3-clause. See LICENSE.  
Portions of this work obviously belong to to OnionOO and therefore the Tor Project. See ONIONOO-LICENSE.
