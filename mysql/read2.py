#!/usr/bin/env python
import sys, MySQLdb

def PrintFields(database, table):
    """ Connects to the table specified by the user and prints out its fields in HTML format used by Ben's wiki. """
    host = 'localhost'
    user = 'user'
    password = 'password'
    conn = MySQLdb.Connection(db='TESTDB1', host='localhost', user='root', passwd='root')
    mysql = conn.cursor()
    sql = """ SHOW COLUMNS FROM %s """ % table
    mysql.execute(sql)
    fields=mysql.fetchall()
    print '<table border="0"><tr><th>order</th><th>name</th><th>type</th><th>description</th></tr>'
    print '<tbody>'
    counter = 0
    print fields
    for field in fields:
        counter = counter + 1
        name = field[0]
        type = field[1]
        print '<tr><td>' + str(counter) + '</td><td>' + name + '</td><td>' + type + '</td><td></td></tr>'
    print '</tbody>'
    print '</table>'
    mysql.close()
    conn.close()

users_database = sys.argv[1]
users_table = sys.argv[2]
print "Wikified HTML for " + users_database + "." + users_table
print "========================"
PrintFields(users_database, users_table)

