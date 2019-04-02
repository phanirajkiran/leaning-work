#!/usr/bin/env python
# encoding: utf-8

import json
import requests
# remove this import it contains the our user name and passwd
from account_info import username, passwd

servername = 'jira-tools.qualcomm.com'
url = 'https://' + servername
urn = '/jira/rest/api/latest/issue/'


class Jira_Issue_Obj(object):
    """
    This class helps you create a object which contains all info
    for creating a jira ticket
    """

    def __init__(self, project):
        """
        In Python, instance attributes are dynamic and can be created at runtime.
        To have self.counter available from the creation of the object, put its
        initialization in a constructor:
        """
        self.project = project
        self.issuetype = "Bug"
        self.reporter = username
        self.summary = None
        self.description = None
        self.assignee = "-1"
        self.priority = "3"

    def set_assignee(self, name):
        """
         system will automatically assign a assignee if name="-1"
        """
        self.assignee = name

    def set_description(self, description):
        """
        """
        self.description = description

    def set_issuetype(self, issuetype):
        """
        """
        self.issuetype = issuetype

    def set_reporter(self, reporter):
        """
        """
        self.reporter = reporter

    def set_summary(self, summary):
        self.summary = summary

    def set_priority(self, priority):
        self.priority = priority

    def to_json_string(self):
        """
        return a json format string of the object
        """
        project = {"project": {"key": self.project}}
        summary = {"summary": self.summary}
        description = {"description": self.description}
        issuetype = {"issuetype": {"name": self.issuetype}}
        reporter = {"reporter": {"name": self.reporter}}
        assignee = {"assignee": {"name": self.assignee}}
        priority = {"priority": {"id": self.priority}}
        fields = {"fields": dict(project.items() +
                                 summary.items() +
                                 description.items() +
                                 issuetype.items() +
                                 reporter.items() +
                                 assignee.items() +
                                 priority.items())}
        return json.dumps(fields)


class Jira_Tool_Object(object):
    """A object to deal with jira API
    Need a table to map error to corresponding
    tech teams
    """

    def __init__(self, user):
        """constructor, login stuff """
        self.user = user
        # login
        self.httpClient = requests.session()

    def createJiraIssue(self, issue_object):
        """@todo: Docstring for create_jira_issue

        :issue_object: @contains info for creating a jira
        :returns: @todo

        """
        # generate json data body

        # mapping error to corresponding tech team project
        #project = {"project": {"key": "WINCRASH"}}
        #summary = {"summary": issue_object.bucket_id}
        #description = {"description": issue_object.bucket_id}
        #issuetype = {"issuetype": {"name": "Bug"}}
        #reporter = {"reporter": {"name": self.user}}
        #assignee = {"assignee": {"name": "shileiz"}}
        #fields = {"fields": dict(project.items() +
        #                        summary.items() +
        #                         description.items() +
        #                         issuetype.items() +
        #                         reporter.items() +
        #                         assignee.items())}
        # post the jira
        return self.httpClient.post(url + urn,
                                    verify=False,
                                    auth=(username, passwd),
                                    data=issue_object.to_json_string(),
                                    headers={'content-type': 'application/json'})

    def resolveJiraIssue(self, issueOrKey, comment, transitionID="5", reslution="Fixed"):
        """
         to close a jira ticket
        """
        # get the json data
        transition = {"transition": {"id": transitionID}}
        fields = {"resolution": {"name": reslution}}
        update = {"update": {"comment": [{"add": {"body": comment}}]}}

        postdata = dict(update.items() + fields.items() + transition.items())
        return self.httpClient.post(url + urn + issueOrKey + '/transitions',
                                    verify=False,
                                    auth=(username, passwd),
                                    data=json.dumps(postdata),
                                    headers={'content-type': 'application/json'})


# TEST STUB
if __name__ == "__main__":
    jira_issue = Jira_Issue_Obj("WINCRASH")
    jira_issue.set_summary("this is jira create summary")
    jira_issue.set_description("this is jira create description")
    jira_issue.set_priority("4")

    j_str = jira_issue.to_json_string()
    print j_str

    jira_obj = Jira_Tool_Object(username)

    res = jira_obj.createJiraIssue(jira_issue)
    print res.text
   # comment = "refer to CR:461128"
#    res = jira_obj.resolveJiraIssue("ARAST-45252", comment)
  #  print res.text
