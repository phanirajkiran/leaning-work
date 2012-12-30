http://virt-manager.org/
The "Virt Install" tool (virt-install for short command name, virtinst for package name) is a command line tool which provides an easy way to provision operating systems into virtual machines. It also provides an API to the virt-manager application for its graphical VM creation wizard. 

The "Virt Clone" tool (virt-clone for short command name, virtinst for package name) is a command line tool for cloning existing inactive guests. It copies the disk images, and defines a config with new name, UUID and MAC address pointing to the copied disks. 

The "Virt Image" tool (virt-image for short command name, virtinst for package name) is a command line tool for installing guest operating systems based on a pre-defined master image. The image provides metadata describing the requirements of the operating system, minimal resource allocations, and pre-installed disk. 

The "Virtual Machine Viewer" application (virt-viewer for short package name) is a lightweight interface for interacting with the graphical display of virtualized guest OS. It uses GTK-VNC as its display capability, and libvirt to lookup the VNC server details associated with the guest. It is intended as a replacement for the traditional vncviewer client, since the latter does not support SSL/TLS encryption of x509 certificate authentication. 


