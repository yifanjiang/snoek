#!/usr/bin/env python
# -*- coding: UTF-8 -*-  


# ---------------Usage--------------------------- 
# from snoek.custom_lib.mail_mod import sendmail
#
# sendmail(to_list,subject,context_list))
#     to_list: A list of addresses to send this mail to.
#     subject: The subject of the mail.
#     context_list: A list of messages to send.
#
# eg. sendmail([xxx@suse.com,xxx@novell.com],"A subject.","Message to send.")


import smtplib
from email.mime.text import MIMEText
from snoek.settings import MAIL_SERVER,SERVER_NAME,MAIL_PREFIX,MAIL_POSTFIX

# Private Function
############
def _sendmail_local(to_list,subject,context_list):
    '''
    Using local Host to send mail.
    '''

    from_user=SERVER_NAME+'< '+SERVER_NAME+'@'+MAIL_POSTFIX+' >'
    msg="\n".join(context_list)

    msg=MIMEText(_text=msg,_charset='utf-8')
    msg['From']=from_user
    msg['To']=";".join(to_list)
    msg['Subject']=MAIL_PREFIX+subject

    try:
        smtp=smtplib.SMTP("localhost")
	smtp.sendmail( from_user,to_list,msg.as_string() )
	smtp.close()

    except Exception,reason:
        print "Error happan in mail send:", reason
	return False

    return True

def _sendmail_LDAP(to_list,subject,context_list):
    '''
    Not finished yet. For using Novell LDAP mail account. 
    '''
    return False


# Public Function
############
def sendmail(to_list,subject,context_list):
    '''
    Choose the selected way to send mail.
    Configuration in setting.py.

    to_list: A list of addresses to send this mail to.
    subject: The subject of the mail.
    context_list: A list of messages to send.

    eg. sendmail([xxx@suse.com,xxx@novell.com],"A subject.","Message to send.")
    '''

    if MAIL_SERVER=="LDAP":
        ret=_sendmail_LDAP(to_list,subject,context_list)
    else:
        ret=_sendmail_local(to_list,subject,context_list)

    return ret
        

def main():
    '''
    Test only.
    Need to comment the line of "from snoek.settings xxx" first
    Then edit to_list below.
    '''
    # The configuration below are all in settings.py
    # Only for testing 
    global MAIL_SERVER,SERVER_NAME,MAIL_PREFIX,MAIL_POSTFIX
    MAIL_SERVER="local"
    SERVER_NAME="snoek-no-reply"
    MAIL_PREFIX="[Snoek] "
    MAIL_POSTFIX="suse.com"

    to_list=["xxx@suse.com","xxx@suse.com"]
    subject="This is a test mail from snoek server. 注意：中文邮件。"
    msg_list=["Message in english.","汉语消息。","New line.","最后一行。"]

    ret=sendmail(to_list,subject,msg_list)

    if ret is True:
        print "Succeed to send mail."
        return True
    else:
	print "Failed to send mail."
        return False

if __name__=='__main__':
    main()
