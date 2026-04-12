import os

from mail_common import readfile_no_strip
from email_scripts import email_nominees

base_dir = '/home/bret/Downloads/'
nominations = os.path.join(base_dir,'nominations.csv')
addresses = os.path.join(base_dir,'USA Member Tracking - 2026.csv')
test_address = 'bret.hess@gmail.com'
sender_name = 'bret'
audience = 'test'  # admin, test, all
queue_dir = '/media/sf_shared_VMs/mail/queued/'
subject = 'You were nominated for USA Board election'
message = readfile_no_strip('nomination.txt')

email_nominees(subject, message, nominations, sender_name, addresses_file=addresses, test_address=test_address)

