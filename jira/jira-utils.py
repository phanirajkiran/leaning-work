#!/usr/bin/env python

import smtplib
from smtplib import SMTPException
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys
from optparse import OptionParser
import ConfigParser
import getpass
from os.path import expanduser
import commands


parser = OptionParser()
parser.add_option("-p", "--path",  \
                 action="store", type="string", dest="path",help="test case path")
parser.add_option("-a", "--assignee",  \
                 action="store", type="string", dest="assignee",help="assign defect to assignee")
parser.add_option("-r", "--reivewer",  \
                 action="store", type="string", dest="reivewer",help="defect reivewer")
parser.add_option("-u", "--userstory",  \
                 action="store", type="string", dest="userstory",help="userstory")
parser.add_option("-j", action="store_true", dest="jira_create",help="create jira defect")
(options, args) = parser.parse_args()
path = options.path
userstory = options.userstory
assignee = options.assignee
reivewer = options.reivewer
if not userstory:
    userstory = NA
jira_create = options.jira_create

problem=commands.getoutput('cat %s |grep -B 1 -A 1 "ERROR CMD OR INFO IS"'%path)
details=commands.getoutput('cat %s |sed -n "/Start testcase/,/End testcase/p"'%path)
step = commands.getoutput("cat %s |sed  '1,/Testing Env/d'|sed '1d'" %path)

sender = "lei.yang@windriver.com"
#receiver = ['lei.yang@windriver.com','%s@windriver.com' %reivewer]
receiver = ['lei.yang@windriver.com','CDC-ENG-Linux-core-test@windriver.com','%s@windriver.com' %reivewer]
subject = "[Bug Review] %s failed" %(commands.getoutput("cat %s |awk -Ftestcase '/Start testcase/{print $2}'" %path))
text_mail='mail'
txt=open(text_mail, "a")
txt.write('o Peer Reviewer:\n\n')
txt.write('%s\n\n' %reivewer)
txt.write('1. Priority\n')
txt.write('****************************\n\n')
txt.write('2\n\n')
txt.write('2. Repeatability :\n')
txt.write('****************************\n\n')
txt.write('reproducible\n\n')
txt.write('3. Summary:\n')
txt.write('****************************\n\n')
txt.write('4. Engineering Details (Not Published):\n\n')
txt.write('****************************\n\n')
txt.write('Environment\n')
txt.write('======================\n\n')
txt.write('Requirement No.: %s\n' %userstory)
txt.write('WRLinux Version: 8.0.0.0\n\n')
txt.write('5. Symptom Details\n\n')
txt.write('****************************\n\n')
txt.write('Problem Description\n\n')
txt.write(problem)
txt.write('\n\n')
txt.write(details)
txt.write('\n\n')
txt.write('6. Steps To Reproduce\n')
txt.write('****************************\n\n')
txt.write(step)
txt.close()
if not jira_create:
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(receiver)
    msg['Subject'] = subject
    
    file = open(text_mail, 'r')
    body = "%s" %(file.read())
    file.close()
    commands.getoutput('rm -rf %s' %text_mail)
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    try:
       smtpObj = smtplib.SMTP('147.11.189.50','25')
       smtpObj.sendmail(sender,receiver, text)         
       print "Successfully sent email"
    except SMTPException:
       print "Error: unable to send email"

if jira_create:
    from jira.client import JIRA
    
    # By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK
    # (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
    # Override this with the options parameter.
    options = {
        'server': 'https://jira.wrs.com:8443'
    }
    
    
    from jira import JIRA
    
    # By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK.
    # See
    # https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK
    # for details.
    jira = JIRA(options,basic_auth=('apiuser', 'apiuser'))    # a username/password tuple
    
    # Find all issues reported by the admin
    #issues = jira.search_issues('assignee=lyang0')
    subject = "ignore me %s failed" %(commands.getoutput("cat %s |awk -Ftestcase '/Start testcase/{print $2}'" %path))
    issue_dict = {
        #issue.fields.project.key
        #'project': {'key': 'LIN8'},
        'project': {'key': 'LTAF6'},
        'issuetype': {'name': 'Bug'},
        'summary': subject,
        'priority': {'name': 'P2'},
        'customfield_10605': {'value':'Standard'},
        #'components': [{'name': 'BSP'}],
        'components': [{'name': 'Test Infrastructure'}],
        'description': details,
        'customfield_11001': step,
        'reporter': {'name': 'lyang0'},
        #'customfield_11000': [{'name': '8.0'}],
        'customfield_11000': [{'name': '6.0'}],
        'customfield_11201': userstory,
        'assignee': {'name': assignee},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    issue = jira.issue(new_issue)
    #associate the jira with rally 
    issue.update(customfield_11201=userstory)
    print 'https://jira.wrs.com:8443/browse/%s' %new_issue

