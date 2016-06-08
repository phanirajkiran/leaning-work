bitbake [recipe name] -c devshell
CFLAGS_append = '${@base_conditional("KERNEL_MAJOR_VERSION", "2.6", " -D__Linux26__ ", " -D__Linux24__ ",d)}'
11. How do I add additional packages to a bootstrap-image generated image? 
You can add packages to your build by setting the MACHINE_EXTRA_RDEPENDS or DISTRO_EXTRA_RDEPENDS in a conf file. Note, you must rebuild task-base after changing these variables (bitbake task-base -crebuild) as bitbake has no way of knowing task-base has changed. See [3] for a more detailed explanation


`bitbake -e -b ../openembedded/recipes/meta/bootstrap-image.bb` 
`bitbake -e <package name>` 

Use the OpenEmbedded showdata command. Ex: `bitbake -b ../openembedded/recipes/meta/bootstrap-image.bb -c showdata` 


INITSCRIPT_PARAMS
Scope: Used in recipes when using update-rc.d.bbclass. Mandatory.

Specifies the options to pass to update-rc.d. An example is "start 99 5 2 . stop 20 0 1 6 ." which gives the script a runlevel of 99, starts the script in initlevels 2 and 5 and stops it in levels 0, 1 and 6.

MACHINE_ESSENTIAL_RRECOOMENDS
List of packages required to boot device (usually additional kernel modules)

RRECOMMENDS
List of packages which extend usability of package. Those packages will be automatically installed but can be removed by user.

RREPLACES
List of packages which are replaced with this one.

STAGING_KERNEL_DIR
Directory with kernel headers required to build out-of-tree modules



INHIBIT_AUTO_STAGE = "1"


FILES_libebook = "${libdir}/libebook-*.so.*"
RRECOMMENDS_libebook = "libedata-book"


FILES_${PN}-dev =+ "${libdir}/pkgconfig/evolution-data-server-*.pc"
RRECOMMENDS_${PN}-dev += "libecal-dev libebook-dev"

PACKAGES =+ "${PN}-client ${PN}-stats"
FILES_${PN}-stats = "${sbindir}/mountstats ${sbindir}/nfsiostat"
RDEPENDS_${PN}-stats = "python"

RRECOMMENDS_${PN} = "kernel-module-nfsd"


SRC_URI = "git://tclap.git.sourceforge.net/gitroot/tclap/tclap;protocal=git;branch=master"

COMPATIBLE_MACHINE = "a^" ??????? 

python () {


meta-oe/recipes-support/ckermit/ckermit_301.bb:SRC_URI = "ftp://kermit.columbia.edu/kermit/archives/cku${PV}.tar.gz;subdir=${BPN}-${PV}"
meta-oe/recipes-support/lzma/lzma.inc:SRC_URI = "http://downloads.sourceforge.net/sevenzip/lzma${@d.getVar('PV',1).replace('.','')}.tar.bz2;subdir=${BPN}-${PV} \

BBCLASSEXTEND = "native"


inherit autotools useradd

http://git.yoctoproject.org/cgit/cgit.cgi/poky/tree/meta-skeleton/recipes-skeleton/useradd/useradd-example.bb


bitbake -e  |grep IMAGE_INSTALL 

bitbake -s : show version 
mime-construct                                       :1.11-r0                          
mingetty                                             :1.08-r3                          
mini-x-session                                        :0.1-r4                          
minicom                                               :2.7-r0 

lyang0@pek-test98:/buildarea1/lyang0/x86-clean/bitbake_build$ bitbake-layers show-layers
layer                 path                                      priority
==========================================================================
wrlinux               /buildarea1/lyang0/x86-clean/layers/wrlinux  5
wrlcompat             /buildarea1/lyang0/x86-clean/layers/wrlcompat  5
wr-sdk-toolchain      /buildarea1/lyang0/x86-clean/layers/wr-sdk-toolchain  100
wr-tcwrappers         /buildarea1/lyang0/x86-clean/layers/wr-tcwrappers  6
meta                  /buildarea1/lyang0/x86-clean/layers/oe-core/meta  5
wr-kernel             /buildarea1/lyang0/x86-clean/layers/wr-kernel  6
intel-x86             /buildarea1/lyang0/x86-clean/layers/wr-bsps/intel-x86  7
wr-base               /buildarea1/lyang0/x86-clean/layers/wr-base  6
wr-fixes              /buildarea1/lyang0/x86-clean/layers/wr-fixes  7
wr-tools-profile      /buildarea1/lyang0/x86-clean/layers/wr-tools-profile  7
wr-tools-debug        /buildarea1/lyang0/x86-clean/layers/wr-tools-debug  7
meta-filesystems      /buildarea1/lyang0/x86-clean/layers/meta-openembedded/meta-filesystems  6
meta-initramfs        /buildarea1/lyang0/x86-clean/layers/meta-openembedded/meta-initramfs  8
meta-gnome            /buildarea1/lyang0/x86-clean/layers/meta-openembedded/meta-gnome  7
meta-multimedia       /buildarea1/lyang0/x86-clean/layers/meta-openembedded/meta-multimedia  6
meta-networking       /buildarea1/lyang0/x86-clean/layers/meta-openembedded/meta-networking  5
meta-oe               /buildarea1/lyang0/x86-clean/layers/meta-openembedded/meta-oe  6
meta-python           /buildarea1/lyang0/x86-clean/layers/meta-openembedded/meta-python  7
meta-perl             /buildarea1/lyang0/x86-clean/layers/meta-openembedded/meta-perl  6
meta-webserver        /buildarea1/lyang0/x86-clean/layers/meta-openembedded/meta-webserver  6
meta-xfce             /buildarea1/lyang0/x86-clean/layers/meta-openembedded/meta-xfce  7
