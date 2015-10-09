#!/usr/bin/env python

import smtplib
from smtplib import SMTPException
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys
from optparse import OptionParser
import ConfigParser
import getpass
from os.path import expanduser
import commands


parser = OptionParser()
parser.add_option("-p", "--path",  \
                 action="store", type="string", dest="path",help="test case path")
(options, args) = parser.parse_args()
path = options.path

sender = "lei.yang@windriver.com"
receiver = "wei.gao@windriver.com"
subject = "xxxx"
text_mail='mail'
txt=open(text_mail, "a")
txt.write('o Peer Reviewer:\n')
txt.write('lei.yang\n')
txt.write('1. Priority\n')
txt.write('****************************\n')
txt.write('2\n')
txt.write('2. Repeatability :\n')
txt.write('****************************\n')
txt.write('reproducible\n')
txt.write('3. Summary:\n')
txt.write('****************************\n')
txt.write('4. Engineering Details (Not Published):\n')
txt.write('Environment\n')
txt.write('======================\n')
txt.write('Requirement No.: US66411\n')
txt.write('WRLinux Version: 8.0.0.0\n')
txt.write('5. Symptom Details\n')
txt.write('Problem Description\n')
problem=commands.getoutput('cat %s |grep -B 1 -A 1 "ERROR CMD OR INFO IS"'%path)
txt.write(problem)
txt.write('\n')
txt.write('6. Steps To Reproduce\n')
step = commands.getoutput("cat %s |sed  '1,/Testing Env/d'" %path)
txt.write('\n')
txt.write(step)
txt.close()
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = subject

file = open(text_mail, 'r')
body = "%s" %(file.read())
file.close()
commands.getoutput('rm -rf %s' %text_mail)
msg.attach(MIMEText(body, 'plain'))
text = msg.as_string()
try:
   smtpObj = smtplib.SMTP('147.11.189.50','25')
   smtpObj.sendmail(sender,receiver, text)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"

