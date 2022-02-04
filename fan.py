#!/usr/bin/env python3
from gpiozero import LED
import subprocess as sub
from time import sleep     # Import the sleep function from the time module
import datetime
import sys
import numpy as np
import starcoder42 as s
import argparse
import get_temp

start = datetime.datetime.now()
print(f'Fan control started at {start}')

procs = sub.Popen("ps auxf", stdout=sub.PIPE, shell=True)
lines = np.array(procs.stdout.readlines())
is_fan = np.array([("/fan.py" in str(proc))
                     for proc in lines])
to_kill = lines[is_fan]

for proc in to_kill:
    parts = proc.split()
    pid = parts[1]
    dt = parts[9]
    m, sec = dt.split(b':')
    dt = datetime.timedelta(minutes=int(m), seconds=int(sec))
    if dt > datetime.timedelta(hours=23):
        sub.call(['kill', pid])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, default=2)
    parser.add_argument("threshhold", type=float, default=60)

    args = parser.parse_args()

    return args

    
def main(args=None):
    if args is None:
        args = parse_args()
    
    fan = LED(args.port)
    print(dir(fan))
    try:
        cond = True
        while cond: # Run forever
            temp = get_temp.get_temp_float()
            if temp > args.threshhold:
                fan.on()
            else:
                fan.off()
            sleep(60)
            dt = datetime.datetime.now() - start
            cond = dt.seconds < 60*60*12
            s.iprint((dt.seconds, temp), 1)

    except KeyboardInterrupt:
        fan.off()
        sys.exit()


if __name__ == "__main__":
    main()

