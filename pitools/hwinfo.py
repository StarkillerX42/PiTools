#!/usr/bin/env python3
import regex as re
import subprocess as sub
import numpy as np


def get_temp() -> float | None:
    cpu_temp_re = re.compile(r"(?<=temp\d*:\s+\+)[\d\.]+")
    sensors = sub.run(["sensors"], capture_output=True, encoding="utf-8")
    cpu_temps = cpu_temp_re.findall(sensors.stdout)
    if len(cpu_temps) > 0:
        return float(cpu_temps[0])
    else:
        return None


def get_ip() -> str | None:
    ipCmd = sub.run(
        ["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"],
        capture_output=True,
        encoding="utf-8",
    )
    ip = ipCmd.stdout.rstrip("\n")
    if ip == "":
        return None
    else:
        return ip


def get_cpu() -> tuple[int]:
    """
    Returns:
        tuple(int): The ratio of user, nice user, system, and total CPU usage
            between 0 and 1.
    """
    with open("/proc/stat", "r") as fil:
        stats = fil.read()
    cpu_stats = re.findall(r"(?<=cpu )[\d ]+", stats)[0].split()
    usage = cpu_stats[:4]
    for i in range(len(usage)):
        usage[i] = int(usage[i])
    tot = np.sum(usage)

    return usage[0] / tot, usage[1] / tot, usage[2] / tot, np.sum(usage[:3]) / tot


def get_mem() -> list[int]:
    free = sub.run(["free"], capture_output=True, encoding="utf-8")
    ret = []
    for line in free.stdout.splitlines():
        if "Mem:" in line or "Swap:" in line:
            ret.append(int(line.split()[2]))
            ret.append(int(line.split()[1]))

    return ret


def main():
    print("get_temp")
    print(get_temp())
    print("get_ip")
    print(get_ip())
    print("get_cpu")
    print(get_cpu())
    print("get_mem")
    print(get_mem())


if __name__  == "__main__":
    main()