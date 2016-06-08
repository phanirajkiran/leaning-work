#!/usr/bin/env python

#################################################################################################
#
#  rallly_utils.py - A script to connect to a Rally server
#              and obtain basic workspace and project information
#
#################################################################################################

import sys
sys.path.append("/folk/lyang0/rally/lib")
from optparse import OptionParser
from pyral import Rally, rallyWorkset
import pprint
import time
from datetime import datetime
import smtplib
from smtplib import SMTPException
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import commands
import os
from datetime import datetime
import getpass
import requests
from datetime import date


#################################################################################################

errout = sys.stderr.write

#################################################################################################


def auto_create_all_task(rally,userstory,owner):
    #criterion=['FormattedID = %s' % userstory, 'User.ref.DisplayName = "Chunguang Yang"']
    criterion='FormattedID = %s' % userstory
#    criterion='FormattedID = TA113895'
    response   = rally.get('UserStory', query=criterion,fetch="Name,FormattedID,Tasks")
   # response   = rally.get('Task', query=criterion)
    #story1 = response.next()
#    print story1.details()
    task_list=[]
    count = 0 
    for story in response:
        for task in story.Tasks:
#            print task.oid, task.Name
#            print dir(task)
#            print task.Owner.Name
#            print task.Name
            if ('LIN8' not in task.Name) and ('[TEST]' not in task.Name):
		name=commands.getoutput('echo %s |sed "s/\[DEV\]//g"' %task.Name)
                task_list.append(name)
                count = count + 1 
#    print task_list
    for task in task_list:
        create_task(userstory,task,owner)
    print "%s the testing tasks for %s are created" %(count,owner)
    sys.exit(0)


def create_task(userstory,task_name,task_owner):
    create_task.counter += 1 
    criterion='FormattedID = %s' % userstory
    target_story   = rally.get('UserStory', query=criterion, instance=True)
    task_owner = rally.getUserInfo(name=task_owner).pop(0)
    info = {
             "Project"     : rally.getProject().ref,
             "WorkProduct" : target_story.ref,
              'Owner'      : task_owner.ref,
             "Name"        : '[TEST] %s' %task_name,
             "State"       : "In-Progress",
             "TaskIndex"   : create_task.counter,
             #"Description" : "Fly to Chile next week to investigate the home of potatoes.  Find the absolute gigantoidist spuds and bring home the eyes to Idaho.  Plant, water, wonder, harvest, wash, slice, plunge in and out of hot oil, drain and enjoy! Repeat as needed.",
             "Estimate"    : 2.0,
             "Actuals"     :  2.0,
             "ToDo"        : 2.0,
             #"Notes"       : "I have really only done some daydreaming wrt this task.  Sorry Jane, I knew you had big plans for Frankie's blowout BBQ next month, but the honeycomb harvest project is taking all my time."
           }

    task = rally.put('Task', info)
    #print "Created  Task: %s   OID: %s" % (task.FormattedID, task.oid)
    print "Created Task: %s [TEST] %s" % (task.FormattedID,task_name)

def list_userstory(rally):
    response = rally.get('UserStory', query=iteration_criterion,fetch="Name,FormattedID")
    for story in response:
        print '    %s: %s' %(story.FormattedID,story.Name)
    sys.exit(0)

def get_task_info(rally):
    response = rally.get('UserStory', query=iteration_criterion,fetch="Name,FormattedID,Tasks,JiraLink,Blocked,Project,ObjectID")
    #response = rally.get('UserStory', query=iteration_criterion)
    task_dict={}
    block_defect={}
    for story in response:
        task_dict[story.FormattedID]={}
        block_defect['%s %s' %(story.FormattedID,story.Name)]=[]
        for task in story.Tasks:
            if task.Owner and task.Owner.Name:
                task_dict[story.FormattedID][task.FormattedID]=[]
        for task in story.Tasks:
            if task.Owner and task.Owner.Name:
                task_dict[story.FormattedID][task.FormattedID].append(story.Name)
                task_dict[story.FormattedID][task.FormattedID].append(task.Owner.Name)
                task_dict[story.FormattedID][task.FormattedID].append(task.Name)
                task_dict[story.FormattedID][task.FormattedID].append(task.State)
                task_dict[story.FormattedID][task.FormattedID].append(task.Blocked) #4
                task_dict[story.FormattedID][task.FormattedID].append(task.BlockedReason)
                task_dict[story.FormattedID][task.FormattedID].append(task.ToDo)
                task_dict[story.FormattedID][task.FormattedID].append(story.Project.oid) #7
                task_dict[story.FormattedID][task.FormattedID].append(story.ObjectID) #8
                task_dict[story.FormattedID][task.FormattedID].append(task.ObjectID) #9
            if task.Blocked and task.BlockedReason:
                block_defect['%s %s' %(story.FormattedID,story.Name)].append(task.BlockedReason)
            if task.Blocked and task.JiraID:
                block_defect['%s %s' %(story.FormattedID,story.Name)].append(task.JiraID)
            if story.Blocked and story.JiraLink:
                block_defect['%s %s' %(story.FormattedID,story.Name)].append(story.JiraLink)
    return task_dict,block_defect

