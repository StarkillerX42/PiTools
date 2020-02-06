#!/usr/bin/env python3
from gpiozero import LED
import subprocess as sub
from time import sleep     # Import the sleep function from the time module
import datetime
import sys
import numpy as np
import starcoder42 as s

start = datetime.datetime.now()
print(f'Fan control started at {start}')

procs = sub.Popen("ps auxf", stdout=sub.PIPE, shell=True)
lines = np.array(procs.stdout.readlines())
is_alarm = np.array([("/fan.py" in str(proc))
                     for proc in lines])
to_kill = lines[is_alarm]

for proc in to_kill:
    parts = proc.split()
    pid = parts[1]
    dt = parts[9]
    m, sec = dt.split(b':')
    dt = datetime.timedelta(minutes=int(m), seconds=int(sec))
    if dt > datetime.timedelta(hours=23):
        sub.call(['kill', pid])

port = int(sys.argv[1])
threshhold = float(sys.argv[2])
fan = LED(port)

try:
    cond = True
    while cond: # Run forever
        temp = str(sub.Popen(['/opt/vc/bin/vcgencmd', 'measure_temp'],
                             stdout=sub.PIPE).stdout.read())
        temp = float(temp.split("=")[1].split("'")[0])
        if temp >threshhold:
            fan.on()
        else:
            fan.off()
        sleep(60)
        dt = datetime.datetime.now() - start
        cond = dt.seconds < 60*60*12
        s.iprint((dt.seconds, temp), 1)
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
