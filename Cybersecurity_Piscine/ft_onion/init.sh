#!/bin/bash
service nginx start
service tor start
exec /usr/sbin/sshd -D