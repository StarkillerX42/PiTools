#!/usr/bin/env python3
import datetime
import slack
import os
import starcoder42 as s

now = datetime.datetime.now()
print("IP Logger started at {}".format(now))

ip_path = os.path.join(os.path.dirname(__file__), "ip_archive.txt")
ip_archive = open(ip_path, "r")
my_ip = os.popen("curl -s ipecho.net/plain").read()
message = "Your Raspberry Pi's IP Address is: {}".format(my_ip)
lines = ip_archive.readlines()
is_there = bool(sum([my_ip in line for line in lines]))
# print(lines)
#print(is_there)
if not is_there: # Posts results to me if it changes on CUAC Research
    sc = slack.WebClient("xoxb-329888754887-33KgV85uLazdCKxGDI6Dx9eG")
    sc.chat_postMessage(channel="@dylan.gatlin", text=message)
# Writes values to the record
ip_archive.close()
ip_archive = open(ip_path, "a")
ip_archive.write("{}, {}\n".format(now, my_ip))
s.iprint(message, 1)
