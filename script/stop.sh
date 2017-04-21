#!/bin/bash

id=`ps -ef |grep "python" |grep 'alien_spirit' | grep 'main' |awk '{print $2}'`
echo "kill " $id
kill $id
