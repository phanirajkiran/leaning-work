commit_id=$1
patch_id=$(git show $commit_id | git patch-id |awk '{print $1}')
for tag in `git tag`
do
    echo "check $tag"
    if git log $tag -p  --since='2 month ago' | git patch-id | grep $patch_id -m1;then
       echo $tag
    fi
done

