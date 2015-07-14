start_build_feature1()
{
	sleep 3
	echo $1
}

start_build_feature2()
{
	sleep 1
	echo $1
}

feature_single1="aa bb c d e f g h i g k l m n u v w x y z"
feature_single2="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15"



f1()
{
        pid_feature1=()
        local i j
        set -- $feature_single1 # NOte $lists IS NOT QUOTED here.

        while [ "$#" -gt 0 ]
        do
                [ ! -z "$1" ] && ((i += 1)) && start_build_feature1 "$1" & pid_feature1[$i]=$!
                [ ! -z "$2" ] && ((i += 1)) && start_build_feature1 "$2" & pid_feature1[$i]=$!
                [ ! -z "$3" ] && ((i += 1)) && start_build_feature1 "$3" & pid_feature1[$i]=$!
                [ ! -z "$4" ] && ((i += 1)) && start_build_feature1 "$4" & pid_feature1[$i]=$!
                [ ! -z "$5" ] && ((i += 1)) && start_build_feature1 "$5" & pid_feature1[$i]=$!
                shift 5
                #for i in ${#pid_feature1[@]}
		for ((j = 1; j <= ${#pid_feature1[@]}; j++))
                do
                        wait ${pid_feature1[$j]}
			echo "start another five in feature_single1"
                done
        done
}

f2()
{
        pid_feature2=()
        local i j
        set -- $feature_single2 # NOte $lists IS NOT QUOTED here.

        while [ "$#" -gt 0 ]
        do
                [ ! -z "$1" ] && ((i += 1)) && start_build_feature2 "$1" & pid_feature2[$i]=$!
                [ ! -z "$2" ] && ((i += 1)) && start_build_feature2 "$2" & pid_feature2[$i]=$!
                [ ! -z "$3" ] && ((i += 1)) && start_build_feature2 "$3" & pid_feature2[$i]=$!
                [ ! -z "$4" ] && ((i += 1)) && start_build_feature2 "$4" & pid_feature2[$i]=$!
                [ ! -z "$5" ] && ((i += 1)) && start_build_feature2 "$5" & pid_feature2[$i]=$!
                shift 5
		for ((j = 1; j <= ${#pid_feature2[@]}; j++))
                #for x in ${#pid_feature2[@]}
                do
                        wait ${pid_feature2[$j]}
			echo "start another five in feature_single"
                done
        done
}
f1 &
f2
