#!/usr/bin/python
import re,urllib
import xmlrpclib
from pprint import pprint
import json


def get_jobs_link(filters):
    links = [ a['test_runs'][0]['link'] for a in filters ]
    return links 

def get_job_id(link):
    data = urllib.urlopen(link).read()
    m = re.search('<dd><a href="/scheduler/job/(.*)"',data)
    return m.group(1)

def get_job_lists(links):
    job_lists= [ get_job_id(link) for link in links] 
    return job_lists

def get_bundle_sha1(job_id):
    return server.scheduler.job_status(job_id)['bundle_sha1']

server = xmlrpclib.ServerProxy("http://lyang0:3pprjnzwf8aepbwy8mnizyeok02t8cxkxx1dwfa7ui861xzucpgjlm5jdrkbi17n98lueq2ci634wqybei0kgoa8fj1to0wsugoh0xqiasm7y7wdf0y51h0zbbyq7038@yow-lpd-lava1.wrs.com/RPC2")
filters1=server.dashboard.get_filter_results('~lyang0/all',200)
#filters2=server.dashboard.get_filter_results('~lyang0/all_weekday',200)
links1=get_jobs_link(filters1)
job_lists1=get_job_lists(links1)
#links2=get_jobs_link(filters2)
#job_lists2=get_job_lists(links2)
job_lists=job_lists1+['15102','15209.0']
print job_lists
for x in job_lists:
   print x
#print job_lists
#print json.dumps(y,indent=4)
#for i in y['test_runs']:
#@    if i['test_id'] == "inter-node-migrate-benchmark-on-host-A":
#        for j in i['test_results']:
#            print j
x=get_bundle_sha1('15193.0')
y=json.loads(server.dashboard.get(x)['content'])
#print json.dumps(y,indent=4)
def get_benchmark_results(job_id):
    x=get_bundle_sha1(job_id)
    y=json.loads(server.dashboard.get(x)['content'])
    L=""
    for i in y['test_runs']:
        for j in i['test_results']:
            if j.has_key('measurement'):
                L+="    %s: %s \n" %(j['test_case_id'],j['measurement'])
    return L
#definition = json.loads(server.scheduler.job_details('15193.0')['definition'])
#print server.scheduler.job_details('15193.0')['_actual_device_cache']['hostname']
#print definition['job_name']
#for i,k in server.scheduler.job_details('15193.0').items():
#    print i
def print_benchmark(job_id):
    results=get_benchmark_results(job_id)
    if results:
	definition = json.loads(server.scheduler.job_details(job_id)['definition'])
	target= server.scheduler.job_details(job_id)['_actual_device_cache']['hostname']
        print definition['job_name'],"on",target
	print results 	
for i in job_lists:
    print_benchmark(i)
