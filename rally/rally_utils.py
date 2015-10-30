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
    #criterion=['FormattedID = %s' % userstory, 'User.ref.DisplayName = "Chunguang Yang"']
    criterion='FormattedID = %s' % userstory
#    criterion='FormattedID = TA113895'
    response   = rally.get('UserStory', query=criterion)
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
            if 'LIN8' not in task.Name:
                task_list.append(task.Name)
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
             "State"       : "Defined",
             "TaskIndex"   : create_task.counter,
             #"Description" : "Fly to Chile next week to investigate the home of potatoes.  Find the absolute gigantoidist spuds and bring home the eyes to Idaho.  Plant, water, wonder, harvest, wash, slice, plunge in and out of hot oil, drain and enjoy! Repeat as needed.",
             "Estimate"    : 2.0,
             "Actuals"     :  2.0,
             "ToDo"        : 2.0,
             #"Notes"       : "I have really only done some daydreaming wrt this task.  Sorry Jane, I knew you had big plans for Frankie's blowout BBQ next month, but the honeycomb harvest project is taking all my time."
           }

    task = rally.put('Task', info)
    #print "Created  Task: %s   OID: %s" % (task.FormattedID, task.oid)
    print "Created  Task: %s [TEST] %s" % (task.FormattedID,task_name)

def list_userstory(rally):
    response = rally.get('UserStory', query=iteration_criterion)
    for story in response:
        print '    %s: %s' %(story.FormattedID,story.Name)
#    print dir(story)
 #   print story.FormattedID

def list_my_userstory(rally):
    response = rally.get('UserStory', query=iteration_criterion)
    my_task_list=[]
    for story in response:
        for task in story.Tasks:
            if owner in task.Owner.Name:
                my_task_list.append('    %s: %s' %(story.FormattedID,story.Name))
                #print '    %s: %s' %(story.FormattedID,story.Name)
    for us in list(set(my_task_list)):
        print us


def list_tasks(rally,userstory):
    response   = rally.get('UserStory', query='FormattedID = %s' % userstory)
   # story1 = response.next()
   # print story1.details()
    task_list=[]
    for story in response:
        print '%s: %s' %(story.FormattedID,story.Name)
        for task in story.Tasks:
#            print task.oid, task.Name
  #           print task.Owner.Name
             print '         %s:%s' %(task.FormattedID,task.Name)
 


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



def main(args):
    usage = '''
      #create all the testing task for US69113
      %s -u US69113 -o "Lei Yang" -a 
      #list all the US in current sprint 
      %s -l 
      #list the task of US69113
      %s -u US69113
      #list the userstory that 'Lei Yang' working on 
      %s -o 'Lei Yang' -m
    ''' %(__file__,__file__,__file__,__file__)
    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--userstory",  \
                     action="store", type="string", dest="userstory",help="userstory")
    parser.add_option("-o", "--owener",  \
                     action="store", type="string", dest="owner",help="task owner")
    parser.add_option("-t", "--task",  \
                     action="store", type="string", dest="task_name",help="task name")
    parser.add_option("-l", action="store_true", dest="listall",help="list all userstory")
    parser.add_option("-a", action="store_true", dest="auto",help="auto create userstory")
    parser.add_option("-m", action="store_true", dest="mine",help="list the my userstory")
    (options, args) = parser.parse_args()
    userstory = options.userstory
    owner = options.owner
    listall = options.listall
    auto = options.auto
    mine = options.mine
    task_name = options.task_name

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
    #print "Workspace: %s " % workspace.Name

    target_project = rally.getProject()
    #target_story   = rally.get('UserStory', query='FormattedID = %s' % storyID, instance=True)
    #print "Project  : %s " % project.Name
    #return target_project,target_story
    return rally,userstory,owner,listall,auto,task_name,mine

if __name__ == '__main__':
    rally,userstory,owner,listall,auto,task_name,mine=main(sys.argv[1:])
    iteration_criterion = 'iteration.Name = \"Lx8 S9 15-11-16\"'
    create_task.counter = 100
    if userstory and owner and auto:
        auto_create_all_task(rally,userstory,owner)
    if listall:
        list_userstory(rally)
    if (not task_name) and (not owner) and ( not auto):
        if userstory:
            list_tasks(rally,userstory)
    if userstory and task_name and owner:
        create_task(userstory,task_name,owner)
    if mine and owner:
        list_my_userstory(rally)
