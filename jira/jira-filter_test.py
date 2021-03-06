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
import requests


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
    #sender = "%s@windriver.com" %getpass.getuser()
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

def draw_table1(L,comments,var_dict,flag):
    L += '''</table>'''
    L += "<p class='y'><strong>%s</strong></p>" %comments
    L += '''<table style="width:25%">'''
    for w in sorted(var_dict, key=var_dict.get, reverse=flag):
        L +='''
  <tr>
    <td width="10%%">%s</td>
    <td width="5%%"><strong>%s</strong></td>          
  </tr>
''' %(w,var_dict[w])
    L += '''</table>'''
    return L

def draw_table0(L,comments,var_list,var_dict,first,num):
    if len(var_list) !=0:
        L += "<p class='x'><strong>%s</strong></p>" %comments
        L += '''<table style="width:75%">'''
        L +='''
  <tr>
    <td width="10%%"><strong>%s</strong></td>
''' %first
        L +='''
    <td width="7%%"><strong>ID</strong></td>
    <td width="5%%"><strong>Priority</strong></td>          
'''
        if num != 3:
            L +='''
    <td width="5%%"><strong>Status</strong></td>          
'''
        L +='''
    <td width="35%%"><strong>Summary</strong></td>          
    <td width="6%%"><strong>Component/s</strong></td>
    <td width="8%%"><strong>Developer</strong></td>
    <td width="8%%"><strong>reporter</strong></td>
    <td width="10%%"><strong>Create date</strong></td>
    <td width="10%%"><strong>Fix version</strong></td>
  </tr>
''' 
        for i in var_list:
            b=var_dict[i]
            if num ==10:
                L += '''
  <tr>
    <td width="10%%"><strong><font color='red'>%s</font></strong></td>
''' %(','.join(b[10]))
            elif num ==3:
                L += '''
  <tr>
    <td width="10%%"><strong><font color='red'>%s</font></strong></td>
''' %(b[3])
            L += '''
    <td width="7%%"><a href='https://jira.wrs.com:8443/browse/%s'>%s</a></td>
    <td width="5%%">%s</td>
'''%(b[0],b[1],b[2])
            if num != 3:
                L +='''   
    <td width="5%%">%s</td>
''' %b[3]
            L +='''
    <td width="35%%">%s</td>
    <td width="6%%">%s</td>
    <td width="8%%">%s</td>
    <td width="8%%">%s</td>
    <td width="10%%">%s</td>
    <td width="10%%">%s</td>
  </tr>
'''%(b[4],b[5],b[6],b[7],b[9],b[11])
        L += '''</table>'''
        return L
    else:
        return L

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
    #total = 0 
    global total
    prioritys=[]
    developers=[]
    componets=[]
    reporters=[]
    today=datetime.now().strftime('%Y-%m-%d')
    print jira.search_issues(jql,maxResults=100000)
    for i in jira.search_issues(jql,maxResults=100000):
        #print i.key
        issue = jira.issue(i.key)
        create_time = time.strptime(issue.fields.created[:19], "%Y-%m-%dT%H:%M:%S")
        create_time = time.strftime("%Y/%m/%d", create_time)
	d0=date(int(today.split('-')[0]),int(today.split('-')[1]),int(today.split('-')[2]))
	integrate_time=getattr(issue.fields,'customfield_12407',None)
	if integrate_time:
            integrate_time = time.strptime(integrate_time[:19], "%Y-%m-%dT%H:%M:%S")
            integrate_time = time.strftime("%Y/%m/%d", integrate_time)
	    integrate_time = datetime.strptime(integrate_time, "%Y/%m/%d")
	    d1=date(int(integrate_time.strftime("%Y")),int(integrate_time.strftime("%m")),int(integrate_time.strftime("%d")))
	    woh=(d0-d1).days	
	else:
	    woh=None
	
        ids.append(i.key)
        issue_dict[i.key].append(i.key)
        issue_dict[i.key].append(i.key)
        issue_dict[i.key].append(issue.fields.priority.name)
        issue_dict[i.key].append(issue.fields.status)
        issue_dict[i.key].append(issue.fields.summary) #4
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
        issue_dict[i.key].append(getattr(issue.fields,'labels',None))
        issue_dict[i.key].append(getattr(issue.fields,'customfield_11002',None)) #11
        issue_dict[i.key].append(woh) #12
        prioritys.append(issue.fields.priority.name)
        developers.append(name)
        componets.append(componet)
        reporters.append(issue.fields.reporter.displayName)
        #print issue.fields.labels
        total = total+1
    pris = Counter(prioritys)
    devs = Counter(developers)
    comps = Counter(componets)
    reps = Counter(reporters)
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
    blocker=[]
    new_incomplete=[]
    for i in ids:
        if any("BLOCKING" in s for s in issue_dict[i][10]):
            blocker.append(i)
        #print issue_dict[i][3]
        if "New_Incomplete" == "%s" %issue_dict[i][3]:
            new_incomplete.append(i)
    if "1" not in not_show:
        L=draw_table0(L,"Blocking defects : %s" %len(blocker),blocker,issue_dict,"labels",10)
    if "2" not in not_show:
        L=draw_table0(L,"New_Incomplete defects : %s" %len(new_incomplete),new_incomplete,issue_dict,"Status",3)
    if len(comps) !=1:
        L=draw_table1(L,"By Components(sorted)",comps,True) 
    L=draw_table1(L,"By Priority(sorted)",pris,False) 
    if "3" not in not_show:
        L=draw_table1(L,"By Developer(sorted)",devs,True) 
    if "4" not in not_show:
        L=draw_table1(L,"By Reporters (sorted)",reps,True) 
    L += '''</table>'''
    if "5" not in not_show:
        L += "<p class='y'><strong>Details(sorted)</strong></p>"
        L += '''<table style="width:75%">'''
        #for i in jira.search_issues('filter=%s' %filter.id):
        L +='''
  <tr>
    <td width="7%%"><strong>ID</strong></td>
    <td width="5%%"><strong>Priority</strong></td>          
    <td width="5%%"><strong>Status</strong></td>          
    <td width="25%%"><strong>Summary</strong></td>          
    <td width="6%%"><strong>Component/s</strong></td>
    <td width="10%%"><strong>Developer</strong></td>
    <td width="10%%"><strong>reporter</strong></td>
    <td width="10%%"><strong>Tester</strong></td>
    <td width="8%%"><strong>Create date</strong></td>
    <td width="8%%"><strong>Fix version</strong></td>
'''
        if "WOH" in summary:
             L +='''
     <td width="8%%"><strong>WOH</strong></td>
'''
	L +="</tr>"
        for j in ids:
            d=issue_dict[j]
        #for k,d in issue_dict.items():
            L += '''
  <tr>
    <td width="7%%"><a href='https://jira.wrs.com:8443/browse/%s'>%s</a></td>
    <td width="5%%">%s</td>          
    <td width="5%%">%s</td>          
    <td width="25%%">%s</td>
    <td width="6%%">%s</td>
    <td width="10%%">%s</td>
    <td width="10%%">%s</td>
''' %(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7])
	    if "WOH" in summary:
                if d[12] >= 7:
                    L+='''    <td width="8%%"><font color="red"><b>%s</b></font></td>''' %d[8]
                else: 
                    L+='''    <td width="8%%">%s</td>''' %d[8]
	    else:
                L+='''    <td width="8%%">%s</td>''' %d[8]
	    L +='''
    <td width="8%%">%s</td>
    <td width="8%%">%s</td>
'''%(d[9],d[11])
            if d[12] >= 7 and "WOH" in summary:
                L+='''    <td width="8%%"><font color="red"><b>%s</b></font></td>''' %d[12]
            elif "WOH" in summary: 
                L+='''    <td width="8%%">%s</td>''' %d[12]
            L+="   </tr>"
