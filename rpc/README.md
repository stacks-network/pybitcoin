coinrpc
=======

Requires memcached:

```
sudo apt-get install memcached libmemcached-dev
sudo apt-get install python2.7-dev

```

For quick deployment:

```
pip install -r requirements.txt
./runserver 
```

Example API call: 
```
http://localhost:5000/namecoind/name_show?key=d/bitcoin
```

Set python-path:

```
ln -s /home/muneeb/.envs/coinrpc/lib/python2.7/site-packages/ python-path
```
