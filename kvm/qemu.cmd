http://doc.opensuse.org/documentation/html/openSUSE/opensuse-kvm/cha.qemu.running.html
http://doc.opensuse.org/products/draft/SLES/SLES-kvm_sd_draft/cha.qemu.running.html


=====================================================
qemu-img create -f raw morespace.raw <size>
qemu-img convert -f qcow2 existing.img -O raw existing.raw
cat morespace.raw >> existing.raw
qemu-img convert -f raw existing.raw -O qcow2 existing-larger.img

#qemu-img convert -O qcow2 /boot/guest_img.raw /boot/guest_img.qcow2;
#qemu-img resize /boot/guest_img.qcow2 100G;


============================================================
qemu-system-x86_64 --enable-kvm -smp 2 -m 512 -net nic,model=e1000 -net tap,script=/etc/qemu-ifup -hda /test.img.raw  -kernel /kernel -append "root=/dev/hda rw console=ttyS0,115200 ip=10.0.2.3 selinux=0" -nographic
#cat /etc/qemu-ifup
#!/bin/sh
/sbin/ifconfig $1 10.0.2.2

============================================
vlan:
http://publib.boulder.ibm.com/infocenter/lnxinfo/v3r0m0/index.jsp?topic=%2Fliaat%2Fliaatbptap.htm

none

    Disables a network card emulation on VM Guest. Only the loopback lo network interface is available. 
nic

    Creates a new Network Interface Card (NIC) and connects it to a specified Virtual Local Area Network (VLAN). For more information, see Section 12.4.1, “Defining a Network Interface Card” 
user

    Specifies a user-mode networking. For more information , see Section 12.4.2, “User-mode Networking”. 
tap

    Specifies a bridged or routed networking. For more information, see Section 12.4.3, “Bridged Networking”. 



QEMU networking options
QEMU networking support includes the following options:

User
    The user option is a networking environment that supports the TCP and UDP protocols. QEMU provides services to the guest operating system such as DHCP, TFTP, SMB, and DNS. QEMU acts as a gateway and a firewall for the guest operating system such that communication from the guest operating system appears to be from the QEMU host.

    You cannot initiate a connection to the guest operating system without help from QEMU. For this type of connection, QEMU provides the redir parameter. The redir parameter redirects TCP or UDP connections from a specific port on the host to a specific port on the guest operating system.

    The user option is the default networking option in QEMU.
Socket
    The socket option is used to connect together the network stacks of multiple QEMU processes. You create one QEMU process that listens on a specified port. Then, you create other QEMU processes that connect to the specified port.
Tap
    The tap option connects the network stack of the guest operating system to a TAP network device on the host. By using a TAP device, QEMU can perform the following actions:

        Receive networking packets from the host network stack and pass the packets to the guest operating system.
        Receive networking packets from the guest operating system and inject the packets into the host network stack.

Use the tap networking option because it provides full networking capability to a guest operating system.


The following example shows the qemu-kvm options you can use to set up multiple interfaces:

-net nic,model=virtio,vlan=0,macaddr=00:16:3e:00:01:01 
-net tap,vlan=0,script=/root/ifup-br0,downscript=/root/ifdown-br0 
-net nic,model=virtio,vlan=1,macaddr=00:16:3e:00:01:02 
-net tap,vlan=1,script=/root/ifup-br1,downscript=/root/ifdown-br1

The example shows two network devices configured for a guest operating system as follows:

    The - net nic command defines a network adapter in the guest operating system. Both network devices are para-virtualized devices which is indicated by the model=virtio value. Both devices also have unique MAC addresses which is indicated by the macaddr values. Each network device is on a different VLAN. The first device is on VLAN 0 and the second network device is on VLAN 1.
    The -net tap command defines how QEMU configures the host. Each network device is added to and removed from a different bridge by using scripts. The first device is added to the br0 bridge by using the /root/ifup-br0 script and removed from the br0 bridge by using the /root/ifdown-br0 script. Similarly, the second network device is added to the br1 bridge by using the /root/ifup-br1 script and removed from the br1 bridge by using the /root/ifdown-br1 script. Each network device is also on a different VLAN. The first device is on VLAN 0 and the second network device is on VLAN 1.


===========================================

A repeat of the same script might do this the very next time:

sudo /bin/tunctl -u myuserid -t kvmtap8358
sudo /sbin/ifconfig kvmtap8358 up 0.0.0.0 promisc
sudo /sbin/brctl addif br8 kvmtap8358

qemu-system-x86_64 -smp 1 -m 512 -usb -localtime <etc> -net nic,vlan=0,model=e1000,macaddr=ac:de:48:6c:5c:a3 -net tap,ifname=kvmtap8358,script=no,vlan=0 <more etc>

sudo /sbin/brctl delif br8 kvmtap8358
sudo /sbin/ifconfig kvmtap8358 down
sudo /bin/tunctl -d kvmtap8358

===============================================

