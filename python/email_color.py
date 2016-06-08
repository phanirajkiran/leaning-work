#!/usr/bin/python

#This will send an email by authenticating with an SMTP email server
#Works on gmail, Google apps email accounts, exchange accounts, anything using SMTP
#Tested on Linux and Mac, should work where ever python is present
#Lots of comments below explaining what is happening at each section
#Feel free to use/edit/whatever to your heart's conent, no attribution needed
#
#Remember to enter your details into the relevent sections listed below before running
#Change the following: first@emailaddress.com, second@emailaddress.com, your@emailaddress.com, youremailaddress@gmail.com, yourpassword

#Import Python modules for sending email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Where the email is being sent to (multiple email address example given if needed)
#If only one is needed just delete the 2nd address as per the comment example below
#emailto   = ['first@emailaddress.com']
emailto   = ['first@emailaddress.com', 'second@emailaddress.com']

#Who the email is being sent from (if using gmail this is ignored, can only send from account owners adddress)
emailfrom = 'your@emailaddress.com'

#Put email message info together. Edit subject line if needed.
message = MIMEMultipart('alternative')
message['To'] = ", ".join(emailto)
message['From'] = emailfrom
message['Subject'] = 'Test email'

#Create your HTML message
htmlemailmessage = unicode("""
<html>
    <head></head>
    <body>
        <p>Hello, this is a test</p>
        <p><strong>Bold text</strong></p>
        <p style="color:#FF0000;">Red text</p>
    </body>
</html>
""")

#Create your plain text message
plaintextemailmessage = unicode("""
Hello this is a test.
No HTML formatting.
""")

#Add the HTML and plain text messages to the message info list (array)
storeplain = MIMEText(plaintextemailmessage, 'plain')
storehtml = MIMEText(htmlemailmessage, 'html')
message.attach(storeplain)
message.attach(storehtml)

#Details of your SMTP server (gmail SMTP url & port entered, change if needed)
#If you're using an exchange server, port 587 should work as well
deetsurl = smtplib.SMTP('147.11.189.50','25')

#Send our prepared message to the SMTP server for a request to send
deetsurl.sendmail('lei.yang@windriver.com', "liang.chi@windriver.com", message.as_string())

#All done so print a message saying the email has been sent, and quit the SMTP session
print "Email sent."
