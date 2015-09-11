#!/usr/bin/python -B
import sys
import ConfigParser
from optparse import OptionParser
import os
import re
import sys
from optparse import OptionParser
import ConfigParser
import os
import getpass
from os.path import expanduser
import commands
from string import digits
import pickle
import pprint
    
config = ConfigParser.RawConfigParser()
config.optionxform = str
config.read('./git.ini')
config_dic = {}
for section in config.sections():
    config_dic[section] = {}
    for option in config.options(section):
        config_dic[section][option] = config.get(section, option)
if os.path.exists('mail.txt'):
    os.remove('mail.txt')
mailtext=open("mail.txt", "a")
for key in config_dic.iterkeys():
    mailtext.write('\n')
    mailtext.write('\n')
    if os.path.exists(key):
        commands.getoutput("cd %s;git pull;git fetch --all" %key)
    else:
        commands.getoutput("git clone %s" %(config_dic[key]['location']))
    branch=config_dic[key]['branch']
    if branch == 'auto':
        branch=commands.getoutput("cd %s;git branch -r |grep -v 2013 |tail -1" %key).replace(' ','')
        mailtext.write("*%s*:%s\n" %(key,branch)) 
    else:
	mailtext.write("*%s*\n" %key)
    mailtext.write('=================\n')
    txt=commands.getoutput("cd %s;git log --pretty=format:'%%h %%aN %%cr %%s' --since='1 days ago'  --name-status %s" %(key,branch))
    mailtext.write(txt)
mailtext.write("*Kerenl bugs*\n")
mailtext.write('=================\n')
mailtext.write(commands.getoutput("jiracli --issue-search-by-filter 21808 --no-color 2>/dev/null"))
mailtext.write('\n')
mailtext.write("*Userspace bugs*\n")
mailtext.write('=================\n')
mailtext.write(commands.getoutput("jiracli --issue-search-by-filter 21807 --no-color 2>/dev/null"))
mailtext.close()

#mailtext.write(defect_list)
commands.getoutput("mail -s 'status' lei.yang@windriver.com < ./mail.txt")

