import os, sys
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import perf_counter, sleep


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


from email.message import EmailMessage

def create_mime_message_from_string(message_string):
    """Creates a MIME message from a string."""

    msg = email.message_from_string(message_string)
    return msg

# Example usage
message_string = """From: sender@example.com
To: recipient@example.com
Subject: Test Message

This is the body of the email message.
"""

message = create_mime_message_from_string(message_string)


queue_dir = 'mnt/P/landscapes-zip/mail'

if not os.path.exists(queue_dir):
    os.mkdir(queue_dir)

loop_period = 60 # sec

go = True
while go:
    to_send = os.listdir(queue_dir)
    for message in to_send:


