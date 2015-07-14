#if after make fs and then make -C build qemu.distclean and make -C build qemu to update the ssated it will contails more dependency so and then you use core-imageinstall it will get the dependency issue  for jboss-as even it doesn't distclean jboss but jobss mayybe full since the build sequence 
#!/bin/bash
PRJ_CONF="$1"
PACKAGES_NUM=$2
FEATURES_NUM=$3
HOME_DIR=`pwd`
RPM="/buildarea1/lyang0/nodel/bitbake_build/tmp/sysroots/x86_64-linux/usr/bin/rpm"
KERNEL="intel-xeon-core"
ROOTFS="ovp-ovirt-engine"
SSTATE="--with-sstate-dir=/buildarea2/lyang0/sstate"
JOBS="--enable-parallel-pkgbuilds=20 --enable-jobs=20"
OTHER_OPT="--enable-reconfig"
BUILD_CMD="$PRJ_CONF --enable-board=$KERNEL --enable-rootfs=$ROOTFS --enable-addons=wr-ovp $JOBS --enable-internet-download=yes --with-license-flags-whitelist=non-commercial $SSTATE $OTHER_OPT"
mkdir -p $HOME_DIR/ldd-logs
mkdir -p $HOME_DIR/summary
get_pkglist()
{
cd $HOME_DIR
if [ -d tmp-dir ];then
	mv tmp-dir xyz-tmp
	rm xyz-tmp -rf &
fi
mkdir -p tmp-dir
cd tmp-dir
eval $BUILD_CMD
wr_ovp_pacakges=`cd layers/wr-ovp/ovp;find ./ -path "./extras.ND" -prune -o -name *.bb -o -name *.bbappend |awk -F/ '{print $NF}' |awk -F_ '{print $1}' |grep -v "image" |grep -v linux-windriver |grep -v task |grep -v extras |sort |uniq`
#meta_java_packages=`cat bitbake_build/pn-depends.dot |grep meta-java |awk '{print $1}' |sed 's/"//gp' |uniq`
meta_virt_packages=`cat bitbake_build/pn-depends.dot |grep meta-virt |awk '{print $1}' |sed 's/"//gp' |uniq`
templates_pkg=`find layers/wr-ovp/ovp/templates -name image.inc -exec cat {} \; |grep "^IMAGE_INSTALL.*\"$" |awk -F"\"" '{print $2}'`
extra_pkgs="socat ltp iproute2 dpdk qat oprofile"
packages="$wr_ovpmgr_packages $wr_ovp_pacakges $meta_java_packages $meta_virt_packages $templates_pkg $extra_pkgs"
#feature_single=`cd layers/wr-ovp/ovp;find ./templates -name template.conf |grep feature |awk -F"/" '{print $(NF-1)}' |grep -v "rt" |xargs`
for layer in wr-base wr-kernel wr-features wr-intel-support wr-ovp/ovp wr-tools-profile wr-ovp/wr-ovpmgr wr-ovp/wr-security wr-tools-debug
do
	cd layers/$layer 
	tmp=`find . -maxdepth 4 -name template.conf |awk -F/ '{print $(NF-1)}' |grep -v default`
	features="$tmp $features"
	cd -
done
feature_single=$features
features=`echo $feature_single |sed -e 's/ /+/g'`
echo $features
echo $packages |xargs -n 1 |sort |uniq > $HOME_DIR/pkglists
cp $HOME_DIR/pkglists $HOME_DIR/summary/pkglists
echo $packages |xargs -n 1 |sort |uniq |grep -v native > $HOME_DIR/pkglists.core_image
cp $HOME_DIR/pkglists.core_image $HOME_DIR/summary/pkglists.core_image
get_bb="cd layers/wr-ovp;find ovp/ -name \$1*.bb"
cat $HOME_DIR/pkglists
#sed -i 's/^/lib32-/g' $HOME_DIR/pkglists
cd $HOME_DIR
mv tmp-dir tmp-dir-del
rm tmp-dir-del -rf &
}

