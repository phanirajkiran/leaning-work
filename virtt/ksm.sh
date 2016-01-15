#!/bin/bash
MEM=1024

for i in {1..10}; do
        echo "====> Starting a new vm..."
        # Remove the old backing file
        rm -f guest_img-$i.qcow2

        # Create a new backing file that is a qcow2 snapshot of the original file
        qemu-img create -f qcow2 -b $BACKING_FILE guest_img-$i.qcow2

        # Actually start the intstance
        /usr/bin/qemu-system-x86_64 \
        -M pc-1.0 \
        -smp 2,sockets=2,cores=1,threads=1 \
        -enable-kvm \
        -m $MEM \
        -drive file=guest_img-$i.qcow2,if=virtio \
        -boot d \
        -net nic,model=virtio \
        -net user \
        -nographic \
        -vnc :$i \
        -device virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x5 \
        -daemonize

        # Let's just sleep for a few seconds...
        echo "====> Sleeping for $SLEEP..."
        sleep $SLEEP
done


if grep KSM /boot/config-`uname –r`;then
        echo "you doesn't enable KSM in the kernel config"
        exit 1
fi

if [ "`cat /sys/kernel/mm/ksm/run`" -ne 1 ] ; then
        echo "KSM is not enabled. Run echo 1 > /sys/kernel/mm/ksm/run to enable it"
        exit 1
else
        SHEM=$((`cat /sys/kernel/mm/ksm/pages_shared`*`getconf PAGE_SIZE`/1024/1024))
        echo Shared memory is ${SHEM} MB
        if [ $SHEM -gt 0 ];then
                echo "KSM:PASS"
        fi
fi

