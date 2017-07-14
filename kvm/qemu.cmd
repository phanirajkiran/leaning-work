http://doc.opensuse.org/documentation/html/openSUSE/opensuse-kvm/cha.qemu.running.html
http://doc.opensuse.org/products/draft/SLES/SLES-kvm_sd_draft/cha.qemu.running.html
http://gmplib.org/~tege/qemu.html

=====================================================
qemu-img create -f raw morespace.raw <size>
qemu-img convert -f qcow2 existing.img -O raw existing.raw
cat morespace.raw >> existing.raw
qemu-img convert -f raw existing.raw -O qcow2 existing-larger.img

#qemu-img convert -O qcow2 /boot/guest_img.raw /boot/guest_img.qcow2;
#qemu-img resize /boot/guest_img.qcow2 100G;
 sudo brctl showstp $bridge_name

============================================================
qemu-system-x86_64 --enable-kvm -smp 2 -m 512 -net nic,model=e1000 -net tap,script=/etc/qemu-ifup.tap -hda /boot/guest_img.raw  -kernel /boot/bzImage -append "root=/dev/hda rw console=ttyS0,115200 ip=10.0.2.5 selinux=0" -nographic
#cat /etc/qemu-ifup
#!/bin/sh
/sbin/ifconfig $1 10.0.2.2
=========================================================
virtio:

qemu-system-x86_64 --enable-kvm -smp 2 -m 512 -net nic,macaddr=00:01:02:03:04:05,model=virtio -net tap,script=/etc/qemu-ifup -hda /boot/guest_img.raw  -kernel /boot/bzImage -append "root=/dev/hda rw console=ttyS0,115200 ip=dhcp"  -nographic

OR change the disk

qemu-system-x86_64 -smp 2 -m 512 -net nic,macaddr=00:01:02:03:04:05,model=virtio -net tap,script=/etc/qemu-ifup -hda /boot/guest_img.raw  -kernel /boot/bzImage -append "root=/dev/sda rw console=ttyS0,115200 ip=dhcp"  -nographic

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


http://qemu.weilnetz.de/qemu-doc.html#host_005fusb_005fdevices
http://www.linux-kvm.org/page/USB_Host_Device_Assigned_to_Guest

#/usr/bin/qemu-kvm -m 1024 -name f15 -drive file=/images/f15.img,if=virtio -usb -device usb-host,hostbus=2,hostaddr=3

http://www.linux-kvm.org/page/USB

sudo losetup /dev/loop0 usb.img
qemu -hda root.img -usbdevice disk:/dev/loop0


qemu-system-ppc -m 1024 -hda ubuntu-ppc.qcow2 \
    -cdrom ubuntu-10.04-server-powerpc.iso -boot d \
    -usb -usbdevice disk:ubuntu-10.04-server-powerpc.iso

qemu-system-x86_64 -no-acpi -usb -usbdevice host:096e:0305 -m 1024 -hda win7.img -cdrom winxp.iso


qemu -usb -usbdevice keyboard 
qemu -usb -usbdevice disk:/dev/sda
qemu -usb -usbdevice host:5.7 -fda usb.img


qemu -usb -usbdevice disk:/dev/sda -fda usb.img

The -L tells QEMU where to find its BIOS images, which is not necessary in a standard unix installation. The -m tells how many megabytes of memory to use; the default is 128
You can use -fda/-fdb for disk image files, and -hda/-hdb/-hdc/-hdd for hard disks. To change boot devices, use -boot {a/b/c/d}. a/b tell it to boot floppy a or b. c for hard disk and d for CDROM.


However I've found another solution. Get the USB device VendorID:ProductID with lsusb. Example:

$ lsusb
...
Bus 002 Device 007: ID 0781:5406 SanDisk Corp. Cruzer Micro U3
Pass that to KVM, and ask for the boot menu:

sudo  kvm -m 512 -smp 1 -drive file=/path/to/hardisk/file.img -usb \ 
-usbdevice host:0781:5406 -boot menu=on
Press F12 for the menu, choose the usb device, it works. There's probably a way to command the usb boot without needing to call the boot menu, but I didn't find any in man kvm.

qemu-system-x86_64 -snapshot -L test -device piix3-usb-uhci -drive id=usbflash,file=dos-drivec-new,if=none,cache=writeback -device usb-storage,drive=usbflash -chardev stdio,id=seabios -device isa-debugcon,iobase=0x402,chardev=seabios

If a hard disk image is added too, i.e.
qemu-system-x86_64.exe -boot menu=on -L . -m 256 -usb -usbdevice disk://./PhysicalDrive1 -hda test.imgit defaults to booting it, so USB boot can be used via F12 only. 

********************************************************************************************************************************************************************
wrs:

root@intel_5500_server:/opt/kvm/virt-test# lsusb
Bus 002 Device 003: ID 1307:0165 Transcend Information, Inc. 2GB/4GB Flash Drive
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 005 Device 002: ID 046b:ff10 American Megatrends, Inc. 
Bus 005 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 006 Device 002: ID 413c:2105 Dell Computer Corp. Model L100 Keyboard
Bus 006 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 003 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 004 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 007 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 008 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub

