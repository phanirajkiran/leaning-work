root@intel_5500_server:~# cat /etc/qemu-ifup.tap 
#!/bin/sh
/sbin/ifconfig $1 0.0.0.0
brctl addif br0 $1


root@intel_5500_server:~# vconfig add eth1 101
root@intel_5500_server:~# brctl addbr br0
root@intel_5500_server:~# brctl addif br0 eth1
root@intel_5500_server:~# brctl show
bridge name	bridge id		STP enabled	interfaces
br0		8000.001517bb5e89	no		eth1.101
							tap1
virbr0		8000.000000000000	yes		

root@intel_5500_server:~# ifconfig br0 10.0.2.8 up
root@intel_5500_server:~# ifconfig 
br0       Link encap:Ethernet  HWaddr 00:15:17:bb:5e:89  
          inet addr:10.0.2.8  Bcast:10.255.255.255  Mask:255.0.0.0
          inet6 addr: fe80::215:17ff:febb:5e89/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:12 errors:0 dropped:0 overruns:0 frame:0
          TX packets:45 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:848 (848.0 B)  TX bytes:7867 (7.6 KiB)

eth0      Link encap:Ethernet  HWaddr 00:15:17:bb:5e:88  
          inet addr:128.224.165.205  Bcast:128.224.165.255  Mask:255.255.255.0
          inet6 addr: fe80::215:17ff:febb:5e88/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:77521 errors:0 dropped:0 overruns:0 frame:0
          TX packets:47459 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:10432211 (9.9 MiB)  TX bytes:5794201 (5.5 MiB)
          Interrupt:32 Memory:b1960000-b1980000 

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:1034 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1034 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:131087 (128.0 KiB)  TX bytes:131087 (128.0 KiB)

tap1      Link encap:Ethernet  HWaddr 16:44:2f:9b:30:50  
          inet6 addr: fe80::1444:2fff:fe9b:3050/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:150 errors:0 dropped:0 overruns:0 frame:0
          TX packets:50 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:500 
          RX bytes:12720 (12.4 KiB)  TX bytes:8289 (8.0 KiB)

virbr0    Link encap:Ethernet  HWaddr 0e:42:45:d4:55:8a  
          inet addr:192.168.122.1  Bcast:192.168.122.255  Mask:255.255.255.0
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

/usr/bin/qemu-system-x86_64 -enable-kvm -smp 8 -m 1024 -net nic,macaddr=de:ef:be:29:07:3e,model=virtio -net tap,script=/etc/qemu-ifup.tap -drive file=/boot/guest_raw.test,if=virtio  -kernel /boot/guest.kernel -append "root=/dev/vda rw console=ttyS0,115200 "  -nographic

then guest can ping host (br0 must have a ip)
----------------------------

root@intel_5500_server:~# ifconfig eth1 up             
root@intel_5500_server:~# ifconfig eth1.101 10.0.2.9 up
root@intel_5500_server:~# 

and then guest can ping 10.0.2.9 (even eth1 no ip)

switch must be up 
