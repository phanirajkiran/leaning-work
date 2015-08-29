commit_id=$1
subject=`git show $commit_id --pretty=format:%s |head -1`
echo $subject
for tag in `git tag`
do
    if git log $tag -p  --since='2 month ago' |grep "$subject" -m1 >/dev/null;then 
       echo $tag
    fi
done

