import os, sys, shutil
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import perf_counter, sleep
from datetime import datetime

shared_path = '/media/shared_VMs'
sys.path.append(os.path.join(shared_path,'common_py'))

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def read_file_no_strip(filepath):
    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    return lines

queue_dir = os.path.join(shared_path,'mail','queued')
sent_dir = os.path.join(shared_path,'mail','sent')
log_file = os.path.join(shared_path,'emails.log')
loop_period = 10 # sec
spinner = spinning_cursor()
spin_tick = 0.3 #sec

if not os.path.exists(queue_dir): os.mkdir(queue_dir)
if not os.path.exists(sent_dir): os.mkdir(sent_dir)
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
        lines = read_file_no_strip(queued_path)
        sender = lines[0].strip()
        domain = sender.split('@')[1]
        recipient = lines[1].strip()
        subject = lines[2].strip()
        body_start = 3 #line 4
        time_tag = datetime.now().strftime("%y/%m/%d %H:%M:%S")
        html = lines[body_start:]

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
            print(time_tag, 'sent', recipient, sender, subject,'\n')
            f = open(log_file,'a')
            f.write('{} sent {} {} {}\n'.format(time_tag, recipient, sender, subject))
            sent_path = os.path.join(sent_dir,message_name)
            shutil.move(queued_path,sent_path)
            os.system('touch {}'.format(sent_path)) #
        except Exception as e:
            print(e, recipient,sender, subject,'\n')
            f.write('{} err  {} {} {}\n'.format(time_tag, recipient, e, subject))
        f.close()
    for _ in range(int(loop_period/spin_tick)):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sleep(spin_tick)
        sys.stdout.write('\b')



