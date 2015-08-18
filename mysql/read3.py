 '''
  This code use python MySQLdb syntax
 '''

 import MySQLdb
 conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "root",db = 
"TESTDB1")
 cursor = conn.cursor ()

 sql="SELECT * from TESTDB1 where fname='Mac'";
 cursor.execute (sql)
 rows = cursor.fetchall ()

 for row in rows:
  print "%s, %s" % (row[0], row[1])
 cursor.close ()
 conn.close ()
 print "Fetch success"
 
