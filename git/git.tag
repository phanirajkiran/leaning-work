
> git tag -l "task_*" --since v0.1.1

To get output like the following.

task_2043
task_2311


> git tag --contains v0.1.1
v0.1.1
task_2043
task_2311
v0.1.2`


git tag -a v5.2 c63a164 -m "Message here"

#Don't use the log commit id 

git log --tags --simplify-by-decoration --pretty="format:%ai %d"
https://stackoverflow.com/questions/6900328/git-command-to-show-all-lightweight-tags-creation-dates
