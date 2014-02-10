coinrpc
=======

For secure deployment:
```
  python setup.py build_ext --inplace
  python secure_run.py
```

This documentation is currently under progress


##Add a new Name:

To add a new name, make a POST request to /namecoind/register_name with the following parameters:
- name=NAME
- value=VALUE
- passphrase=PASSPHRASE
- freegraph - [optional] pass freegraph if you want to register a name with u/ (instead of the default d/), otherwise, skip this parameter.

###Sample Request:
curl -i http://127.0.0.1:5000/namecoind/register_name -d "name=halfmoon&value=halfmoonlabs.com&passphrase=PASSPHRASE&freegraph"


##Scan blockchain

Make a GET request to /namecoind/name_scan. You can optionally pass the following arguments
- start_name - [optional]
- max_returned - [optional]
 

###Sample Request:
http://127.0.0.1:5000/namecoind/name_scan?start_name=g/p&max_returned=10
