#!/bin/sh
./rally_utils.py -u $ -o "Wei Gao" -t "kgdb"
#./rally_utils.py -u $1 -o "Wei Gao" -t "kexec"
./rally_utils.py -u $1 -o "Wei Gao" -t "kdump"
./rally_utils.py -u $1 -o "Wei Gao" -t "gdbserver"
