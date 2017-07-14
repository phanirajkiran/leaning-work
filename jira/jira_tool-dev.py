#!/usr/bin/env python
import json
import requests
import getpass
import optparse
from optparse import OptionParser
import os 
import re
import smtplib
from smtplib import SMTPException
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import getpass
import urllib2
import textwrap
import platform

servername = 'jira.wrs.com:8443'
url = 'https://' + servername
url_issue = '/rest/api/2/issue/'
url_components = '/rest/api/2/project/LIN9/components'

class BetterFormatter(optparse.IndentedHelpFormatter):
    def __init__(self, *args, **kwargs):
        optparse.IndentedHelpFormatter.__init__(self, *args, **kwargs)
        self.wrapper = textwrap.TextWrapper(width=self.width)
    def _formatter(self, text):
        return '\n'.join(['\n'.join(p) for p in map(self.wrapper.wrap,
        self.parser.expand_prog_name(text).split('\n'))])

    def format_description(self, description):
        if description:
            return self._formatter(description) + '\n'
        else:
            return ''

    def format_epilog(self, epilog):
        if epilog:
            return '\n' + self._formatter(epilog) + '\n'
        else:
            return ''

    def format_usage(self, usage):
        return self._formatter(optparse._("Usage: %s\n") % usage)

    def format_option(self, option):
        # Ripped and modified from Python 2.6's optparse's HelpFormatter
        result = []
        opts = self.option_strings[option]
        opt_width = self.help_position - self.current_indent - 2
        if len(opts) > opt_width:
            opts = "%*s%s\n" % (self.current_indent, "", opts)
            indent_first = self.help_position
        else:                       # start help on same line as opts
            opts = "%*s%-*s  " % (self.current_indent, "", opt_width, opts)
            indent_first = 0
        result.append(opts)
        if option.help:
            help_text = self.expand_default(option)
            # Added expand program name
            help_text = self.parser.expand_prog_name(help_text)
            # Modified the generation of help_line
            help_lines = []
            wrapper = textwrap.TextWrapper(width=self.help_width)
            for p in map(wrapper.wrap, help_text.split('\n')):
                if p:
                    help_lines.extend(p)
                else:
                    help_lines.append('')
           # End of modification
            result.append("%*s%s\n" % (indent_first, "", help_lines[0]))
            result.extend(["%*s%s\n" % (self.help_position, "", line)
                     for line in help_lines[1:]])
        elif opts[-1] != "\n":
            result.append("\n")
        return "".join(result)

class Jira_Issue(object):
    """
    This class helps you create a object which contains all info
    for creating a jira ticket
    """

    def __init__(self,arg):
        """
        In Python, instance attributes are dynamic and can be created at runtime.
        To have self.counter available from the creation of the object, put its
        initialization in a constructor:
        """
	self.issue_obj=arg

    def to_json_string(self):
        """
        returl_issue a json format string of the object
        """
        fields = {"fields": self.issue_obj}
        return json.dumps(fields)

class jiraInit(object):
    """A object to deal with jira API
    Need a table to map error to corresponding
    tech teams
    """

    def __init__(self):
        self.httpClient = requests.session()

class jiraShowComponents(jiraInit):

    def show_components(self):
	r=self.httpClient.get(url+url_components, auth=("apiuser", "apiuser"))
	return [ x['name'] for x in r.json()]

    def __call__(self):
	return self.show_components()

class jiraAction(jiraInit):
    """A object to deal with jira API
    Need a table to map error to corresponding
    tech teams
    """
    def createJiraIssue(self,issue_object):
        """@todo: Docstring for create_jira_issue
        :issue_object: @contains info for creating a jira
        """
        return self.httpClient.post(url + url_issue,
                                    verify=False,
                                    auth=('apiuser', 'apiuser'),
                                    data=issue_object.to_json_string(),
                                    headers={'content-type': 'application/json'})



class createEmail(object):
    @staticmethod
    def email(review_obj):
        L = '''
  o Peer Reviewer:
    {reviewer}
  o Check the CQ, Is there a duplicate?
    (No)

 1. Priority
****************************
{priority}


 2. Severity
****************************
N/A


 3. Repeatability :
****************************
reproducible


 4. Summary:
****************************



 5. Faulty Part:
****************************
{domain}


 6. Engineering Details (Not Published):
****************************

Environment
======================
Requirement No.: {userstory}
Peer Reviewer: {reviewer} 
WRLinux Kernel Version: 4.8.x
Binary/FS From: WRL9_GIT
BSP/Configuration: NA
HOST OS: {hostos}

Log location
======================
NA


 7. Symptom Details
****************************

Problem Description
======================
{problem}

Expected Behavior
======================
no problem shown

Observed Behavior
======================
please check section "Problem Description"

Logs
======================
{details}

Misc Info
======================


 8. Steps To Reproduce
****************************
{test_step}

 9. Workaround
****************************
N/A


 10. Failure Scenarios Checking
****************************
(1) Is this defect found by the existing test cases?
Yes
''' .format(**review_obj.defect)
	return L

