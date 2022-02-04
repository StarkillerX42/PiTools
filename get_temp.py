#!/usr/bin/env python3
import subprocess as sub
from astropy.time import Time
from pathlib import Path

import starcoder42 as s


def get_temp():

    try:
        x = sub.check_output("sensors").decode("utf-8")
        for line in x.splitlines():
            if "temp" in line:
                temp = line.split()[1][1:]
    except FileNotFoundError:
        ubuntu_temp = Path("/sys/class/thermal/thermal_zone0/temp")
        with ubuntu_temp.open('r') as fil:
            temp = "{:.1f}\N{DEGREE SIGN}C".format(float(fil.readline()) / 1000)
    return temp


def get_temp_float():
    temp = get_temp()
    temp = float(temp.split('\N{DEGREE SIGN}')[0])
    return temp


def main():
    temp = get_temp()
    s.iprint(f"The temperature is {temp}", 1)
    here = Path(__file__).parent
    log = here / "temp_log.txt"
    with log.open('a') as fil:
        fil.write(f"{Time.now().iso},{temp[:-2]:>6}\n")


if __name__ == "__main__":
    main()

