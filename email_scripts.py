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


def queue_email(sender_addr, recip_name, recip_adrr, subject, text_list, help_line='', signature_line='', id=None):
    '''
    """
    Queues email to a recipient or a test address.
    creates a text file for each email that email server
    on another machine will read
"""
    text_lines: a list of lines that has all html needed except for paragraph tags
    '''

    from datetime import datetime
    time_format = '%Y-%m-%d.%H.%M.%S.%f'
    queue_dir = '/media/sf_shared_VMs/mail/queued'
    log_file = '/media/sf_shared_VMs/mail/emails.log'
    if not os.path.exists(queue_dir):
        os.mkdir(queue_dir)
    html = []
    for line in text_list:
        html.append(to_HTML(line))
    html.append(help_line)
    html.append(signature_line)
    try:
        file_name = datetime.now().strftime(time_format) + '_skylines_c.msg'
        time_tag = datetime.now().strftime('%y/%m/%d %H:%M:%S')
        f = open(os.path.join(queue_dir, file_name), 'w')
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
        print(f'Queued email to {recip_str} {recip_adrr}')
    except BaseException as e:
        print(f'Queueing failed {recip_str} {subject}')
        print(e)
