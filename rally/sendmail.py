#!/usr/bin/env python

import smtplib
from smtplib import SMTPException
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import commands
import os 
from datetime import datetime

present = datetime.now()
if present <= datetime(2015, 9, 14) and present >= datetime(2015, 8, 24):
    sprint="Lx8 S6 15-09-14"
elif present <= datetime(2015, 10, 05) and present >= datetime(2015, 9, 14):
    sprint="Lx8 S7 15-10-05"
elif present <= datetime(2015, 10, 26) and present >= datetime(2015, 10, 05):
    sprint="Lx8 S8 15-10-26"
elif present <= datetime(2015, 11, 16) and present >= datetime(2015, 10, 26):
    sprint="Lx8 S9 15-11-16"
elif present <= datetime(2015, 12, 07) and present >= datetime(2015, 11, 16):
    sprint="Lx8 S10 15-12-07"
else:
    sprint = ""

sender = "lei.yang@windriver.com"
#receiver = ["lei.yang@windriver.com","wei.gao@windriver.com","xiangyu.dong@windriver.com","liang.chi@windriver.com"]
receiver = ["lei.yang@windriver.com"]
cc= ["lei.yang@windriver.com"]
subject = "BSP Testers Rally Task Status for %s" %sprint
text_mail='/tmp/xxx'
if os.path.exists(text_mail):
    os.remove(text_mail)
txt=open(text_mail, "a")
name=['Lei Yang','Liang Chi','Xiangyu Dong','Wei Gao']
#name=['Lei Yang','Liang Chi','Xiangyu Dong','Wei Gao','Zumeng Chen','Lu Jiang','Quanyang Wang','Yanjiang Jin','Pengyu Ma','Chunguang Yang','Liwei Song']
#name=['Lei Yang']
for x in name:
    ret,results = commands.getstatusoutput("/home/lyang001/leaning-work/rally/rally_utils.py -o '%s'" %x)
    txt.write("*%s* 's Task (*Total todo* = %s hours)\n" %(x,ret >> 8))
    txt.write("==============================================\n")
    txt.write('%s\n' %results)
    txt.write('\n')
txt.close()
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = ", ".join(receiver)
msg['Cc'] = ", ".join(cc)
msg['Subject'] = subject

file = open(text_mail, 'r')
body = "%s" %(file.read())
file.close()
msg.attach(MIMEText(body, 'plain'))
text = msg.as_string()
try:
   smtpObj = smtplib.SMTP('147.11.189.50','25')
   smtpObj.sendmail(sender,receiver, text)
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"


#parser = OptionParser()
#parser.add_option("-p", "--path",  \
#                 action="store", type="string", dest="path_name",help="test case path")
#(options, args) = parser.parse_args()

