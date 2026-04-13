Python scripts to compose email messages and send via postfix. 

queue_email can be used in a web app to send messages with custom text to users or in a mailmerge with .csv files

See the mailmerge example in `mail_example.py`

### Directory structure
Create directory `mail` somewhere
```
  mail
  ├── emails.log
  ├── queued
  └── sent
```
### mail_server.py
mail_server reads message files from `queued` and submits them to postfix which sends the emails and has its own queue and log and .

It enters a line in `emails.log`, and moves the message from `queued` to `sent`.

There is no checking to see if the email was sent by postfix.

There is no provision to receive emails.

### Mailing scripts and mailmerge example



### message file format for `queue_email` 
See example `merge_message.txt` in `mail_example`.
To make composing easier, leave out all html paragraph tags...they are added by `queue_email`.

```
<sender address>
<recipent address>
<subject>
<line1 that has any needed html tags except paragraph tags>
...
<line1 that has any needed needed html tags except paragraph tags>
```

### Message-generating scripts
#### email_scripts.py
Script `queue_email` creates message files.

```queue_email(sender_addr, recip_name, recip_adrr, subject, message_list, help_line='', signature_line='', id=None)```

### Mailmerge example



