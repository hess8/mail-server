import os,sys
import csv

from mail_common import match_names
sys.path.append('/')
from email_scripts import queue_email

""" 
Contains a mailmerge example that is called by merge_example.  See README.md
"""

def merge(mail_dir, subject, message, noms_file, sender_name, domain, addresses_file=None, test_address=None):
    message_lines = message
    with open(noms_file, mode='r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        non_header_lines = list(reader)
        total_count  = non_header_lines[0]['Total']
        n_users = non_header_lines[0]['Users']
        nominees_rows = non_header_lines[1:]

        if 'Email' not in headers:
            if not os.path.exists(addresses_file):
                sys.stop(f"Stop: nominations file {noms_file} has no Email column, but you haven't specified an address_file")
            with open(addresses_file, mode='r') as f:
                 email_rows = list(csv.DictReader(f))
                 email_nom = {}
                 e_names = []
                 for erow in email_rows:
                    e_name = f'{erow["First"]} {erow["Last"]}'
                    e_names.append(e_name)
                    if erow['Email']:
                        email_nom[e_name] = erow['Email']
                    else:
                        print(f'{e_name} in {noms_file} has no Email entry')
                 for nrow in nominees_rows:
                    matches = match_names(nrow['Name'], e_names)
                    if len(matches) == 1:
                        nrow['Email'] = email_nom[matches[0][0]]
                    elif len(matches) == 0:
                        print(f'No email found for {nrow["Name"]}')
        for nrow in nominees_rows:
            sender_addr = f'{sender_name}@{domain}'
            if test_address:
                recip_adrr = test_address
            else:
                recip_adrr = nrow['Email']

            message_lines = [
                line.replace('$first',nrow['Name'].split(' ')[0])\
                    .replace('$n_users',n_users)\
                    .replace('$count', nrow['Count'])\
                    .replace('$total_count', total_count)
                for line in message_lines
                ]

            queue_email(mail_dir, sender_addr, nrow['Name'], recip_adrr, subject, message_lines)

            if test_address: #send only one email
                break

