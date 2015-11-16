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
import ConfigParser
from optparse import OptionParser
import os
import re
import sys
from optparse import OptionParser
import ConfigParser
from os.path import expanduser
from string import digits
import pickle
import pprint
from datetime import datetime
from datetime import date
import time
from collections import defaultdict
from collections import Counter


def get_details(configfile):    
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read('%s' %configfile)
    config_dic = {}
    for section in config.sections():
        config_dic[section] = {}
        for option in config.options(section):
            config_dic[section][option] = config.get(section, option)
    return config_dic,config.sections()


def send_email(mail,receiver):
    sender = "lei.yang@windriver.com"
    cc= ["lei.yang@windriver.com"]
    global subject 
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(receiver)
    msg['Cc'] = ", ".join(cc)
    msg['Subject'] = subject
    
    msg.attach(MIMEText(mail, 'html'))
    text = msg.as_string()
    try:
       smtpObj = smtplib.SMTP('147.11.189.50','25')
       smtpObj.sendmail(sender,list(set(receiver+cc)), text)
       print "Successfully sent email"
    except SMTPException:
       print "Error: unable to send email"

def con_jira():
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
    jira = JIRA(options,basic_auth=('apiuser', 'apiuser'))
    return jira

def jira_test(jira,summary,jql):
    try:
	pass
    except:
        pass
    #filter = jira.create_filter(name="testme", description="my filter", jql=jql, favourite=False)
    #print filter.searchUrl
    #print filter.viewUrl 
    #print jira.filter(filter.id)
    global L
    import time
    issue_dict = defaultdict(list)
    ids=[]
    total = 0 
    prioritys=[]
    developers=[]
    componets=[]
    for i in jira.search_issues(jql,maxResults=10000):
        #print i.key
        issue = jira.issue(i.key)
        create_time = time.strptime(issue.fields.created[:19], "%Y-%m-%dT%H:%M:%S")
        create_time = time.strftime("%Y/%m/%d", create_time)
	ids.append(i.key)
	issue_dict[i.key].append(i.key)
	issue_dict[i.key].append(i.key)
	issue_dict[i.key].append(issue.fields.priority.name)
	issue_dict[i.key].append(issue.fields.status)
	issue_dict[i.key].append(issue.fields.summary) #3
	if not issue.fields.components:
	    componet=None
	else:
	    componet=issue.fields.components[0].name
	issue_dict[i.key].append(componet)
        if not issue.fields.assignee:
	    name = None
 	else:
	    name = issue.fields.assignee.displayName
	issue_dict[i.key].append(name)
	issue_dict[i.key].append(issue.fields.reporter.displayName)
	#issue_dict[i.key].append(issue.fields.customfield_10012) #8
	issue_dict[i.key].append(getattr(issue.fields,'customfield_10012',None)) #8
	issue_dict[i.key].append(create_time)
	prioritys.append(issue.fields.priority.name)
	developers.append(name)
	componets.append(componet)
        total = total+1
    pris = Counter(prioritys)
    devs = Counter(developers)
    comps = Counter(componets)
    L += '''
<!DOCTYPE html>
<style>
p.x {
font-family: sans-serif;
font-size: 14px;
line-height: 1.5;
}
p.y {
font-family: sans-serif;
font-size: 12px;
line-height: 1.2;
}
table {
border:1px solid yellowgreen;
border-collapse:collapse;
}
td {
font-family: sans-serif;
font-size: 12px;
border: 1px solid black;
}
u {
    text-bottom: 2px solid black;
  }
</style>
<html>
<body>
'''
    L += "<p class='x'><strong>%s Total: <font size='7' color='blue'> <mark>%s</mark> </font></strong></p>" %(summary,total)
    if len(comps) !=1:
        L += '''</table>'''
        L += "<p class='y'><strong>By Components(sorted)</strong></p>"
        L += '''<table style="width:25%">'''
        for w in sorted(comps, key=comps.get, reverse=True):
            L +='''
  <tr>
    <td width="10%%">%s</td>
    <td width="5%%"><strong>%s</strong></td>          
  </tr>
''' %(w,comps[w])

        L += '''</table>'''


    L += "<p class='y'><strong>By Priority(sorted) </strong></p>"
    L += '''<table style="width:25%">'''
    for w in sorted(pris,reverse=False):
        L +='''
  <tr>
    <td width="7%%">%s</td>
    <td width="5%%"><strong>%s</strong></td>          
  </tr>
''' %(w,pris[w])

    L += '''</table>'''
    L += "<p class='y'><strong>By Developer(sorted)</strong></p>"
    L += '''<table style="width:25%">'''
    for w in sorted(devs, key=devs.get, reverse=True):
        L +='''
  <tr>
    <td width="10%%">%s</td>
    <td width="5%%"><strong>%s</strong></td>          
  </tr>
''' %(w,devs[w])
 
    L += '''</table>'''
    L += "<p class='y'><strong>Details(sorted)</strong></p>"
    L += '''<table style="width:95%">'''
    #for i in jira.search_issues('filter=%s' %filter.id):
    L +='''
  <tr>
    <td width="7%%"><strong>ID</strong></td>
    <td width="5%%"><strong>Priority</strong></td>          
    <td width="5%%"><strong>Status</strong></td>          
    <td width="35%%"><strong>Summary</strong></td>          
    <td width="10%%"><strong>Component/s</strong></td>
    <td width="10%%"><strong>Developer</strong></td>
    <td width="10%%"><strong>reporter</strong></td>
    <td width="10%%"><strong>Tester</strong></td>
    <td width="30%%"><strong>Create date</strong></td>
  </tr>
'''
    for j in ids:
        d=issue_dict[j]
    #for k,d in issue_dict.items():
        L += '''
  <tr>
    <td width="7%%"><a href='https://jira.wrs.com:8443/browse/%s'>%s</a></td>
    <td width="5%%">%s</td>          
    <td width="5%%">%s</td>          
    <td width="35%%">%s</td>
    <td width="10%%">%s</td>
    <td width="10%%">%s</td>
    <td width="10%%">%s</td>
    <td width="10%%">%s</td>
    <td width="30%%">%s</td>
  </tr>
'''%(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9])
#'''% (i.key,i.key,issue.fields.priority,issue.fields.components[0],issue.fields.summary,issue.fields.assignee,issue.fields.customfield_10012,create_time)

        #for j in dir(issue.fields):
	#print issue.fields.labels
    L += '''</table>'''
    #filter.delete()
    issue = jira.issue('SCP7-214')
   # for j in dir(issue.fields):
   #     print j,getattr(issue.fields,j)
    
    return L

parser = OptionParser()
parser.add_option("-t", type="string", dest="to",default="1",help="email whom")
parser.add_option("-c", type="string", dest="configfile",default="1",help="config file")
parser.add_option("-s", type="string", dest="subject",default="1",help="email subject")
(options, args) = parser.parse_args()
to = options.to
configfile = options.configfile
subject = options.subject
subject = "[Send By Utils] %s" %subject
receiver = [x+'@windriver.com' for x in to.split(" ")]
    
L = ""
jira=con_jira()
n=0
config_dic,sections=get_details(configfile)
#for k,v in config_dic.items():
  # print k
for k in sections:
   n=n+1
   jira_test(jira,"%s" %(config_dic[k]['summary']),config_dic[k]['filter'])
send_email(L.encode('utf-8'),receiver)
