
### Directory structure
Create directory `mail` somewhere
```
  mail
  ├── emails.log
  ├── queued
  └── sent
```
### mail_server.py
mail_server reads message files from `queue` and submits them to posfix, which has its own queue and log and sends the emails.

It enters a line in `emails.log`, and moves the message from `queued` to `sent`.

There is no checking to see if the email was sent by postfix.

### Message file format
```
<sender address>
<recipent address>
<subject>
<html line 1>
...
<html line n>
```

### Message-generating scripts
#### email_scripts.py
Script `queue_email` creates message files.

```queue_email(sender_addr, recip_name, recip_adrr, subject, message_list, help_line='', signature_line='', id=None)```

### Mailmerge example



