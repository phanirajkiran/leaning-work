#!/usr/bin/python
'''
a script to diff the kernel configs for different branches 
'''
import subprocess
from optparse import OptionParser  

#child = subprocess.Popen('ping -c4 blog.linuxeye.com',shell=True)


def checkout_branch(branch):
    current_branch=subprocess.check_output(["git", "describe","--tags"]).strip()
    if branch != current_branch:
        subprocess.call('git checkout %s' %branch,shell=True)
        

def get_configs():
    #configs=subprocess.check_output("find . -name 'Kconfig*' ! -path './drivers/*' -exec grep -P 'config [A-Z]' {} \; |grep -v menuconfig |sed 's/config //g' |sort |uniq",shell=True)
    configs=subprocess.check_output('find -name "Kconfig*" -exec grep "^config [A-Z]" {} \;',shell=True)
    return configs.replace('config ','CONFIG_').split('\n')

def get_diff_configs(configs1,configs2):
    target_configs=[]
    for i in configs1:
        if i not in configs2:
            target_configs.append(i) 
    return target_configs 


def get_final_configs(branch1,branch2):
    checkout_branch(branch1)
    configs1=get_configs()
    checkout_branch(branch2)
    configs2=get_configs()
    obsolete_configs=get_diff_configs(configs1,configs2)
    new_configs=get_diff_configs(configs2,configs1)
    return obsolete_configs,new_configs

def write_configs_to_file(configs,file_name,summary=None):
    if summary:
        with open(file_name,"w") as f:
            f.write("%s\n" %summary)
    for i in configs:
        with open(file_name,"a") as f:
            f.write("%s\n" %i)


def show_branch_configs(branch):
    checkout_branch(branch)
    configs=get_configs()
    write_configs_to_file(configs,"%s_configs" %branch,"This is %s branch's configs")

def show_code_changes(days):
    changes=subprocess.check_output('''git log --pretty=oneline --name-status --since="%s days ago" --no-merges''' %days,shell=True)
    print changes 

parser = OptionParser()  
parser.add_option("-o", "--oldbranch", dest="oldbranch",  
                  help="oldbranch")  
parser.add_option("-n", "--newbranch", dest="newbranch",  
                  help="newbranch")  

parser.add_option("-s", "--show", dest="show_branch",  
                  help="show a branch's configs")  
parser.add_option("-c", "--changes", dest="days",  
                  help="show changes over past days")  

parser.add_option("-q", "--quiet",  
                  action="store_false", dest="verbose", default=True,  
                  help="don't print status messages to stdout")  
(options, args) = parser.parse_args()  
old_branch=options.oldbranch
new_branch=options.newbranch
show_branch=options.show_branch
days=options.days
if old_branch and new_branch:
    obsolete_configs,new_configs=get_final_configs(old_branch,new_branch)
    write_configs_to_file(obsolete_configs,"obsolete_configs","From branch %s to %s" %(old_branch,new_branch))
    write_configs_to_file(new_configs,"new_configs","From branch %s to %s" %(old_branch,new_branch))
if show_branch:
    show_branch_configs(show_branch)
if days:
    show_code_changes(days)
