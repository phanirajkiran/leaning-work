#!/usr/bin/python

import MySQLdb


db1 = MySQLdb.connect(host="localhost",user="root",passwd="root")
cursor = db1.cursor()
sql = 'CREATE DATABASE TESTDB1'
cursor.execute(sql)
