#!/usr/bin/env python3

# smsbackupbackup
# David Couzelis, 2017

import datetime
import mailbox
import sys

def run(mbox_filename, my_name, my_descriptor_list, friend_name, friend_descriptor_list):
    """Read an mbox mailbox made from a downloaded archive of SMS Backup+ messages and
    save them to local text files. Any MMS pictures or videos that are received (but
    not those that you sent) will be saved as well.

    mbox_files             : The filename of an mbox mailbox archive
    my_name                : A string containing your name
    my_descriptor_list     : A list of strings that are something in the 'From' field
                             of the downloaded email denoting you (your name, phone
                             number...)
    friend_name            : A string containing the name of your contact
    friend_descriptor_list : A list of strings, likewise, for the contact

    The messages and media will be formatted nicely and saved in text documents
    by year + month.
    """

    try:
        mbox = mailbox.mbox(mbox_filename, create=False)
    except:
        print('Failed to load mbox file: ' + mbox_filename, file=sys.stderr)
        exit(1)
    
    # A timestamp (YYYYMMDD), to be used as a suffix specifying when the output files were created
    timestamp_str = datetime.datetime.now().strftime('%Y%m%d')
    
    # Use the message 'Sent' date to sort the messages
    messages = dict()
    for key in mbox.keys():
        datetime_str = datetime.datetime.strptime(mbox[key]['Date'], '%a, %d %b %Y %H:%M:%S %z')
        messages[datetime_str] = mbox[key]

    attachment_count = 100
    
    for datetime_str in sorted(messages):
    
        from_me = True
    
        message = messages[datetime_str]
        sms_str = str()
    
        # Begin the line of output with who sent the message...
        if any(x in message['From'] for x in friend_descriptor_list) and any(x in message['To'] for x in my_descriptor_list):
            # This message was sent by the friend
            sms_str += friend_name + ' '
            from_me = False
        elif any(x in message['From'] for x in my_descriptor_list) and any(x in message['To'] for x in friend_descriptor_list):
            # This message was sent by me
            sms_str += my_name + ' '
        else:
            # I have no clue who sent this message!
            print('WARNING: Unknown sender: ' + message['From'], file=sys.stderr)
            # Skip it
            continue
    
        # ...Next, add a timestamp to the message...
        sms_str += datetime_str.strftime('(%Y-%m-%d %H:%M:%S): ')
    
        # ...Finally, add the actual content of the message...
        if not message.is_multipart():
            # (Get rid of that silly '\r' that is used by Windows)
            sms_str += message.get_payload(decode=True).decode('utf-8').strip().replace('\r', '')
        else:
            # ...Unless it was an MMS!
            for part in message.walk():
                # ...Save any attachments...
                if part.get_content_disposition() == 'attachment':
                    # (...as long as they're not from me, I already have a copy!...)
                    if not from_me:
                        sms_str += '[' + part.get_filename() + '] '
                        filename = datetime_str.strftime('%Y%m%d') + '-' + str(attachment_count) + '-' + part.get_filename()
                        with open(filename, 'wb') as attachment_file:
                            attachment_file.write(part.get_payload(decode=True))
                        attachment_count += 1
                elif part.get_content_type() == 'text/plain':
                    # ...And save any other text that was included in the message, too...
                    sms_str += part.get_payload(decode=True).decode('utf-8').strip().replace('\r', '')
                else:
                    if part.get_content_type() != 'multipart/mixed':
                        print('WARNING: Unknown type: ' + part.get_content_type(), file=sys.stderr)
    
        # Finally, write (or append) the message to a dated file
        sms_filename = 'sms-' + datetime_str.strftime('%Y%m') + '-' + timestamp_str + '.txt'
        with open(sms_filename, 'a') as yearmonth_file:
            yearmonth_file.write(sms_str.strip() + '\n')

if __name__ == '__main__':
    message = """
    SMS Backup+ Backup ("smsbackupbackup")
    David Couzelis, 2017
    
    This file is meant to be used as a library.

    Example:

        #!/usr/bin/env python3
        import smsbackupbackup
        import sys
        smsbackupbackup.run(sys.argv[1], 'John', ['johnemailname', '4565552324'], 'Tony', ['Tony', 'abcmail'])

    Please see the README.md or docstring for more information.
    """
    print(message, file=sys.stderr)
    exit(1)
