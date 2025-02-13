import email
import os,sys
import dkim
#
#import dkim
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import perf_counter, sleep

sys.path.append('/media/sf_shared_VMs/common_py')
from common import readfileNoStrip, checkAdminRights, subPopenTry

domain = 'soardata.org'
private_key_path = 'dkimKey' # also in: '/etc/opendkim/keys/soardata.org/default.private'
queue_dir = '/media/sf_shared_VMs/mail'

#if not checkAdminRights():
#    sys.exit('Stop.  Must run with admin privileges: sudo /snap/pycharm-community/current/bin/pycharm')
with open(private_key_path, 'rb') as f:
    private_key = f.read()
if not os.path.exists(queue_dir):
    os.mkdir(queue_dir)

loop_period = 60 # sec
headers = ["To", "From", "Subject"]
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
        subject =  lines[2].strip()
        plain = []
        html = []
        for line in lines[3:]:
            if line[0] =='<':
                html.append(line)
            else:
                plain.append(line)

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg['Date'] = email.utils.formatdate()
        msg['Message-ID'] = email.utils.make_msgid(domain=domain)
        msg.attach(MIMEText(''.join(plain), "plain"))
        msg.attach(MIMEText(''.join(html), "html"))
        sig = dkim.sign(
            message=msg.as_string().encode("ascii"),
            selector=str("mail").encode("ascii"),
            domain=domain.encode("ascii"),
            privkey=private_key,
            include_headers=headers, )
        msg["DKIM-Signature"] = sig.decode("ascii").lstrip("DKIM-Signature: ")
        s = smtplib.SMTP("{}".format('localhost:25'))
        s.sendmail(sender, recipient, msg.as_string())
        sleep(loop_period)



