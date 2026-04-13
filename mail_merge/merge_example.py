import os

from mail_common import readfile_no_strip
from mail_merge.mail_merge import merge

"""
See README.md for the example description
"""

base_dir = '/home/bret/mail-server/'
nominations = os.path.join(base_dir,'nominations.csv')
addresses = os.path.join(base_dir,'members.csv')
test_address = 'bret.hess@gmail.com'
sender_name = 'Bret'
domain = 'soardata.org'
queue_dir = '/home/bret/mail-server/mail/queued/'
subject = 'You were nominated for the board election'
message = readfile_no_strip('merge_message.txt')

# to send a single test message use:
merge(subject, message, nominations, sender_name, addresses_file=addresses, test_address=test_address)

# to send to all members use:
# merge(subject, message, nominations, sender_name, addresses_file=addresses)

