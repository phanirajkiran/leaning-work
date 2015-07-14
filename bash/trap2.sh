trap_sig()
{
for sig in SIGHUP SIGINT SIGQUIT SIGABRT SIGKILL SIGALRM SIGTERM EXIT; do
#    trap 'cleanup "$sig"' $sig
     trap 'echo "caught signal '$sig'..."' $sig
done
}

cleanup()
{
 echo "caught signal '$1'..."
}
echo $$
trap_sig
read