def list_my_userstory(rally,owner,task_dict):
    n = 0
    sum_todo = 0
    string = ""
    for a,b in task_dict.items():
        task_flag = False
        z = 0
        userstory_todo = 0
        #task_dict['%s: %s' %(story.FormattedID,story.Name)] = []
        #print story.Blocked,story.JiraLink
        for c,d in b.items():
            #print story.Name,owner,task.Owner.Name
            #if task.Owner and owner == task.Owner.Name:
            if owner == d[1]:
                #print task.Owner.Name
                task_flag = True
                z = z+1
                if z == 1:
                    n = n+1
                    #print "%s.%s %s" %(n,story.FormattedID,story.Name)
                    #if not story.Blocked:
                    #string += "%s.%s %s\n" %(n,story.FormattedID,story.Name)
                    string += '''<p class='y'>&nbsp&nbsp&nbsp&nbsp%s.<a href="https://rally1.rallydev.com/#/%s/detail/userstory/%s">%s</a> %s</p>''' %(n,d[7],d[8],a,d[0])
                    string += '''<table style="width:65%">'''
                #task_dict['%s: %s' %(story.FormattedID,story.Name)].append('    %s: %s' %(task.FormattedID,task.Name))
                #print '    %s: %s(%s) todo:%s' %(task.FormattedID,task.Name,task.State,task.ToDo)
                #if not task.ToDo:
                if not d[6]:
                    #task.ToDo=0.0
                    d[6]=0.0
                sum_todo = d[6] + sum_todo
                userstory_todo = d[6] + userstory_todo
                #print("    %-6s:%-39s(%-5s) Todo:%-5s" % (task.FormattedID,task.Name,task.State,task.ToDo))
                if d[6] != 0:
                    #if not task.Blocked:
                    if not d[4]:
                        #string += "    %-6s:%-39s(%-5s) Todo:%-5s\n" % (task.FormattedID,task.Name,task.State,task.ToDo)
                        #string += "<p class='y'>&nbsp&nbsp&nbsp&nbsp%-6s:%-39s(%-5s) Todo:%-5s<br></p>" % (c,d[2],d[3],d[6])
                        string += '''
  <tr>
    <td width="80%%">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&#10004&nbsp<a href="https://rally1.rallydev.com/#/%s/detail/task/%s">%s</a>:%s</td>
    <td width="30%%">%s</td>          
    <td width="30%%">%s</td>
  </tr>
'''% (d[7],d[9],c,d[2],d[3],d[6])
                    else:
                        #string += "    %-6s:%-39s(%-5s) Todo:%-5s *Blocked By* https://jira.wrs.com:8443/browse/%-50s \n" % (task.FormattedID,task.Name,task.State,task.ToDo,task.BlockedReason)
                        #string += "<p class='y'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%-6s:%-39s(%-5s) Todo:%-5s *Blocked By* https://jira.wrs.com:8443/browse/%-50s</p>" % (c,d[2],d[3],d[6],d[5])
                        string += '''<p class='y'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&#10004&nbsp<a href="https://rally1.rallydev.com/#/%s/detail/task/%s">%s</a>:%-39s(%-5s) Todo:%-5s <strong>Blocked By</strong> <a href="https://jira.wrs.com:8443/browse/%s">%s</a></p>''' % (d[7],d[9],c,d[2],d[3],d[6],d[5],d[5])
        #print userstory_todo,task_flag,story.Name,owner,"xxx"
        string += '''</table>'''
        if (userstory_todo == 0 or userstory_todo == 0.0) and (task_flag):
            #string += "    *All the task for %s in %s complete*\n" %(owner,story.FormattedID)
            string += "<p class='y'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<i><strong><font color='green'>All the task for %s in %s complete</font></strong></i></p>" %(owner,a)
    return int(sum_todo),string
'''
    n = 0
    for k,v in task_dict.iteritems():
        if v:
            n = n + 1 
            print "%s.%s" %(n,k)
            for z in v:
                print z     
'''
def list_tasks(rally,userstory):
    response   = rally.get('UserStory', query='FormattedID = %s' % userstory,fetch="Name,FormattedID,Tasks")
   # story1 = response.next()
   # print story1.details()
    task_list=[]
    for story in response:
        print '%s: %s' %(story.FormattedID,story.Name)
        for task in story.Tasks:
#            print task.oid, task.Name
  #           print task.Owner.Name
    #         print '         %s:%s(%s)' %(task.FormattedID,task.Name,task.State)
            if task.Owner:
                print("    %-6s:%-49s(%-5s) Todo:%-8s %-50s" % (task.FormattedID,task.Name,task.State,task.ToDo,task.Owner.Name))
    sys.exit(0)
 

def list_features(rally,release):
    print release
    response = rally.get('Feature',query='Release.Name = "%s"' %release,fetch="Name,FormattedID,UserStories,Owner")
    for feature in response:
        print '%s: %s' %(feature.FormattedID,feature.Name)
        for userstory in feature.UserStories:
	    #print type(userstory.Owner)
            #print dir(userstory.Owner)
	    #print userstory.Owner
	    owner=getattr(userstory.Owner,"Name","None")
            print("       %-6s:%-19s (%s)" % (userstory.FormattedID,userstory.Name,owner))


def update_task(userstory,task_name,task_owner):
    taskID = args.pop()   # for this example use the FormattedID
    print "attempting to update Task: %s" % taskID

    #
    # following assumes there is:
    #     a User in the system whose DisplayName is 'Crandall',
    #     a UserStory with a FormattedID of S12345, 
    #     a Release with a name of 'April-A', 
    #    an Iteration with a Name of 'Ivanhoe' 
    # within the current Workspace and Project.
    #
    owner_name = task_owner
    storyID    = userstory
  #  release_target   = 'April-A'
  #  iteration_target = 'Ivanhoe'

    target_workspace = rally.getWorkspace()
    target_project   = rally.getProject()
    target_owner = rally.getUserInfo(name=owner_name).pop(0) # assume a unique match...

    release      = rally.get('Release',   query='Name = %s' % release_target,   instance=True)
    iteration    = rally.get('Iteration', query='Name = %s' % iteration_target, instance=True)
    print dir(iteration)
    target_story = rally.get('UserStory', query='FormattedID = %s' % storyID,   instance=True)

    info = {
             "Workspace"     : target_workspace.ref,
             "Project"       : target_project.ref,
             "FormattedID"   : taskID,
             "Name"          : "Stamp logo watermark on all chapter header images",
             "Owner"         : target_owner.ref,
   #          "Release"       : release.ref,
   #         "Iteration"     : iteration.ref,
             "WorkProduct"   : target_story.ref,
             "State"         : "In-Progress",
             "Rank"          : 2,
             "TaskIndex"     : 2,
             "Estimate"      : 2,
             #"Actuals"       : 2.5,
             "ToDo"          : 2,
   #          "Notes"         : "Bypass any GIFs, they are past end of life date",
   #          "Blocked"       : "false"
           }

##    print info   

    try:
        task = rally.update('Task', info)
    except RallyRESTAPIError, details:
        sys.stderr.write('ERROR: %s \n' % details)
        sys.exit(2)

def con_rally(server, user, password, workspace, project):
    rally= None
    try:
        rally = Rally(server, user, password, workspace=workspace, project=project)
    except:
        time.sleep(1)
        rally=con_rally(server, user, password, workspace=workspace, project=project)
    finally:
        return rally

def current_iteration(rally):
    today = datetime.now().strftime('%Y-%m-%d')
    #query = ['StartDate <= "{}"'.format(today),
    #         'EndDate >= "{}"'.format(today)]
    query = ['StartDate <= today',
             'EndDate >= today']
    #iterations = rally.get('Iteration', query=query,fetch="Name")
    iterations = rally.get('Iteration', query=query)
    i=next(iterations)
    interation_name=i.Name 
    interation_end=i.EndDate
    return interation_name,interation_end,today
    #return next(iterations).Name,next(iterations).EndDate,today

def get_each_status(domain,rally,names):
    #text_mail='/tmp/xxx_%s' %domain
    #if os.path.exists(text_mail):
    #    os.remove(text_mail)
    #txt=open(text_mail, "a")
    mail = ""
    #print iteration_criterion
    response1 = rally.get('Task', query=iteration_criterion,fetch="Owner,Project,Name")
    #response1 = rally.get('Task', query=iteration_criterion)
    #print response1.next().details()
    owners = []
    for j in response1:
        if j.Owner and j.Name: 
            owners.append(j.Owner.Name)
    owners=list(set(owners))
    #print owners
    if not names:
        name=owners
        #name=['Lei Yang','Liang Chi','Xiangyu Dong','Wei Gao','Zumeng Chen','Lu Jiang','Quanyang Wang','Yanjiang Jin','Pengyu Ma','Chunguang Yang','Liwei Song']
        #name=['Lei Yang','Liang Chi','Xiangyu Dong','Wei Gao','Ting Wang','Hongjun Yang','Boyang Xue','Chi Xu','Hong Chen','Le Liu','Jian Kang','Peng Yan','Tingting Wen','Wanling Wu','Yongmin Cheng']
        #name=['Lei Yang','Liang Chi','Xiangyu Dong','Wei Gao','Ting Wang','Hongjun Yang','Boyang Xue','Chi Xu','Hong Chen','Le Liu','Jian Kang','Peng Yan','Tingting Wen','Wanling Wu','Yongmin Cheng','Zumeng Chen','Lu Jiang','Quanyang Wang','Yanjiang Jin','Pengyu Ma','Chunguang Yang','Liwei Song']
    else:
        name = [x for x in names.split(",")]
    #print owners
    task_dict,blocked_defect=get_task_info(rally)
    owner_todo=[]
    for x in name:
    #    ret,results = commands.getstatusoutput("/home/lyang001/leaning-work/rally/rally_utils.py -o '%s'" %x)
        if x in owners:
            owner=x
            ret,results=list_my_userstory(rally,owner,task_dict)
            owner_todo.append((x,ret))
        #txt.write("*%s* 's Task (*Total todo* = %s hours)\n" %(x,ret >> 8))
            if ret != 0:
                title = "<p class='x'><u><strong>%s</strong> 's Task (Total todo = <strong>%s hours</strong>)</u></p>" %(x,ret)
                #title = "<u><strong>%s</strong> 's Task (Total todo = <strong>%s hours</strong>)</u>" %(x,ret)
                #lines = '''<hr noshade size=4 width="25%" align=left>'''
                mail += title
                #mail += lines 
                mail += results 
            #txtt='<font color="red"><b>' + "BLA BLA BLA" + "</b></font>"
            #txt.write(txtt)
    #if not send:
    #    print mail 
    L = '''
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
font-family: sans-serif;
font-size: 12px;
}
u {
    text-bottom: 2px solid black;
  }
</style>
<html>
<body>
'''
    L += "<p class='x'><u><strong>Scrum Master</strong> : %s</u></p>" %scrum_master
    #end_date=datetime.strptime(end_date,"%Y-%m-%dT%H:%M:%S.000Z")
    global end_date,today
    end_date = time.strptime(end_date[:19], "%Y-%m-%dT%H:%M:%S")
    end_date = time.strftime("%Y/%m/%d", end_date)
    end_date = datetime.strptime(end_date, "%Y/%m/%d")
    d0=date(int(end_date.strftime("%Y")),int(end_date.strftime("%m")),int(end_date.strftime("%d")))
    d1=date(int(today.split('-')[0]),int(today.split('-')[1]),int(today.split('-')[2]))
    left = (d0-d1).days
    if left <= 9:
        L +="<strong><font color='red'><strong></strong> Only <font size='7' color='blue'> <mark>%s</mark> </font>  days left for this sprint<strong>!!!</strong></font></strong>" %left
    #L += '''<hr noshade size=4 width="20%" align=left>'''
    L +="<br>"
    keyword_flag=0
    s=0
    for x,y in blocked_defect.items():
        if x and y:
            keyword_flag = keyword_flag+1
            if keyword_flag == 1:
                L += "<p class='x'><u><strong>Block issue</strong> in %s</u></p>" %domain
                #L += '''<hr noshade size=4 width="20%" align=left>'''
            s = s+1
            L += "<p class='x'>&#10148&nbsp%s <strong><font font size='3' color='red'>some task blocked by</font></strong> <br></p>" %(x)
            #L += "    *blocked by* :\n"
            c = 0
            for z in list(set(y)):
                c = c+1
                #L += "<p class='y'> &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%s.https://jira.wrs.com:8443/browse/%s<br></p>" %(c,z)
                L += '''<p class='y'> &nbsp&nbsp&nbsp&nbsp&nbsp&#10004&nbsp<a href="https://jira.wrs.com:8443/browse/%s">%s</a></p>''' %(z,z)
    else:
        if keyword_flag == 0:
            L += "<p class='x'><u><strong><font color='green'>NO block issue found in %s</font></strong></u></p>" %domain
            #L += '''<hr noshade size=4 width="20%" align=left>'''
    #L +="<br>"
    L += "<p class='x'><u><strong>Task to-do hours left</strong> (sorted):</u></p>"
    #L += '''<hr noshade size=4 width="20%" align=left>'''
    owner_todo=sorted(owner_todo, key=lambda x:x[1],reverse=True)
    L += '''<table style="width:15%">'''
    for i in xrange(len(owner_todo)):
        L += '''
  <tr>
    <td>&nbsp&nbsp&nbsp&nbsp%s</td>
    <td>:</td>          
    <td>%s</td>
  </tr>
'''%(owner_todo[i][0],owner_todo[i][1])
        #L += "&nbsp&nbsp&nbsp&nbsp%-16s : %-5s<br>" %(owner_todo[i][0],owner_todo[i][1])
    L +="</table>"
    L += "<br>"
    mail = L + mail
    mail = mail + "</font></p></body></html>"
    return mail 


def send_email(names,domain,send):
    #sender = "%s@windriver.com" %getpass.getuser() 
    sender = "lei.yang@windriver.com"
    if owner or (not send):
        #receiver = ["CDC-ENG-Linux-core-test@windriver.com"]
        #receiver = ["%s@windriver.com" %getpass.getuser()]
        receiver = [ "%s@windriver.com" %getpass.getuser() ]
    if send:
        #receiver = ["%s@windriver.com" %getpass.getuser()]
        #receiver = ["lpd-eng-bsp@windriver.com","wei.gao@windriver.com","xiangyu.dong@windriver.com","liang.chi@windriver.com","bo.liu@windriver.com","Zhenfeng.Zhao@windriver.com","CDC-ENG-Linux-core-test@windriver.com"]
        #receiver = ["CDC-ENG-Linux-core-test@windriver.com"]
        receiver = [x+'@windriver.com' for x in send.split(" ")]
        receiver = list(set(receiver))
        #receiver = ["lei.yang@windriver.com"]
    cc= ["lei.yang@windriver.com"]
    if not owner:
        subject = "%s : Rally Task Status in %s" %(domain,sprint)
    else:
        subject = "%s : %s Rally Task Status in %s" %(domain,owner,sprint)
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(receiver)
    msg['Cc'] = ", ".join(cc)
    msg['Subject'] = subject
    mail=get_each_status(domain,rally,names)    
    #file = open(text_mail, 'r')
    #body = "%s" %(file.read())
    #file.close()
    #txtt='<font color="red"><b>' + "BLA BLA BLA" + "</b></font>"
    msg.attach(MIMEText(mail, 'html'))
    #msg.attach(MIMEText(txtt, 'html'))
    text = msg.as_string()
    mail_addr=" "
    for z in receiver:
        mail_addr += "%s " %z
    try:
       smtpObj = smtplib.SMTP('147.11.189.50','25')
       smtpObj.sendmail(sender,list(set(receiver+cc)), text)
       print "Successfully sent email to%s" %mail_addr
    except SMTPException:
       print "Error: unable to send email"
    sys.exit(0)


