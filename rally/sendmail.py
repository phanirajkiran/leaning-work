#!/usr/bin/env python

import smtplib
from smtplib import SMTPException
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import commands
import os 
from datetime import datetime

def send_email():
    sender = "lei.yang@windriver.com"
    receiver = ["lei.yang@windriver.com"]
    cc= ["lei.yang@windriver.com"]
    subject = "BSP Testers Rally Task Status" 
    text_mail='./xx'
#    if os.path.exists(text_mail):
 #       os.remove(text_mail)
    txt=open(text_mail, "a")
    txt.close()
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(receiver)
    msg['Cc'] = ", ".join(cc)
    msg['Subject'] = subject
    
    file = open(text_mail, 'r')
    body = "%s" %(file.read())
    file.close()
    msg.attach(MIMEText(body, 'html'))
    text = msg.as_string()
    try:
       smtpObj = smtplib.SMTP('147.11.189.50','25')
       smtpObj.sendmail(sender,receiver, text)
       print "Successfully sent email"
    except SMTPException:
       print "Error: unable to send email"
send_email()
