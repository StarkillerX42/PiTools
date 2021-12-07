#!/usr/bin/env python3
"""A tool for grabbing your router's external IP address.
This is best run as a daily cronjob with a slack bot to send the values to,
make sure to specify sys.argv[1] as the slack key file and sys.argv[2] as the
recipient on slack
"""
import datetime
import slack
import starcoder42 as s
from pathlib import Path
import subprocess as sub
import sys

now = datetime.datetime.now()
print("IP Logger started at {}".format(now))

ip_path = (Path(__file__).parent / "ip_archive.txt").absolute()
my_ip = sub.Popen('dig +short myip.opendns.com @resolver1.opendns.com',
                  shell=True, stdout=sub.PIPE).stdout.read().decode(
    'utf-8').strip('\n')
message = "Your Raspberry Pi's IP Address is: {}".format(my_ip)
s.iprint(message, 1)

# Now that we have it, we'll save it
if not ip_path.exists():
    ip_path.touch()
else:
    ip_archive = ip_path.open('r')
    lines = ip_archive.readlines()
    is_there = bool(sum([my_ip in line for line in lines]))
    ip_archive.close()

    has_argv = False
    try:
        sys.argv[1]
        sys.argv[2]
        has_argv = True
    except IndexError as e:
        s.iprint(e, 1)
        s.iprint('No arguments given', 1)
    if (not is_there) and has_argv:  # Posts results to me
        print('Sending IP to {}'.format(sys.argv[1]))

        key = (Path(__file__).parent / sys.argv[1]
                ).open('r').readline().strip('\n')
        sc = slack.WebClient(key)
        sc.chat_postMessage(channel=sys.argv[2], text=message)

# Writes values to the record
ip_archive = ip_path.open('a')
ip_archive.write("{}, {}\n".format(now, my_ip))

