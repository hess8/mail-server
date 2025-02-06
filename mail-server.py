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


queue_dir = '/media/sf_landscapes-zip/mail'
if not os.path.exists(queue_dir):
    os.mkdir(queue_dir)

loop_period = 60 # sec

go = True
while go:
    to_send = []
    items = os.listdir(queue_dir)
    for item in items:
        if '.msg' in item:
         to_send.append(item)
    for message_file in to_send:
        lines = readfileNoStrip(os.path.join(queue_dir,message_file))
        #sender = lines[0].strip()
        sender = 'bret@soardata.org'
        recipient = lines[1].strip()
        body = ''
        for line in lines[2:]:
            body += line
        s = smtplib.SMTP('soardata.org')
        s.sendmail(sender, recipient, body)
        s.quit()
        sys.exit('Stop')
        sleep(loop_period)



