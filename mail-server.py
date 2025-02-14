import os, sys
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import perf_counter, sleep
from datetime import datetime

sys.path.append('/media/sf_shared_VMs/common_py')
from common import readfileNoStrip, checkAdminRights, subPopenTry

sender ='SkylinesCondor'
queue_dir = '/media/sf_shared_VMs/mail'
log_file = os.path.join(queue_dir,'emails.log')
loop_period = 10 # sec
domain = 'soardata.org'
private_key_path = 'dkimPrivate' # also in: '/etc/opendkim/keys/soardata.org/default.private'


#if not checkAdminRights():
#    sys.exit('Stop.  Must run with admin privileges: sudo /snap/pycharm-community/current/bin/pycharm')
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
        message_file = os.path.join(queue_dir,message_name)
        lines = readfileNoStrip(message_file)
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
        try:
            #sig = dkim.sign(
            ##     message=msg.as_string().encode("ascii"),
            #     selector=str("default").encode("ascii"),
            #     domain=domain.encode("ascii"),
            #     privkey=private_key,
            #     include_headers=headers, )
            #msg["DKIM-Signature"] = sig.decode("ascii").lstrip("DKIM-Signature: ")
            s = smtplib.SMTP("{}".format('localhost:25'))
            s.sendmail(sender, recipient, msg.as_string())
            print(timeTag, 'sent', recipient, sender, subject,'\n')
            f = open(log_file,'a')
            f.write('{} sent {} {} {}\n'.format(timeTag, recipient, sender, subject))
            f.close()
            os.remove(message_file)
        except Exception as e:
            print(e, recipient,sender, subject,'\n')
    sleep(loop_period)



