#!/usr/bin/python -B
import sys
import os
from optparse import OptionParser
import ConfigParser
from os.path import expanduser
from string import digits
import collections
from collections import OrderedDict
import subprocess
import smtplib
from smtplib import SMTPException
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time

#https://www.w3schools.com/html/tryit.asp?filename=tryhtml_table_collapse

def run_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    return proc_stdout

style='''
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 5px;
  font-size: 9pt;
}
th {
  text-align: left;
}
</style>
<u><strong>defect resolved</strong></u>
<br>
<br>
'''


class jira_2_html(object):

    #key='<a href="https://jira.wrs.com/browse/{}">{}</a>'.format(i['key'],i['key'])
    @classmethod
    def bug_table(cls,defect_list):
    
        _table=""
        def gen_table(d):
            _s='''
      <tr>
        <td><a href="https://jira.wrs.com/browse/{key}">{key}</a></td>
        <td>{priority}</td>
        <td>{summary}</td>
        <td>{component}</td>
        <td>{assignee}</td>
        <td>{resolution}</td>
        <td>{resolutiondate}</td>
      </tr>
    '''.format(**d)
    	    return _s
    

	print defect_list
	l=sorted(defect_list,key=lambda k:k['priority'],reverse=False)
	for i in l:
            _x=gen_table(i)
    	    _table+=_x
    
        table='''
    <table style="width:100%">
      <tr>
        <th>key</th>
        <th>priority</th> 
        <th>summary</th>
        <th>component</th>
        <th>assignee</th>
        <th>resolution</th>
        <th>resolutiondate</th>
      </tr>
    {}
    </table>
'''.format(_table)
        return style+table
    
    

class Jira(object):

    @classmethod
    def gen_filter_list(cls,s):
   	'''
	struct:
	[{'key': u'LIN1019-790', 'resolutiondate': u'2019-03-07T16:57:21.000-0800', 'summary': u'systemd_241.bb:do_compile() failed: git/src/basic/build.h:4:10: fatal error: version.h: No such file or directory', 'priority': u'P1', 'assignee': u'JKang', 'components': u'Userspace', 'resolution': {u'self': u'https://jira.wrs.com/rest/api/2/resolution/3', u'id': u'3', u'name': u'Duplicate', u'description': u'The problem is a duplicate of an existing issue.'}}]
	''' 
        import json
	#form collections import defaultdict
	#defect_dict=defaultdict(list)
	l=[]
        _d = json.loads(s)
	d=_d['issues']
	
	k=[
	   "key",
	   "priority",
	   "summary",
	   "component",
	   "assignee",
	   "resolution",
	   "resolutiondate"
	   ]
	def time_format(t,t_format):
	    ts = time.strptime(t,t_format)
	    return time.strftime("%Y-%m-%d", ts)
        for i in d:
	    defect_dict={}
	    key=i['key']
	    f=i['fields']
            priority=f['priority']['name']
            summary=f['summary']
            component=f['components'][0]['name']
            assignee=f['assignee']['name']
            resolution=f['resolution']['name']
            resolutiondate=time_format(f['resolutiondate'],"%Y-%m-%dT%H:%M:%S.000-0800")
	    for x in k:
	        defect_dict[x]=locals()[x]
	    l.append(defect_dict)
        return l

cmd='''curl -u apiuser:apiuser -X GET -H "Content-Type: application/json" "https://jira.wrs.com/rest/api/2/search?jql=resolutiondate%20>%20-7d%20and%20project%20%3D%20'Linux%2010.19'&fields=id,key,priority,assignee,reporter,resolution,components,summary,resolutiondate"'''
out=run_cmd(cmd)
defect_list=Jira.gen_filter_list(out)
x=jira_2_html.bug_table(defect_list)
print x
#defect_dict={u'LIN1019-243': [u'LIN1019-243', u'P3', u'Security Advisory - libsndfile1 - CVE-2018-19432', u'Userspace', u'ytao']}

