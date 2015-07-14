pkglists="a b c d e f g"
f()
{
local i
set -- $pkglists 
[ ! -z "$1" ] && sleep 3 & ((i+=2));sleep 3;echo $i
}
f
