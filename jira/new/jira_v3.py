#!/usr/bin/python
#reference http://stackoverflow.com/questions/14048948/how-can-i-use-python-finding-particular-json-value-by-key
import requests
import json
def findall(myjson, key):
    if type(myjson) == str:
        myjson = json.loads(myjson)
    if type(myjson) is dict:
        for jsonkey in myjson:
            if type(myjson[jsonkey]) in (list, dict):
                findall(myjson[jsonkey], key)
            elif jsonkey == key:
                print myjson[jsonkey]
    elif type(myjson) is list:
        for item in myjson:
            if type(item) in (list, dict):
                findall(item, key)

#findall(json.loads(a), 'P1')
class Jira(object):
    def runJqlQuery(self):
        #SEARCH_URL = "https://jira.lsstcorp.org/rest/api/2/search"
        #MAX_RESULTS = 10000 # May be limited server-side
        #return requests.get(SEARCH_URL, params={"maxResults": MAX_RESULTS, "jql": jql.format(**kwargs)}).json()
        #url = "https://jira.wrs.com:8443/rest/api/2/issue/LTAF8-620"
        url = "https://jira.wrs.com:8443/rest/api/2/project/LIN8/components"
        #url = "https://jira.wrs.com:8443/rest/api/2/search"
        r = requests.session().get(url, auth=("apiuser", "apiuser"))
        #r = requests.get(url, auth=("apiuser", "apiuser"))
        #r = requests.get(url, auth=("apiuser", "apiuser"),params={"fields":['customfield_12703','description','issuelinks']})
        #r = requests.get(url, auth=("apiuser", "apiuser"),params={"jql":'project in ("Linux 7","Linux 8","Carrier Grade Profile 7","Carrier Grade Profile 8","Secure Linux 7","LINPUL8","OVP8","SCP8","GWP8","IDP3") AND status = Integrated AND resolution not in ("Not Applicable") ORDER BY "Integrated Date" ASC,component ASC',"fields":['key','summary']})
        #print r.status_code
	print json.dumps(r.json(),indent=4)
        #print findall(r.json(), 'created')
a=Jira()
a.runJqlQuery()
