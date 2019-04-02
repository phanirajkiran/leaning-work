#!/usr/bin/env python
import commands
import json
from pprint import pprint
import json
import subprocess
import os
from datetime import datetime
from datetime import date
import time
OUTPUT_BUFSIZE = int(os.getenv('CI_OUTPUT_BUFSIZE', 4 * 1024 * 1024))  # 4 MiB


def cmd(_cmd):
    proc=subprocess.Popen(_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=OUTPUT_BUFSIZE,shell=True)
    return  proc.communicate()[0].strip()


def format_date(date_value):
    date_value= time.strptime(date_value[:19], "%Y-%m-%dT%H:%M:%S")
    date_value= time.strftime("%Y/%m/%d", date_value)
    date_value= datetime.strptime(date_value, "%Y/%m/%d")
    simple_date=date(int(date_value.strftime("%Y")),int(date_value.strftime("%m")),int(date_value.strftime("%d")))
    return simple_date

def get_today():
    today = datetime.now().strftime('%Y-%m-%d')
    today=datetime.strptime(today,'%Y-%m-%d')
    today=date(int(today.strftime("%Y")),int(today.strftime("%m")),int(today.strftime("%d")))
    return today


def get_week(start_date,today):
    left = (today-start_date).days
    return "Week%s" %(divmod(left,7)[0]+1)

userstory="US102572"
raw_data=cmd("curl  -u 'lei.yang@windriver.com:windwind001' 'https://rally1.rallydev.com/slm/webservice/v2.0/hierarchicalrequirement?query=(FormattedID%20%3D%20{})'".format(userstory))
raw_data=json.loads(raw_data)
real_addr=raw_data['QueryResult']['Results'][0]['_ref']
data=cmd("curl  -u 'lei.yang@windriver.com:windwind001' '{}'".format(real_addr))
data=json.loads(data)
pprint(data)
#get sprint: 
print data['HierarchicalRequirement']['Iteration']['_refObjectName']
iteration_api=data['HierarchicalRequirement']['Iteration']['_ref']
iteration_data=cmd("curl  -u 'lei.yang@windriver.com:windwind001' '{}'".format(iteration_api))
iteration_data=json.loads(iteration_data)
startdate,enddate = iteration_data['Iteration']['StartDate'],iteration_data['Iteration']['EndDate']
startdate=format_date(startdate)
print startdate,enddate
today=get_today()
print get_week(startdate,today)
print iteration_api
