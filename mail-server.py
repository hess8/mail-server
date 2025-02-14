import os, sys
#
#import dkim
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import perf_counter, sleep

sys.path.append('/media/sf_shared_VMs/common_py')
from common import readfileNoStrip, checkAdminRights

private_key_path = '/etc/opendkim/keys/soardata.org/default.private'
queue_dir = '/media/sf_landscapes-zip/mail'

if not checkAdminRights():
    sys.exit('Stop.  Must run with admin privileges: sudo /snap/pycharm-community/current/bin/pycharm')
with open(private_key_path, 'rb') as f:
    private_key = f.read()
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
        subject =  lines[2].strip()
        plain = lines[3]
        html = lines[4]
        msg = MIMEMultipart('alternative')
        msg["Subject"] = subject
        msg["From"] = sender
        msg.attach(MIMEText(plain, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        dkim_header = dkim.sign(
            msg.as_bytes(),
            private_key=private_key,
            #selector=selector,
            domain='soardata.org'
        )
        msg_str = dkim_header.decode('utf-8') + '\n' + msg.as_string()
        try:
            server = smtplib.SMTP_SSL('localhost',465) #port 465 does automatic encryption
#            server.login('your_smtp_username', 'your_smtp_password')
            server.sendmail(sender, recipient, msg_str)
            server.quit()
            print("Email sent successfully with DKIM signature.")
        except Exception as e:
            print(f"Error sending email: {e}")




        s = smtplib.SMTP('soardata.org')
        s.sendmail(sender, recipient, body)
        s.quit()
        sys.exit('Stop')
        sleep(loop_period)