start_single_build()
{
        mkdir -p  $HOME_DIR/single-$1
        cd $HOME_DIR/single-$1
        eval $BUILD_CMD 
	sleep 30
	echo $BUILD_CMD |tee -a  $HOME_DIR/single-build-logs/$1.log
        make -C build $1 2>&1 |tee -a  $HOME_DIR/single-build-logs/$1.log
        if [ ${PIPESTATUS[0]} -ne 0 ];then
        	echo "$1   fail  single-build-logs/$1.log   `eval $get_bb`" >> $HOME_DIR/single-build-logs/single-steps.log
		column -t $HOME_DIR/single-build-logs/single-steps.log >$HOME_DIR/summary/single-steps.log
	else
        	echo "$1   pass  single-build-logs/$1.log   `eval $get_bb`" >> $HOME_DIR/single-build-logs/single-steps.log
		column -t $HOME_DIR/single-build-logs/single-steps.log > $HOME_DIR/summary/single-steps.log
		if ! echo $1 |grep native;then
			
			#version=`cat build/*/$1.spec |awk '/^Version/{print $NF}'`
			#release=`cat build/*/$1.spec |awk '/^Release/{print $NF}'`
			suffix=`echo  build/$1-*/deploy-rpms |awk -F/ '{print $(NF-1)}' |sed -e "s/$1//g"`
			for file in build/$1$suffix/deploy-rpms/*/*.rpm
			do
				if [ -f $file ];then
					echo $file >> $HOME_DIR/ldd-logs/debug.log
        				pkg_basename=`basename $file`
        				pkg_name=`echo $pkg_basename|sed -e "s/$suffix//g"`
        				eval $RPM -qp --requires $file > $HOME_DIR/ldd-logs/$pkg_name.dep
				fi
			done
		fi
	fi
        if ! echo $1 |grep native;then
                echo "IMAGE_INSTALL_append=\"$1\"" >>$HOME_DIR/single-$1/bitbake_build/conf/local.conf
                make -C build core-image-minimal 2>&1 |tee -a  $HOME_DIR/single-build-logs/core-image-$1.log
                if [ ${PIPESTATUS[0]} -eq 0 ];then
                        echo "$1  pass  single-build-logs/core-image-$1.log   `eval $get_bb`" |tee -a  $HOME_DIR/single-build-logs/core-image-steps.log
			column -t $HOME_DIR/single-build-logs/core-image-steps.log > $HOME_DIR/summary/core-image-steps.log
		else
                        echo "$1  fail  single-build-logs/core-image-$1.log   `eval $get_bb`" |tee -a  $HOME_DIR/single-build-logs/core-image-steps.log
			column -t $HOME_DIR/single-build-logs/core-image-steps.log > $HOME_DIR/summary/core-image-steps.log
		fi
        fi
        if [ -f bitbake_build/tmp/qa.log ];then
                cat bitbake_build/tmp/qa.log >> $HOME_DIR/single-build-logs/qa.log
        fi
        cd $HOME_DIR
        mv $HOME_DIR/single-$1 $HOME_DIR/single-$1-del
        rm $HOME_DIR/single-$1-del -rf &
}


build_core_image_minimal()
{
	rm -rf $HOME_DIR/single-build-logs
	mkdir -p $HOME_DIR/single-build-logs
	pkglists=`cat $HOME_DIR/pkglists`
        echo "                                                        "   
	pid_s_build=()                                     
	local i j
        set -- $pkglists # NOte $pkglists IS NOT QUOTED here.

        while [ "$#" -gt 0 ]
        do
		for ((k = 1; k <= ${PACKAGES_NUM}; k++))
		do
			[ ! -z "$(eval echo \$${k})" ] && start_single_build "$(eval echo \$${k})" & a=$! && ((i += 1)) && pid_s_build[$i]=$a
		done
		if [ "$#" -gt ${PACKAGES_NUM} ];then 
                	shift ${PACKAGES_NUM}
			
		else
			shift "$#"
		fi
		for ((j = 1; j <= ${#pid_s_build[@]}; j++))
                do
                        wait ${pid_s_build[$j]}
                done
        done

} 
build_all()
{
        mkdir -p  $HOME_DIR/full
        cd $HOME_DIR/full
        eval $BUILD_CMD
        make fs  2>&1 |tee -a  $HOME_DIR/ldd-logs/all.log
        pkglists=`cat $HOME_DIR/pkglists`
        for pkg in $pkglists
        do
		if ! echo $pkg |grep native;then
			echo $pkg |tee -a $HOME_DIR/summary/full.steps
			#make -C build $pkg 
                	make -C build $pkg.distclean 
			make -C build $pkg |tee -a $HOME_DIR/ldd-logs/$pkg-full-sstate.log
			if [ ${PIPESTATUS[0]} -eq 0 ];then
#				version=`cat build/*/$pkg.spec |awk '/^Version/{print $NF}'`
#                        	release=`cat build/*/$pkg.spec |awk '/^Release/{print $NF}'`
				suffix=`echo  build/$pkg-*/deploy-rpms |awk -F/ '{print $(NF-1)}' |sed -e "s/$pkg//g"`
				for file in build/$pkg$suffix/deploy-rpms/*/*.rpm
                        	do
					if [ -f $file ];then
                                		pkg_basename=`basename $file`
                                		pkg_name=`echo $pkg_basename|sed -e "s/$suffix//g"`
                                		eval $RPM -qp --requires $file > $HOME_DIR/ldd-logs/$pkg_name-full.dep
					fi
                        	done
			else 
				echo $pkg |tee -a $HOME_DIR/ldd-logs/distclean_build.fail
			fi
		fi
        done
        cd $HOME_DIR
        mv $HOME_DIR/full $HOME_DIR/full-delme
        rm $HOME_DIR/full-delme -rf &
}

start_build_feature()
{
        echo "start to build $1" >> $HOME_DIR/single-feature-logs/steps.log
        sleep 3
        mkdir -p  $HOME_DIR/$1
        cd $HOME_DIR/$1
        BUILD_CMD="$PRJ_CONF --enable-board=$KERNEL --enable-rootfs=$ROOTFS+$1 --enable-addons=wr-ovp $JOBS --enable-internet-download=yes --with-license-flags-whitelist=non-commercial $SSTATE $OTHER_OPT"
        eval $BUILD_CMD
	echo $BUILD_CMD  |tee -a  $HOME_DIR/single-feature-logs/$1.log
        make -C build linux-windriver 2>&1  |tee -a  $HOME_DIR/single-feature-logs/$1.log
        if [ ${PIPESTATUS[0]} -eq 0 ];then
                echo "$1   pass  single-feature-logs/$1.log" >> $HOME_DIR/single-feature-logs/fail.log
		column -t $HOME_DIR/single-feature-logs/fail.log > $HOME_DIR/single-feature-logs/fail.log
        else
                echo "$1   fail  single-feature-logs/$1.log" >> $HOME_DIR/single-feature-logs/fail.log
		column -t $HOME_DIR/single-feature-logs/fail.log > $HOME_DIR/single-feature-logs/fail.log
	fi
        cd $HOME_DIR
        mv $HOME_DIR/$1 $HOME_DIR/delme-$1
        rm $HOME_DIR/delme-$1 -rf &

}
build_single_feature()
{
        rm -rf $HOME_DIR/single-feature-logs
        mkdir $HOME_DIR/single-feature-logs
        echo "--------------------------------------------------------" >> $HOME_DIR/single-feature-logs/steps.log
        echo $feature_single >> $HOME_DIR/single-feature-logs/steps.log
        echo "--------------------------------------------------------" >> $HOME_DIR/single-feature-logs/steps.log
        echo "                                                        "  
	pid_feature=()
	local i j
        set -- $feature_single # NOte $lists IS NOT QUOTED here.

        while [ "$#" -gt 0 ]
        do
		for ((k = 1; k <= ${FEATURES_NUM}; k++))
		do
			[ ! -z "$(eval echo \$${k})" ] && start_build_feature "$(eval echo \$${k})" & a=$! && ((i += 1)) && pid_feature[$i]=$a
		done
:<<ABC
		[ ! -z "$3" ] && start_build_feature "$3" & a=$! && ((i += 1)) && pid_feature[$i]=$a
		[ ! -z "$4" ] && start_build_feature "$4" & a=$! && ((i += 1)) && pid_feature[$i]=$a
		[ ! -z "$5" ] && start_build_feature "$5" & a=$! && ((i += 1)) && pid_feature[$i]=$a
ABC
		if [ "$#" -gt ${FEATURES_NUM} ];then 
                	shift ${FEATURES_NUM}
		else
			shift "$#"
		fi
		for ((j = 1; j <= ${#pid_feature[@]}; j++))
		do
			wait ${pid_feature[$j]}
        	done
	done
}

check_dep()
{
        while [[ $over -ne 1 ]]
        do
        sleep 100
	mkdir -p $HOME_DIR/ldd-logs/tmp	
	mv $HOME_DIR/ldd-logs/{*-dbg*,*-staticdev*,*-doc*,*-dev*,*-locale*} $HOME_DIR/ldd-logs/tmp/
        for pkg in `ls $HOME_DIR/ldd-logs/*.dep |awk -F/ '{print $NF}' |sort`
        do
                pkgname=`echo $pkg |grep -v full |sed -e 's/.dep//g'`
                if [[ ! -z $pkgname ]] && [[ -f $HOME_DIR/ldd-logs/$pkgname.dep  && -f $HOME_DIR/ldd-logs/$pkgname-full.dep ]];then
			cat $HOME_DIR/ldd-logs/$pkgname.dep |sed -e 's/(.*//g' -e 's/>=.*//g' |sort |uniq >$HOME_DIR/ldd-logs/$pkgname.data
			cat $HOME_DIR/ldd-logs/$pkgname-full.dep |sed -e 's/(.*//g' -e 's/>=.*//g' |sort |uniq >$HOME_DIR/ldd-logs/$pkgname-full.data
			if [[ `awk 'NR==FNR{a[$0]++;next}(!a[$0])' $HOME_DIR/ldd-logs/$pkgname.data $HOME_DIR/ldd-logs/$pkgname-full.data` != "" ]];then
                        	echo "$pkg requires:"
                        	echo "-----------------------------------"
				awk 'NR==FNR{a[$0]++;next}(!a[$0])' $HOME_DIR/ldd-logs/$pkgname.data $HOME_DIR/ldd-logs/$pkgname-full.data	
                        	echo "-----------------------------------"
                        	echo "                                   "
			fi
                fi
        done > $HOME_DIR/summary/report.dep
	done
}

if [ ! -f pkglists ];then
	get_pkglist
fi
#ppid=$$
#echo $ppid > $HOME_DIR/pid.log
build_all #NOTE: Can' run in the background since I want to get full dependency in the sstate
build_core_image_minimal &
core_image_pid="$$"
#build_all_features &
#build_single_feature &
#check_dep &
wait $core_image_pid
sleep 120
over=1
#check_dep &
