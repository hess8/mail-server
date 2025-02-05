import os, sys
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import perf_counter, sleep

def readfileNoStrip(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines(True) #keeplinebreaks=True.  Does not strip the lines of \n
    return lines

def sendEmail(string):
    msg = email.message_from_string(string)
    print("Sending email to {} (ID: {})...".format(user.name.encode("utf-8"), user.id))
    print(format(user.email_address))
    try:
        s.sendmail(sender, recipient.encode("ascii"), msg.as_string())
        s.quit()
    except BaseException as e:
        print(recipient)
        print("Sending email failed: {}".format(e))
        sys.exit('Stop')



queue_dir = '/media/sf_landscapes-zip/mail'
if not os.path.exists(queue_dir):
    os.mkdir(queue_dir)

loop_period = 60 # sec

go = True
while go:
    to_send = []
    items = os.listdir(queue_dir)
    for item in items:
        if '.str' in item:
         to_send.append(item)
    for message in to_send:
        lines = readfileNoStrip(os.path.join(queue_dir,item))
        sender = lines[0].strip()
        recipient = lines[1].strip()
        body = ''
        for line in lines[2:]:
            body += line
    s = smtplib.SMTP('skylinescondor.com')
    s.sendmail(sender, recipient.encode("ascii"), body)
    s.quit()

    sleep(loop_period)