1)qemu-system-x86_64 -nographic -k en-us -m 1024 -net user,hostname="kvm-guest" -net nic,macaddr=1a:46:0b:ca:bc:7b,model=virtio -drive if=virtio,file=/boot/usb.img -usb -usbdevice host:1307:0165 -nographic

OR

2)qemu-system-x86_64 -nographic -k en-us -m 1024 -net user,hostname="kvm-guest" -net nic,macaddr=1a:46:0b:ca:bc:7b,model=virtio -drive if=virtio,file=/boot/usb.img -usb -device usb-host,hostbus=2,hostaddr=3  -nographic


qemu-system-x86_64 -nographic -k en-us -m 1024 -net user,hostname="kvm-guest" -net nic,macaddr=1a:46:0b:ca:bc:7b,model=virtio -device ich9-usb-uhci1 -drive id=aaaaaa,file=/boot/usb.img,if=none -device usb-storage,drive=aaaaaa -nographic

root@localhost:~# df . -h 
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       1.9G  1.5G  309M  83% /
root@localhost:~# ls /dev/sda2
/dev/sda2
root@localhost:~# mount /dev/sda1 /mnt 
root@localhost:~# ls ./mnt
ls: cannot access ./mnt: No such file or directory
root@localhost:~# ls /mnt
help.txt  isolinux.bin	menu.c32    splash.txt	  vesamenu.c32
initrd	  ldlinux.sys	splash.lss  syslinux.cfg  vmlinuz


root@localhost:/sys# find . -name sda*
./devices/pci0000:00/0000:00:04.0/usb1/1-1/1-1:1.0/host0/target0:0:0/0:0:0:0/block/sda
./devices/pci0000:00/0000:00:04.0/usb1/1-1/1-1:1.0/host0/target0:0:0/0:0:0:0/block/sda/sda1
./devices/pci0000:00/0000:00:04.0/usb1/1-1/1-1:1.0/host0/target0:0:0/0:0:0:0/block/sda/sda2
./block/sda
./class/block/sda
./class/block/sda1
./class/block/sda2
root@localhost:/sys# find . -name hdc 
./devices/pci0000:00/0000:00:01.1/ide1/1.0/block/hdc
./block/hdc
./class/block/hdc
root@localhost:/sys# lspci 
00:00.0 Host bridge: Intel Corporation 440FX - 82441FX PMC [Natoma] (rev 02)
00:01.0 ISA bridge: Intel Corporation 82371SB PIIX3 ISA [Natoma/Triton II]
00:01.1 IDE interface: Intel Corporation 82371SB PIIX3 IDE [Natoma/Triton II]
00:01.3 Bridge: Intel Corporation 82371AB/EB/MB PIIX4 ACPI (rev 03)
00:02.0 VGA compatible controller: Cirrus Logic GD 5446
00:03.0 Ethernet controller: Red Hat, Inc Virtio network device
00:04.0 USB controller: Intel Corporation 82801I (ICH9 Family) USB UHCI Controller #1 (rev 03)
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


==========================================
virsh console vm1 

virsh start vm1 --console 


/usr/bin/kvm -M pc -m 2048 -smp 4 -monitor pty -drive file=/var/lib/libvirt/images/<vm_name>.img,if=ide,boot=on -net nic,macaddr=00:16:ff:09:28:1e,vlan=0 -net tap,fd=4,script=,vlan=0 -usb -vnc 127.0.0.1:1 
char device redirected to /dev/pts/1

from fupan:
qemu-system-ppc --enable-kvm -smp 2 -kernel /root/uImage.new -nographic -M mpc8544ds -drive if=virtio,file=/root/hd.disk -append "console=ttyS0 ip=dhcp root=/dev/vda" -netdev type=user,id=mynet0 -device e1000,netdev=mynet0 -m 512

tap:

/usr/bin/qemu-system-x86_64 -enable-kvm -smp 8 -m 1024 -net nic,macaddr=de:ef:be:ad:c6:f3,model=virtio -net tap,ifname=tap1,script=/etc/qemu-ifup.tap -drive file=/boot/guest_raw.test,if=virtio  -kernel /boot/guest.kernel -append "root=/dev/vda rw console=ttyS0,115200 "  -nographic


cpu flags:


qemu-system-x86_64 -cpu qemu64,+x2apic -enable-kvm -net nic,macaddr=52:54:00:EE:EE:E1,model=virtio -net tap,script=/etc/ovs-br-ifup,downscript=/etc/ovs-br-ifdown -drive file=/boot/guest_raw.test,if=virtio  -kernel /boot/guest.kernel -append "root=/dev/vda rw console=ttyS0,115200 ip=192.168.2.2"  -nographic


add a usb disk
qemu-system-x86_64 -enable-kvm -smp 2 -m 1G,slots=3,maxmem=4G -net nic,macaddr=00:01:02:03:04:06,model=virtio          -net tap,script=../../configs/qemu-ifup.tap  -drive file=/tmp/vm2 -drive if=none,id=uas-disk1,file=/tmp/vm2 -device nec-usb-xhci,id=xhci -device usb-uas,id=uas,bus=xhci.0 -device scsi-hd,bus=uas.0,scsi-id=0,lun=0,drive=uas-disk1          -kernel /boot/kernel -append "root=/dev/sda rw console=ttyS0,115200 ip=dhcp"  -nographic 
