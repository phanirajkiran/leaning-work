#!/usr/bin/expect
exec ping 128.224.165.20 &
sleep 10
exec killall -2 ping