def main(args):
    usage = '''
      #send "Lx BSPs" status to you to mail list "lpd-eng-bsp and  lei.yang" 
        %s -d "Lx BSPs" -t "lpd-eng-bsp lei.yang"
      #send 'Lei Yang' and 'Wei Gao's status in "Lx BSPs" to mail list "lpd-eng-bsp and  CDC-ENG-Linux-core-test" 
        %s -d "Lx BSPs" -n "Lei Yang,Wei Gao" -t "lpd-eng-bsp CDC-ENG-Linux-core-test"
      # create all the testing task for US69113 based on current dev task automatically 
        %s -u US69113 -d "Lx BSPs" -o "Lei Yang" -a 
      # create task "xxxx" for US69113 in "Lx BSPs"
        %s -u US69113 -d "Lx BSPs" -o "Lei Yang" -c "xxxx" 
      # list all the US in current sprint for "Lx Userspace" 
        %s -d "Lx Userspace" -l 
      # list the task of US69113 in "Lx BSPs"
        %s -d "Lx BSPs" -u US69113
      # For component can be(it can be used in any product):
            "Linux Core Project"
            "Lx Test"
            "Lx BSPs" (default)
            "Lx Kernel"
            "Lx Userspace"
            "Lx Build System"
            "Lx Tools"
	    "Linux Nucleo-T"
            "Vx-7 Test"
            "Vx-7 Project"
            "Vx-7 Cert Test"
            ..............
            ..............
            ..............
           
    ''' %(__file__,__file__,__file__,__file__,__file__,__file__)
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--domain",  \
                     action="store", type="string", dest="domain",help="domain")
    parser.add_option("-u", "--userstory",  \
                     action="store", type="string", dest="userstory",help="userstory")
    parser.add_option("-o", "--owener",  \
                     action="store", type="string", dest="owner",help="task owner")
    parser.add_option("-c", "--ctask",  \
                     action="store", type="string", dest="task_name",help="task name")
    parser.add_option("-l", action="store_true", dest="listall",help="list all userstory")
    parser.add_option("-a", action="store_true", dest="auto",help="auto create userstory")
    parser.add_option("-t", "--team",  \
                     action="store", type="string", dest="send",help="send to whom")
    parser.add_option("-n", "--names",  \
                     action="store", type="string", dest="names",help="whose status you want to get")
    parser.add_option("-r", "--release",  \
                     action="store", type="string", dest="release",help="given an release to list features")
 #   parser.add_option("-m", action="store_true", dest="mine",help="list the my userstory")
    (options, args) = parser.parse_args()
    userstory = options.userstory
    release = options.release
    owner = options.owner
    if not owner:
        owner = None 
    listall = options.listall
    auto = options.auto
#    mine = options.mine
    task_name = options.task_name
    domain = options.domain
    send = options.send
    names = options.names
    if not domain:
        domain = "Lx BSPs"
    

    options = [opt for opt in args if opt.startswith('--')]
#    print options
    args    = [arg for arg in args if arg not in options]
    #server, user, password, apikey, workspace, project = rallyWorkset(options)
    server, user, password, apikey, workspace, project = "rally1.rallydev.com", "interface_rally@windriver.com", "interface_rally", "","Wind River", "%s" %domain
    #server, user, password, apikey, workspace, project = "rally1.rallydev.com", "lei.yang@windriver.com", "windwind001", "","Wind River", "%s" %domain
    #help(Rally)
    #print " ".join(["|%s|" % item for item in [server, user, password, workspace, project]])
    #rally = Rally(server, user, password, workspace=workspace, project=project)
    rally=con_rally(server, user, password, workspace=workspace, project=project)
    #help(rally)
    rally.enableLogging('fire.log')
    specified_workspace = workspace

    workspace = rally.getWorkspace()
    #print dir(a)
    #print "Workspace: %s " % workspace.Name

    target_project = rally.getProject()
    #target_story   = rally.get('UserStory', query='FormattedID = %s' % storyID, instance=True)
    #print "Project  : %s " % project.Name
    #return target_project,target_story
    return rally,userstory,owner,listall,auto,task_name,send,domain,names,release

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    rally,userstory,owner,listall,auto,task_name,send,domain,names,release=main(sys.argv[1:])
    sprint,end_date,today=current_iteration(rally)
    iteration_criterion = 'iteration.Name = \"%s\"' %sprint
    a=rally.getProject(name="%s" %domain)
    current_iteration(rally)
    if a.ScrumMaster:
        scrum_master=a.ScrumMaster
    else:
        scrum_master="Not defined"
    #get_task_info(rally,domain)
    create_task.counter = 100
    if userstory and owner and auto:
        auto_create_all_task(rally,userstory,owner)
    if listall:
        list_userstory(rally)
        send_email(names,domain,send)
    if (not task_name) and (not owner) and ( not auto):
        if userstory:
            list_tasks(rally,userstory)
    if userstory and task_name and owner:
        create_task(userstory,task_name,owner)
    if (not userstory) and (not auto) and (not send) and (not release):
        #get_task_info(rally,get_task_info)
        send_email(names,domain,send)
    if release:
        list_features(rally,release)
    if send:
        send_email(names,domain,send)

