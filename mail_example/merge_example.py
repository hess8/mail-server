import os

from mail_common import readfile_no_strip
from mail_merge import merge

"""
See README.md for the description of this mailmerge example
"""

base_dir = '/home/bret/mail-server/'
mail_dir = '/home/bret/mail-server/mail_example/mail'
nominations = os.path.join(base_dir,'mail_example/nominations.csv')
addresses = os.path.join(base_dir,'mail_example/members.csv')
test_address = 'admin@gmail.com'
sender_name = 'president'
domain = 'mydomain.org'
subject = 'You were nominated for the board election'
message = readfile_no_strip('merge_message.txt')

# to send to all members:
merge(mail_dir, subject, message, nominations, sender_name, domain, addresses_file=addresses)

# to send a single test message:
# merge(subject, message, nominations, sender_name, domain, addresses_file=addresses, test_address=test_address)