class argParser(optparse.OptionParser):

    usage='''
       #Send BUG review to lei.yang and CDC-ENG-Linux-core-test for US66411
       %s -l testcase.log -u US66411 -r lei.yang -t 
    
       #Create P2 BSP defect and assign it to lyang0,assoicate to US66411
       %s -l testcase.log -u US66411 -a lyang0 -c BSP -p P2 -j''' %(__file__,__file__)

    def __call__(self):
	request_obj=jiraShowComponents()
        components='\n'.join(request_obj())
        parser = OptionParser(formatter=BetterFormatter(),usage=argParser.usage)
        parser.add_option("-l", "--log",  \
                         action="store", type="string", dest="log",help="test case log")
        parser.add_option("-s", "--subject",  \
                         action="store", type="string", dest="subject",help="defect subject")
        parser.add_option("-r", "--reviewer",  \
                         action="store", type="string", dest="reviewer",help="defect reviewer")
        parser.add_option("-t", action="store_true", dest="team",help="send to team")
        parser.add_option("-u", "--userstory",  \
                         action="store", type="string", dest="userstory",help="associate userstory")
        parser.add_option("-j", action="store_true", dest="jira",help="Jira: create defect")
        parser.add_option("-c", "--component",  \
                         action="store", type="string", dest="component",help="Jira: component (Default:BSP): \
			 %s"%components)
        parser.add_option("-a", "--assignee",  \
                         action="store", type="string", dest="assignee",help="Jira: Defect assignee(Defalut None)")
        parser.add_option("-p", "--priority",  \
                         action="store", type="string", dest="priority",help="Jira: Defect Priority(Default P2)")
        (options, args) = parser.parse_args()
	return options
  

class analysisDefect(object):

    def __init__(self,url):
	self.txt=None
	if os.path.exists(url):
	    with open(url) as f:
		self.txt=f.read()
	else:
	    self.txt = urllib2.urlopen(url).read()
	defect_sections={}
	try:
	    test_name=re.findall(r'Start testcase (.*?) testing',self.txt)[0]
	except:
	    test_name=None
	try:
	    problem=re.findall(r'test results:(.*?)Excution Time',self.txt,re.DOTALL)[0]
	except:
	    problem=None
	try:
	    test_step=re.findall(r'Testing Env(.*?)Extra Info',self.txt,re.DOTALL)[0]	
	except:
	    test_step=None
	try:
	    details=re.findall(r'Start testcase(.*?)End testcase',self.txt,re.DOTALL)[0]	
	except:
	    details=None
	defect_sections['testcase']=test_name	
	defect_sections['problem']=problem	
	defect_sections['test_step']=test_step	
	defect_sections['details']=details	
	self.defect_sections=defect_sections
		 
class baseDefect(object):
    def __init__(self):
        self.options=argParser()()
	obj_analysisDefect=analysisDefect(self.options.log)
	self.analysis_defect=obj_analysisDefect.defect_sections

    def __getattr__(self, name):
        return getattr(self.options, name)

class jiraData(baseDefect): 

    issue_obj={}
    issue_obj['project']={"key":"LIN9"}
    issue_obj['issuetype']={'name': 'Bug'}
    issue_obj['customfield_11000']=[{'name':'9.0'}]

    def __init__(self):
	super(jiraData,self).__init__()
	if self.component:
            self.issue_obj['components']=[{'name': self.component}]
	else:
            self.issue_obj['components']=[{'name': 'BSP'}]
        self.issue_obj['reporter']={'name': getpass.getuser()}
        self.issue_obj['assignee']={'name':self.assignee}
	if not self.priority:
            self.issue_obj['priority']={'name':self.priority}
	else:
            self.issue_obj['priority']={'name':'P2'}
        self.issue_obj['customfield_11201']=self.userstory
	if not self.subject:
            self.issue_obj['summary']="Test case %s failed " %self.analysis_defect['testcase']
	else:
            self.issue_obj['summary']=self.subject
        self.issue_obj['description']=self.analysis_defect['details']
        self.issue_obj['customfield_11001']=self.analysis_defect['test_step']
        self.issue_obj['customfield_12801']={"value": "Reproducible"}

class reviewData(baseDefect):
    def __init__(self):
	super(reviewData,self).__init__()
        self.defect={}
	self.defect['subject']=self.subject
	self.defect['reviewer']=self.reviewer
	self.defect['priority']=self.priority
	self.defect['userstory']=self.userstory
	self.defect['problem']=self.analysis_defect['problem']
	self.defect['details']=self.analysis_defect['details'] 
	self.defect['test_step']=self.analysis_defect['test_step']
	self.defect['testcase']=self.analysis_defect['testcase']
	self.defect['hostos']=" ".join(platform.linux_distribution())
	self.defect['domain']=self.component

	
	
class sendDefectReview(object):
    def __init__(self,content,review_obj):
	reviewer=review_obj.defect['reviewer']
	testcase=review_obj.defect['testcase']
	sender = "%s@windriver.com" %getpass.getuser()
	reviewer = ['lei.yang@windriver.com','%s@windriver.com' %reviewer]
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ", ".join(reviewer)
	if not review_obj.defect['subject']:
            msg['Subject'] = "[Bug Review] %s failed" %testcase
	else:
            msg['Subject'] = review_obj.defect['subject']
        #body = "%s" %(file.read())
        msg.attach(MIMEText(content, 'plain'))
        text = msg.as_string()
        try:
           smtpObj = smtplib.SMTP('147.11.189.50','25')
           smtpObj.sendmail(sender,reviewer, text)
           print "Successfully sent email"
        except SMTPException:
           print "Error: unable to send email"

if __name__ == '__main__':
    base_obj=baseDefect()
    if not base_obj.jira:
        review_obj=reviewData()
	email=createEmail().email(review_obj)
        sendDefectReview(email,review_obj)
    if base_obj.jira:
        defect_obj=jiraData().issue_obj    
        issue_obj=Jira_Issue(defect_obj)
        jiraAction().createJiraIssue(issue_obj)
