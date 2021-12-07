#!/usr/bin/env python3
import subprocess as sub
from astropy.time import Time
from pathlib import Path

import starcoder42 as s

x = sub.check_output("sensors").decode("utf-8")
for line in x.splitlines():
    if "temp" in line:
        temp = line.split()[1][1:]
s.iprint(f"The temperature is {temp}", 1)
here = Path(__file__).parent
log = here / "temp_log.txt"
with log.open('a') as fil:
    fil.write(f"{Time.now().iso},{temp[:-2]:>6}\n")

