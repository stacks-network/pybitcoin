coinrpc
=======

This documentation is currently under progress

Add a new Name:

To add a new name, make a post request to namecoind/register_name with the following parameters:
-name=NAME
-value=VALUE
-passphrase=PASSPHRASE
-freegraph - [optional] pass freegraph if you want to register a name with u/, otherwise, skip this parameter.

Sample Request:

curl -i http://127.0.0.1:5000/namecoind/register_name -d "name=halfmoon&value=halfmoonlabs.com&passphrase=PASSPHRASE&freegraph"

