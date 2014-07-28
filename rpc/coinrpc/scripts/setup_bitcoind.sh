#!/bin/bash
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

echo "Enter BITCOIND_SERVER:"
read input
export BITCOIND_SERVER=$input

echo "Enter BITCOIND_PORT:"
read input
export BITCOIND_PORT=$input

echo "Enter BITCOIND_USER:"
read input
export BITCOIND_USER=$input

echo "Enter BITCOIND_PASSWD:"
read input
export BITCOIND_PASSWD=$input

echo "Done"