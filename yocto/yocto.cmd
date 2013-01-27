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