#'''% (i.key,i.key,issue.fields.priority,issue.fields.components[0],issue.fields.summary,issue.fields.assignee,issue.fields.customfield_10012,create_time)

        #for j in dir(issue.fields):
        #print issue.fields.labels
        L+= '''</table>'''
    #filter.delete()
    #issue = jira.issue('SCP7-214')
   # for j in dir(issue.fields):
   #     print j,getattr(issue.fields,j)
    
    return L

requests.packages.urllib3.disable_warnings()
parser = OptionParser()

parser.add_option("-t", action="store",type="string", dest="to",help="email whom")
parser.add_option("-c", action="store",type="string", dest="configfile",help="config file")
parser.add_option("-s", action="store",type="string", dest="subject",help="email subject")
parser.add_option("-n", action="store",type="string", dest="not_show",help="-n 1,not show developer,testers,blocking, -n 2,not show details, -n 12,not show both")
(options, args) = parser.parse_args()
to = options.to
configfile = options.configfile
subject = options.subject
not_show = options.not_show
if not_show is None:
   not_show= "0"
receiver = [x+'@windriver.com' for x in to.split(" ")]
    
L = ""
total=0
jira=con_jira()
n=0
config_dic,sections=get_details(configfile)
if not subject:
    subject=config_dic["%s" %(sections[0])]['summary']
subject = "%s" %subject
#for k,v in config_dic.items():
  # print k
for k in sections:
   n=n+1
   if len(sections)==1:
       jira_test(jira,"%s" %(config_dic[k]['summary']),config_dic[k]['filter'])
   else:
       jira_test(jira,"%s. %s" %(n,config_dic[k]['summary']),config_dic[k]['filter'])
if total > 0:
    send_email(L.encode('utf-8'),receiver)
