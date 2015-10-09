#!/usr/bin/env python
# This script shows how to use the client in anonymous mode
# against jira.atlassian.com.

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
jira = JIRA(options,basic_auth=('lyang0', '!windwind001'))    # a username/password tuple
#jira = JIRA(options)    # a username/password tuple

# Find all issues reported by the admin
#issues = jira.search_issues('assignee=lyang0')
issue_dict = {
    #issue.fields.project.key
    'project': {'key': 'LTAF6'},
    'issuetype': {'name': 'Bug'},
    'summary': 'Ignore me:TEST TO CREATE DEFECT AUTOMATICALLY',
    'priority': {'name': 'P3'},
    'customfield_10605': {'value':'Standard'},
    'components': [{'name': 'Test Infrastructure'}],
    'description': 'TEST ERROR INFORMATION\nXXXXXXX\nYYYYYYYY',
    'customfield_11001': 'steps to reproduce yyyyyyyyyyyyyyyyyyyyyy',
    'reporter': {'name': 'lyang0'},
    'customfield_11000': [{'name': '6.0'}],
    'customfield_11201': 'US66524',
}
new_issue = jira.create_issue(fields=issue_dict)
print new_issue

