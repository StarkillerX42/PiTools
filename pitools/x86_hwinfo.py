#!/usr/bin/env python3
import regex as re
import subprocess as sub


def get_ups() -> tuple:
    loadRE = re.compile(r"(?<=Load\.+ \d+\s*Watt\()\d+")
    capRE = re.compile(r"(?<=Battery Capacity\.+\s*)\d+")
    runRE = re.compile(r"(?<=Remaining Runtime\.+\s*)\d+")
    ret = sub.run(
        ["pwrstat -status"],
        stdout=sub.PIPE,
        stderr=sub.PIPE,
        encoding="utf-8",
        shell=True,
    )
    assert ret.stderr == ""
    load = loadRE.search(ret.stdout)
    if load is not None:
        load = int(load.group())
    cap = capRE.search(ret.stdout)
    if cap is not None:
        cap = int(cap.group())
    run = runRE.search(ret.stdout)
    if run is not None:
        run = int(run.group())

    return (load, cap, run)


def main():
    print("get_ups")
    print(get_ups())
