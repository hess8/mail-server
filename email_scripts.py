import os


def to_HTML(line):
    '''
    Adds paragraph tags to a line
    '''
    if line.strip()[:3] not in ['<p>', '<br', '<hr']:
        newline = '<p>{}</p>\n'.format(line.rstrip('\n'))
    else:
        newline = line
    return newline


def queue_email(mail_dir, sender_addr, recip_name, recip_adrr, subject, message_list, help_line='', signature_line='', id=None):

    """
    Queues email to a recipient or a test address.
    creates a text file for each email that email server
    on another machine will read

    message_list: a list of lines that has all html needed except for paragraph tags
    """
    domain = sender_addr.split('@')[1]
    from datetime import datetime
    time_format = '%Y-%m-%d.%H.%M.%S.%f'
    queued_dir = os.path.join(mail_dir, 'queued')
    log_file = os.path.join(mail_dir,'emails.log')
    for path in [mail_dir, queued_dir]:
        if not os.path.exists(path): os.mkdir(path)
    html = []
    for line in message_list:
        html.append(to_HTML(line))
    html.append(help_line)
    html.append(signature_line)
    try:
        file_name = f'{datetime.now().strftime(time_format)}_{domain}.msg'
        time_tag = datetime.now().strftime('%y/%m/%d %H:%M:%S')
        f = open(os.path.join(queued_dir, file_name), 'w')
        f.write(sender_addr + '\n')
        f.write(recip_adrr + '\n')
        f.write(subject + '\n')
        f.writelines(html)
        f.close()

        f = open(log_file, 'a')
        f.write(f'{time_tag} queu {recip_name} {recip_adrr} {sender_addr} {subject}\n')
        f.close()

        recip_str = recip_name
        if id:
            recip_str += f' {id}'
        print(f'Queued email: {recip_str} - {recip_adrr} - {subject} - {sender_addr}')
    except BaseException as e:
        print(f'Failed to queue: {recip_str} - {recip_adrr} - {subject} - {sender_addr}')
        print(e)
