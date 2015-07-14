
          vm0     vm1
          tap0    tap1
              ovsbr0

service openvswitch-switch start

ovs-vsctl add-br ovsbr0

vm1:
qemu-system-x86_64 -enable-kvm -net nic,macaddr=00:11:22:EE:EE:E8 -net tap,script=/etc/openvswitch/ovs-ifup,downscript=/etc/openvswitch/ovs-ifdown -drive file=/boot/guest_raw.test,if=virtio  -kernel /boot/guest.kernel -append "root=/dev/vda rw console=ttyS0,115200"  -nographic

setup: 10.0.2.3
vm2
qemu-system-x86_64 -enable-kvm -net nic,macaddr=00:11:22:EE:EE:E9 -net tap,script=/etc/openvswitch/ovs-ifup,downscript=/etc/openvswitch/ovs-ifdown -drive file=/boot/guest_raw.test,if=virtio  -kernel /boot/guest.kernel -append "root=/dev/vda rw console=ttyS0,115200"  -nographic
setup 10.0.2.4

vm1 can ping eachother but can't ping host,becasue


now:host:

root@intel_5500_server:~# ifconfig 
eth0      Link encap:Ethernet  HWaddr 00:15:17:bb:5e:88  
          inet addr:128.224.165.205  Bcast:128.224.165.255  Mask:255.255.255.0
          inet6 addr: fe80::215:17ff:febb:5e88/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:70670 errors:0 dropped:0 overruns:0 frame:0
          TX packets:41873 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:9489484 (9.0 MiB)  TX bytes:5086757 (4.8 MiB)
          Interrupt:32 Memory:b1960000-b1980000 

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:1021 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1021 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:129799 (126.7 KiB)  TX bytes:129799 (126.7 KiB)

tap0      Link encap:Ethernet  HWaddr 26:02:7b:f3:91:10  
          inet6 addr: fe80::2402:7bff:fef3:9110/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:31 errors:0 dropped:0 overruns:0 frame:0
          TX packets:29 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:500 
          RX bytes:6969 (6.8 KiB)  TX bytes:5205 (5.0 KiB)

tap1      Link encap:Ethernet  HWaddr 0e:ad:bc:00:dd:2e  
          inet6 addr: fe80::cad:bcff:fe00:dd2e/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:23 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:500 
          RX bytes:4737 (4.6 KiB)  TX bytes:1026 (1.0 KiB)

virbr0    Link encap:Ethernet  HWaddr 0e:42:45:d4:55:8a  
          inet addr:192.168.122.1  Bcast:192.168.122.255  Mask:255.255.255.0
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)


to ping host:
root@intel_5500_server:~# ifconfig ovsbr0 10.0.2.2 up


root@intel_5500_server:~# cat /etc/openvswitch/ovs-ifup 
#!/bin/sh
switch="ovsbr0"
ifconfig $1 0.0.0.0 up
ovs-vsctl add-port $switch $1
root@intel_5500_server:~# cat /etc/openvswitch/ovs-ifdown
#!/bin/sh

switch='ovsbr0'
/sbin/ifconfig 0.0.0.0 down
ovs-vsctl del-port ${switch} $1



vlan guest:
vlan guest:
root@wrs-guest:~# modprobe 8021q
8021q: 802.1Q VLAN Support v1.8

root@wrs-guest:~# ifconfig eth0 10.0.2.4 up

root@wrs-guest:~# vconfig add eth0 100
Added VLAN with VID == 100 to IF -:eth0:-
root@wrs-guest:~# ifconfig eth0.100 10.0.2.100
root@wrs-guest:~# ifconfig eth0.100 10.0.2.100 up

can ping host and vm2
===================================================================================================================
