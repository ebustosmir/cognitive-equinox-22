#!/bin/bash

echo "Start DNS server"
/etc/init.d/bind9 start

/bin/bash -c "while :; do rndc reload; sleep 1; done"