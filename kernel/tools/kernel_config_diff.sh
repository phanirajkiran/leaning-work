#!/bin/bash
#old tag
if [ X`git describe --tags` != X"$1" ];then 
    git checkout $1
fi
config1=`find . -name "Kconfig*" ! -path "./drivers/*" -exec grep -P "config [A-Z]" {} \; |grep -v menuconfig |sed 's/config //g' |sort |uniq`
#new tag 
git checkout $2
config2=`find . -name "Kconfig*" ! -path "./drivers/*" -exec grep -P "config [A-Z]" {} \; |grep -v menuconfig |sed 's/config //g' |sort |uniq`


rm obsolete.configs new.configs -rf 

get_obsolete_configs()
{
    for i in $config1
    do
         if [[ X`echo $config2 |grep $i` == X"" ]];then
    	obsolete_configs="$obsolete_configs $i" 
    	echo $i >> i
         fi
    done
    
    echo "from $1 to $2,obsolete kernel configs are:" >> obsolete.configs
    for i in $obsolete_configs
    do
        echo "$i" >> obsolete.configs
    done
}

get_new_configs()
{
    for i in $config2
    do
         if [[ X`echo $config1 |grep $i` == X"" ]];then
    	new_configs="$new_configs $i" 
         fi
    done
    
    echo "from $1 to $2,new kernel configs are:" >> new.configs
    for i in $new_configs
    do
        echo "$i" >> new.configs
    done
}

get_latest_configs()
{
    echo "all of the new kernel configs are:" >> all.configs
    for i in $config2
    do
        echo "$i" >> all.configs
    done
}


get_obsolete_configs &
get_new_configs &
get_latest_configs &

wait
