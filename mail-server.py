import email
import os,sys
import dkim
from datetime import datetime
#
#import dkim
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import perf_counter, sleep

sys.path.append('/media/sf_shared_VMs/common_py')
from common import readfileNoStrip, checkAdminRights, subPopenTry

sender = ''
queue_dir = '/media/sf_shared_VMs/mail'
log_file = os.path.join(queue_dir,'emails.log')
loop_period = 10 # sec
domain = 'soardata.org'
private_key_path = 'dkimKey' # also in: '/etc/opendkim/keys/soardata.org/default.private'


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
        #sender = lines[0].strip()
        recipient = lines[1].strip()
        firstName =  lines[2].strip()
        subject = lines[3].strip()
        bodyStart = 4 #line 4
        timeTag = datetime.now().strftime("%y/%m/%d %H:%M:%S")
        plain = ['Hi {},\n'.format(firstName)]
        html = []

        for il,line in enumerate(lines[bodyStart:]):
            if not line[0] == '<':
                plain.append(line)
            else:
                html = lines[bodyStart + il:]
                break

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg['Date'] = email.utils.formatdate()
        msg['Message-ID'] = email.utils.make_msgid(domain=domain)
        msg.attach(MIMEText(''.join(plain), "plain"))
        msg.attach(MIMEText(''.join(html), "html"))
        try:
            sig = dkim.sign(
                message=msg.as_string().encode("ascii"),
                selector=str("mail").encode("ascii"),
                domain=domain.encode("ascii"),
                privkey=private_key,
                include_headers=headers, )
            msg["DKIM-Signature"] = sig.decode("ascii").lstrip("DKIM-Signature: ")
            s = smtplib.SMTP("{}".format('localhost:25'))
            s.sendmail(sender, recipient, msg.as_string())
            print(timeTag, 'sent', recipient, sender, subject)
            f = open(log_file,'a')
            f.write('{} sent {} {} {}'.format(timeTag, recipient, sender, subject))
            f.close()
            os.remove(message_file)
        except Exception as e:
            print(e, recipient,sender, subject)
    sleep(loop_period)



