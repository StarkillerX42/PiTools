#!/usr/bin/env python3

import sys
import datetime
import argparse

import numpy as np
import subprocess as sub

from gpiozero import LED


# Prevent duplicate processes
procs = sub.Popen("ps auxf", stdout=sub.PIPE, shell=True)
lines = np.array(procs.stdout.readlines())
is_fan = np.array([("fan.py" in proc) for proc in lines])
to_kill = lines[is_fan]

for proc in to_kill:
    parts = proc.split()
    pid = parts[1]
    dt = parts[9]
    m, sec = dt.split(b":")
    dt = datetime.timedelta(minutes=int(m), seconds=int(sec))
    if dt > datetime.timedelta(hours=23):
        sub.call(["kill", pid])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, default=2)
    parser.add_argument("threshhold", type=float, default=60)
    parser.add_argument("-d", "--daytime", action="store_true")
    parser.add_argument("-v", "--verbose", action="count")

    args = parser.parse_args()

    return args


def main(args=None):
    if args is None:
        args = parse_args()
    if args.verbose:
        start = datetime.datetime.now()
        print(f"Fan control started at {start}")

    fan = LED(args.port)
    try:
        cond = True
        while cond:  # Run forever
            temp = get_temp.get_temp_float()
            fan_on = temp > args.threshhold
            now = dattime.datetime.now()
            fan_on = (
                fan_on and (now.hour > 7) and (now.hour < 20)
                if args.daytime
                else fan_on
            )
            if fan_on:
                fan.on()
            else:
                fan.off()

            sleep(60)
            dt = datetime.datetime.now() - start

    except KeyboardInterrupt:
        fan.off()
        sys.exit()


if __name__ == "__main__":
    main()

