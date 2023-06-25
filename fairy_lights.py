#!/usr/bin/env python3
from gpiozero import LED
import subprocess as sub
from time import sleep  # Import the sleep function from the time module
import datetime
import sys
import numpy as np


procs = sub.run(["ps", "auxf"], stdout=sub.PIPE, shell=True, encoding="utf-8")
lines = np.array(procs.stdout.readlines())
is_fairy = np.array([("/fairy_lights.py" in str(proc)) for proc in lines])
to_kill = lines[is_fairy]

for proc in to_kill:
    parts = proc.split()
    pid = parts[1]
    dt = parts[9]
    m, sec = dt.split(b":")
    dt = datetime.timedelta(minutes=int(m), seconds=int(sec))
    if dt > datetime.timedelta(hours=23):
        sub.call(["kill", pid])


def main():
    start = datetime.datetime.now()
    print(f"Fairy Lights control started at {start}")
    port = int(sys.argv[1])
    lights = LED(port)
    lights.on()
    while True:
        sleep(500)


class Lights:
    def __init__(self, port):
        self.port = port
        self.controller = LED(self.port)

    def on(self):
        self.controller.on()
        return

    def off(self):
        self.controller.off()
        return


if __name__ == "__main__":
    main()
