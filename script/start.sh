#!/bin/bash

d=`date +"%Y%m%d-%H%M%S"`
mv nohup.out ../log/nohup.$d
cur_dir=`pwd`
nohup python -u $cur_dir/../worker/main.py &
