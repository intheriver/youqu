# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import common

smtpserver = 'smtp.fiberhome.com'
username = common.mail_addr
password = common.mail_pw
sm = smtplib.SMTP(smtpserver,timeout=20)
#sm.set_debuglevel(1)

def sendmail(to_addr , content,
    cc_addr = None,
    subject = "signin notification"):

    from_addr = username
    message = MIMEText(content, 'plain', 'utf-8')
    message["Subject"] = subject
    message["From"] = from_addr
    message["To"] = to_addr
    message["Cc"] = cc_addr

    msg = message.as_string()

    try:
        sm.login(username,password)
        sm.sendmail(from_addr , to_addr , msg)
        sm.quit()
    except Exception as ex:
        print ex

