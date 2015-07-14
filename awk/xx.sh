cp xx xx.report
awk '
(NR==1)		{min=$2;max=$2;typ=$3}
($2<min)	{min=$2}
($2>max)	{max=$2}
		{tot+=$2}
END	{print "min: " min " " typ " avg: " tot/NR " " typ " max: " max " " typ }' xx >> xx.report
