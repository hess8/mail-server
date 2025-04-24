import os, sys, shutil
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import perf_counter, sleep
from datetime import datetime
from dotenv import load_dotenv

sys.path.append('/media/sf_shared_VMs/common_py')
from common import readfileNoStrip, checkAdminRights, subPopenTry

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

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

sender ='SkylinesCondor'
queue_dir = '/media/sf_shared_VMs/mail/queued'
sent_dir = '/media/sf_shared_VMs/mail/sent'
log_file = os.path.join(queue_dir,'emails.log')
loop_period = 10 # sec
domain = 'soardata.org'
private_key_path = '../.secure/dkimPrivate'
spinner = spinning_cursor()
spinTick = 0.3 #sec


if not os.path.exists(queue_dir): os.mkdir(queue_dir)
if not os.path.exists(sent_dir): os.mkdir(sent_dir)
with open(private_key_path, 'rb') as f:
    private_key = f.read()
if not os.path.exists(queue_dir):
    os.mkdir(queue_dir)

headers = ["To", "From", "Subject"]
go = True
while go:
    to_send = []
    items = os.listdir(queue_dir)
    for item in items:
        if '.msg' in item:
         to_send.append(item)
    for message_name in to_send:
        queued_path = os.path.join(queue_dir,message_name)
        lines = readfileNoStrip(queued_path)
        recipient = lines[1].strip()
        subject = lines[2].strip()
        bodyStart = 3 #line 4
        timeTag = datetime.now().strftime("%y/%m/%d %H:%M:%S")
        html = lines[bodyStart:]

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg['Date'] = email.utils.formatdate()
        msg['Message-ID'] = email.utils.make_msgid(domain=domain)
        msg.attach(MIMEText(''.join(html), "html"))
        f = open(log_file, 'a')
        try:
            s = smtplib.SMTP("{}".format('localhost:25'))
            s.sendmail(sender, recipient, msg.as_string())

            print(timeTag, 'sent', recipient, sender, subject,'\n')
            f = open(log_file,'a')
            f.write('{} sent {} {} {}\n'.format(timeTag, recipient, sender, subject))
            sent_path = os.path.join(sent_dir,message_name)
            shutil.move(queued_path,sent_path)
            os.system('touch {}'.format(sent_path)) #
        except Exception as e:
            print(e, recipient,sender, subject,'\n')
            f.write('{} err  {} {} {}\n'.format(timeTag, recipient, e, subject))
        f.close()
    for _ in range(int(loop_period/spinTick)):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sleep(spinTick)
        sys.stdout.write('\b')