QEMU also defaults to the RTL8139 network interface card (NIC) model. Again this card is compatible with most guests, but does not offer the best performance. If your guest supports it, switch to the virtio model:

 qemu -net nic,model=virtio,mac=... -net tap,ifname=...

Using virtio for the networking

/usr/libexec/qemu-kvm -hda disk.img  -m 512 -net nic,model=virtio -net tap,ifname=tap0,script=no

Using virtio for the storage

/usr/libexec/qemu-kvm -drive file=disk.img,if=virtio,boot=on  -m 512 -net nic,model=virtio -net tap,ifname=tap0,script=no
-
======================================================



To simplify defining of block devices, QEMU understands several shortcuts which you may find handy when entering the qemu-kvm command line.

You can use

qemu-kvm -cdrom /images/cdrom.iso

instead of

qemu-kvm -drive file=/images/cdrom.iso,index=2,media=cdrom

and

qemu-kvm -hda /images/imagei1.raw -hdb /images/image2.raw -hdc \
/images/image3.raw -hdd /images/image4.raw

instead of

qemu-kvm -drive file=/images/image1.raw,index=0,media=disk \
-drive file=/images/image2.raw,index=1,media=disk \
-drive file=/images/image3.raw,index=2,media=disk \
-drive file=/images/image4.raw,index=3,media=disk



===================================================
To access the host CD-ROM drive, use

qemu-kvm [...] -drive file=/dev/cdrom,media=cdrom

To access the host hard disk, use

qemu-kvm [...] -drive file=/dev/hdb,media=disk

=================================================

USB passthrogh usb

tux@vmhost:~> lsusb
[...]
Bus 002 Device 005: ID 12d1:1406 Huawei Technologies Co., Ltd. E1750
[...]

In the above example, we want to assign a USB stick connected to the host's USB bus number 2 with device number 5. Now run the VM Guest with the following additional options:

qemu-kvm [...] -usb -device usb-host,hostbus=2,hostaddr=5


===================================================
PCI passthrogh 

    tux@vmhost:~> lspci -nn
    [...] 00:1b.0 Audio device [0403]: Intel Corporation 82801H (ICH8 Family) \
    HD Audio Controller [8086:284b] (rev 02) [...]

    Note down the device (00:1b.0) and vendor (8086:284b) ID.

    Unbind the device from host Kernel driver and bind it to the PCI stub driver.

    tux@vmhost:~> modprobe pci_stub
    tux@vmhost:~> echo "8086 284b" > /sys/bus/pci/drivers/pci-stub/new_id
    tux@vmhost:~> echo "0000:00:1b.0" > /sys/bus/pci/devices/0000:00:1b.0/driver/unbind
    tux@vmhost:~> echo "0000:00:1b.0" > /sys/bus/pci/drivers/pci-stub/bind

    Now run the VM Guest with the PCI device assigned.

    qemu-kvm [...] -device pci-assign,host=00:1b.0

[Note]	

If the PCI device shares IRQ with other devices, it cannot be assigned to a VM Guest.

KVM also supports PCI device hotplugging to a VM Guest. To achieve this, you need to switch to a QEMU monitor (see Chapter 13, Administrating Virtual Machines with QEMU Monitor for more information) and issue the following commands:

    hot add:

    device_add pci-assign,host=00:1b.0,id=new_pci_device

    hot remove:

    device_del new_pci_device

===================================================================
Example 12.2. User-mode Networking with Custom IP Range¶

qemu-kvm [...] -net user,net=10.2.0.0/81,host=10.2.0.62,dhcpstart=10.2.0.203,\
hostname=tux_kvm_guest4

1
Specifies the IP address of the network that VM Guest sees and optionally the netmask. Default is 10.0.2.0/8.
2
Specifies the VM Host Server IP address that VM Guest sees. Default is 10.0.2.2.
3
Specifies the first of the 16 IP addresses that the built-in DHCP server can assign to VM Guest. Default is 10.0.2.15.
4	
Specifies the hostname that the built-in DHCP server will assign to VM Guest. 


===========================================================
OPTIONS
-daemonize

    'Daemonizes' the QEMU process after it is started. QEMU will detach from the standard input and standard output after it is ready to receive connections on any of its devices. 

==========================================================

qemu -hda imagefile.img -net nic -net tap,ifname=tap0,script=no,downscript=no

==========================================================================
Audio
qemu-system-x86_64 -smp 2 -m 512 -net nic,macaddr=00:01:02:03:04:05,model=virtio -net tap,script=/etc/qemu-ifup -hda /boot/guest_img.qcow2  -device ich9-usb-uhci1,id=usb1 -device usb-audio,id=usb-audio1,bus=usb1.0,port=1 -kernel /boot/bzImage -append "root=/dev/hda rw console=ttyS0,115200 ip=dhcp"  -nographic 


==============================================================================
usb-image
qemu-system-x86_64 -nographic -k en-us -m 1024 -net user,hostname="kvm-guest" -net nic,macaddr=1a:46:0b:ca:bc:7b,model=virtio -drive if=virtio,file=/boot/usb.img -nographic
