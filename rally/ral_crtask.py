#!/usr/bin/env python

#################################################################################################
#
#  rallyfire - Exemplar script to test the basic connectivity to a Rally server
#              and obtain basic workspace and project information
#
#################################################################################################

import sys
from optparse import OptionParser
from pyral import Rally, rallyWorkset

#################################################################################################

errout = sys.stderr.write

#################################################################################################

def auto_create_all_task(rally,userstory,owner):
    storyID = userstory
    response   = rally.get('UserStory', query='FormattedID = %s' % storyID)
#    story1 = response.next()
#    print story1.details()
    task_list=[]
    for story in response:
        for task in story.Tasks:
#            print task.oid, task.Name
#            print dir(task)
#            print task.Owner.Name
            task_list.append(task.Name)
#    print task_list
    for task in task_list:
        auto_create_task(userstory,task,owner)
    sys.exit(0)

def auto_create_task(userstory,task_name,task_owner):
    target_story   = rally.get('UserStory', query='FormattedID = %s' % userstory, instance=True)
    task_owner = rally.getUserInfo(name=task_owner).pop(0)
    info = {
             "Project"     : rally.getProject().ref,
             "WorkProduct" : target_story.ref,
              'Owner'      : task_owner.ref,
             "Name"        : '[TEST] %s' %task_name,
             "State"       : "Defined",
             #"TaskIndex"   : 1,
             #"Description" : "Fly to Chile next week to investigate the home of potatoes.  Find the absolute gigantoidist spuds and bring home the eyes to Idaho.  Plant, water, wonder, harvest, wash, slice, plunge in and out of hot oil, drain and enjoy! Repeat as needed.",
             "Estimate"    : 2.0,
             "Actuals"     :  2.0,
             "ToDo"        : 2.0,
             #"Notes"       : "I have really only done some daydreaming wrt this task.  Sorry Jane, I knew you had big plans for Frankie's blowout BBQ next month, but the honeycomb harvest project is taking all my time."
           }

    task = rally.put('Task', info)
    #print "Created  Task: %s   OID: %s" % (task.FormattedID, task.oid)
    print "Created  Task: %s [TEST] %s" % (task.FormattedID,task_name)



def main(args):
    parser = OptionParser()
    parser.add_option("-u", "--userstory",  \
                     action="store", type="string", dest="userstory",help="userstory")
    parser.add_option("-o", "--owener",  \
                     action="store", type="string", dest="owner",help="task owner")
    (options, args) = parser.parse_args()
    userstory = options.userstory
    owner = options.owner

    options = [opt for opt in args if opt.startswith('--')]
#    print options
    args    = [arg for arg in args if arg not in options]
    #server, user, password, apikey, workspace, project = rallyWorkset(options)
    server, user, password, apikey, workspace, project = "rally1.rallydev.com", "lei.yang@windriver.com", "windwind001", "","Wind River", "Lx BSPs"
#    print server, user, password, apikey, workspace, project
    #print " ".join(["|%s|" % item for item in [server, user, password, workspace, project]])
    rally = Rally(server, user, password, workspace=workspace, project=project)
    rally.enableLogging('fire.log')
    specified_workspace = workspace

    workspace = rally.getWorkspace()
    print "Workspace: %s " % workspace.Name

    target_project = rally.getProject()
    #target_story   = rally.get('UserStory', query='FormattedID = %s' % storyID, instance=True)
    #print "Project  : %s " % project.Name
    #return target_project,target_story
    return rally,userstory,owner

if __name__ == '__main__':
    rally,userstory,owner=main(sys.argv[1:])
    auto_create_all_task(rally,userstory,owner)
