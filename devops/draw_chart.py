#!/usr/bin/env python

def die(message):
    print(message)
    import sys
    sys.exit(1)

import optparse
import json
from getpass import getpass
try:
    import pygraphviz as pgv
except ImportError:
    die("Please install pygraphviz (in debian: python-pygraphviz)")
try:
    from restkit import Resource, BasicAuth
except ImportError:
    die("Please install restkit (in debian: python-restkit)")

# Using REST is pretty simple. The vast majority of this code is about the "other stuff": dealing with
# command line options, formatting graphviz, calling Google Charts, etc. The actual JIRA REST-specific code
# is only about 5 lines.


def fetcher_factory(url, auth):
    """ This factory will create the actual method used to fetch issues from JIRA. This is really just a closure that saves us having
        to pass a bunch of parameters all over the place all the time. """
    def get_issue(key):
        """ Given an issue key (i.e. JRA-9) return the JSON representation of it. This is the only place where we deal
            with JIRA's REST API. """
        print('Fetching ' + key)
        # we need to expand subtasks and links since that's what we care about here.
        resource = Resource(url + ('/rest/api/latest/issue/%s' % key), filters=[auth])
        response = resource.get(headers={'Content-Type': 'application/json'})
        if response.status_int == 200:
            # Not all resources will return 200 on success. There are other success status codes. Like 204. We've read
            # the documentation for though and know what to expect here.
            issue = json.loads(response.body_string())
            return issue
        else:
            return None
    return get_issue


def build_graph_data(start_issue_key, get_issue, epic_id):
    """ Given a starting image key and the issue-fetching function build up the GraphViz data representing relationships
        between issues. This will consider both subtasks and issue links.
    """
    def get_key(issue):
        return issue['key']

    # since the graph can be cyclic we need to prevent infinite recursion
    seen = []

    def walk(issue_key, graph):
        """ issue is the JSON representation of the issue """
        try:
            issue = get_issue(issue_key)
        except Exception:
            print("Could not get issue:", issue_key)
            raise()
        seen.append(issue_key)
        children = []
        fields = issue['fields']
        if fields.get(epic_id):
            epickey = fields[epic_id]
            if (epickey, get_key(issue)) not in graph.edges():
                graph.add_edge(epickey, get_key(issue), color='violet', label='epic')
                children.append(epickey)
        if 'subtasks' in fields:
            for subtask in issue['fields']['subtasks']:
                if (get_key(issue), get_key(subtask)) not in graph.edges():
                    graph.add_edge(get_key(issue), get_key(subtask), color='blue', label='subtask', penwidth='0.5')
                children.append(subtask['key'])
        if 'issuelinks' in fields:
            for link in issue['fields']['issuelinks']:
                if 'outwardIssue' in link:
                    if (get_key(issue), get_key(link['outwardIssue'])) not in graph.edges():
                        graph.add_edge(get_key(issue), get_key(link['outwardIssue']), label=link['type']['outward'])
                        children.append(link['outwardIssue']['key'])
                if 'inwardIssue' in link:
                    if (get_key(link['inwardIssue']), get_key(issue)) not in graph.edges():
                        graph.add_edge(get_key(link['inwardIssue']), get_key(issue), label=link['type']['outward'])
                        children.append(link['inwardIssue']['key'])
        # now construct graph data for all subtasks and links of this issue
        for child in (x for x in children if x not in seen):
            walk(child, graph)
        return graph

    graph = pgv.AGraph(strict=False, directed=True)
    graph.graph_attr['label'] = 'Dependency Graph for %s' % start_issue_key
    graph.add_node(start_issue_key, color='red', penwidth='2.0')
    graph = walk(start_issue_key, graph)
    return graph

# Epic Link is a custom field so we need to find its id:
def get_epic_id(url, key, auth):
        resource = Resource(url + ('/rest/api/latest/issue/%s?expand=names' % key), filters=[auth])
        response = resource.get(headers={'Content-Type': 'application/json'})
        if response.status_int == 200:
            for field_id, field_name in json.loads(response.body_string())['names'].items(): 
                if field_name == 'Epic Link':
                    return field_id
        else:
            return None

def create_local_graph_image(graph, image_file):
    graph.layout(prog='dot')
    print('Writing to ' + image_file)
    graph.draw(image_file)


def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--user', dest='user', default='admin', help='Username to access JIRA')
    parser.add_option('-p', '--password', dest='password', help='Password to access JIRA')
    parser.add_option('-j', '--jira', dest='jira_url', default='http://jira.example.com', help='JIRA Base URL')
    parser.add_option('-f', '--file', dest='image_file', default='issue_graph.png', help='Filename to write image to')

    return parser.parse_args()


def get_password():
    return getpass("Please enter the Jira Password:")

if __name__ == '__main__':
    (options, args) = parse_args()
    print args

    # Basic Auth is usually easier for scripts like this to deal with than Cookies.
    auth = BasicAuth(options.user, options.password or get_password())
    issue_fetcher = fetcher_factory(options.jira_url, auth)

    if len(args) != 1:
        die('Must specify exactly one issue key. (e.g. JRADEV-1107, JRADEV-1391)')
    start_issue_key = args[0]

    epic_id = get_epic_id(options.jira_url, start_issue_key, auth)

    graph = build_graph_data(start_issue_key, issue_fetcher, epic_id)
    create_local_graph_image(graph, options.image_file)
