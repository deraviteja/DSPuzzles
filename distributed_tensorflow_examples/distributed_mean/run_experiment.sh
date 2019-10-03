#!/usr/bin/env bash

size=1000000000
python sequential.py ${size} > sequential.log

python worker.py 0 & echo $! > worker0.pid
python worker.py 1 & echo $! > worker1.pid

python master.py ${size} > master.log

kill `cat worker0.pid`
kill `cat worker1.pid`