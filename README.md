# SMS Backup+ Backup

## Background

There is an outstanding open source application for Android devices called [SMS Backup+](https://github.com/jberkel/sms-backup-plus) (by Jan Berkel) that will automatically upload your SMS (and MMS) to an IMAP server, such as Gmail.

In addition to having a copy saved online, I also want to be able to have a nicely formatted local copy of my messages (text files, pictures...). That's where this software comes in...

## Purpose

This software allows you to save the messages that were backed up to Gmail by SMS Backup+ as nicely formatted text files on your computer, including an MMS pictures and videos you received.

## Usage

Go to the Gmail website to [download an archive of your messages](https://takeout.google.com/settings/takeout). Be sure to only select the message that were uploaded by SMS Backup+ and that you want saved.

Extract the mbox file from the download, and send it to the function provided in this software.

See the Python docstring for more information on usage.

## Example output

The filenames created will look like this:

    20160921-IMG_8904.jpg
    20160921-IMG_8907.jpg
    20161003-497209663.jpg
    20161004-2f033013c.gif
    20161008-IMG_9290.3gp
    sms-201609-20170224.txt
    sms-201610-20170224.txt
    sms-201611-20170224.txt
    sms-201612-20170224.txt
    sms-201701-20170224.txt
    sms-201702-20170224.txt

And the text files will be formatted like this:

    John (2017-02-05 13:56:27): We are driving to Disneyland right now.
    John (2017-02-05 13:57:15): [IMG_0411.3gp]
    John (2017-02-05 13:58:06): [508013861.jpg]
    Tony (2017-02-05 14:09:47): Oh my gosh!!! It was a surprise to me too! Lol 😄

