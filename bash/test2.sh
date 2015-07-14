#!/bin/bash
#set -x 
feature_single="1 2 3 4 5 6 7 8 9 10"
pkglists="a b c d e f g h i j k  l m n"




start_build_feature()
{
	sleep 2
	echo $1
}
start_single_build()
{
	sleep 1
	echo $1
}

build_core_image_minimal()
{
        pid_s_build=()
#        local i j
        set -- $pkglists # NOte $pkglists IS NOT QUOTED here.

        while [ "$#" -gt 0 ]
        do
                [ ! -z "$1" ] && start_single_build "$1" & a=$! && ((i += 1)) && pid_s_build[$i]=$a
#		echo xxxxxxxxxxx ${pid_s_build[$i]}
                [ ! -z "$2" ] && start_single_build "$2" & a=$! && ((i += 1)) && pid_s_build[$i]=$a
:<<abc
                [ ! -z "$3" ] && ((i += 1)) && start_single_build "$3" & pid_s_build[$i]=$!
                [ ! -z "$4" ] && ((i += 1)) && start_single_build "$4" & pid_s_build[$i]=$!
                [ ! -z "$5" ] && ((i += 1)) && start_single_build "$5" & pid_s_build[$i]=$! 
                [ ! -z "$6" ] && ((i += 1)) && start_single_build "$6" & pid_s_build[$i]=$! 
                [ ! -z "$7" ] && ((i += 1)) && start_single_build "$7" & pid_s_build[$i]=$! 
                [ ! -z "$8" ] && ((i += 1)) && start_single_build "$8" & pid_s_build[$i]=$! 
                [ ! -z "$9" ] && ((i += 1)) && start_single_build "$9" & pid_s_build[$i]=$! 
abc
                shift 2
		#echo ${pid_s_build[1]}
                for ((j = 1; j <= ${#pid_s_build[@]}; j++))
                do
		#	echo aaaa ${pid_s_build[$j]}
                        wait ${pid_s_build[$j]}
                done
                echo "start another five package" 
        done

}



build_single_feature()
{
        pid_feature=()
        local i j
        set -- $feature_single # NOte $lists IS NOT QUOTED here.

        while [ "$#" -gt 0 ]
        do
                [ ! -z "$1" ] && start_single_build "$1" & a=$! && ((i += 1)) && pid_feature[$i]=$a
                [ ! -z "$2" ] && start_single_build "$2" & a=$! && ((i += 1)) && pid_feature[$i]=$a
:<<ABC
                [ ! -z "$3" ] && ((i += 1)) && start_build_feature "$3" & pid_feature[$i]=$!
                [ ! -z "$4" ] && ((i += 1)) && start_build_feature "$4" & pid_feature[$i]=$!
                [ ! -z "$5" ] && ((i += 1)) && start_build_feature "$5" & pid_feature[$i]=$!
                [ ! -z "$6" ] && ((i += 1)) && start_build_feature "$6" & pid_feature[$i]=$!
                [ ! -z "$7" ] && ((i += 1)) && start_build_feature "$7" & pid_feature[$i]=$!
                [ ! -z "$8" ] && ((i += 1)) && start_build_feature "$8" & pid_feature[$i]=$!
                [ ! -z "$9" ] && ((i += 1)) && start_build_feature "$9" & pid_feature[$i]=$!
ABC
                shift 2
                for ((j = 1; j <= ${#pid_feature[@]}; j++))
                do
                        wait ${pid_feature[$j]}
                done
                echo "start another five feature" 
        done
}
build_single_feature &
build_core_image_minimal &
wait
echo "game over"
