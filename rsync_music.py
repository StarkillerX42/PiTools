#!/usr/bin/env python3
import json
import argparse
import copy
import subprocess as sub
from pathlib import Path
from astropy.time import Time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="Passed on to rsync for testing")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose printing, also passed to rsync")
    return parser.parse_args()


def main(args=parse_args()):
    t_start = Time.now()
    print(f"Starting RSync Music at {t_start.isot}")
    here = Path(__file__).absolute().parent
    config_path = here / "to_sync.json"

    config = json.load(config_path.open('r'))
    outfig = copy.deepcopy(config)

    source_flac_path = config["source_flac_path"]
    destination_flac_path = config["destination_flac_path"]
    dest_machine = config["destination_machine"]
    if config["last_sync"] == t_start.isot[:10]:
        raise ValueError("Last sync was today, not syncing")

    try:
        x = sub.check_output(f'ping -c 1 "{dest_machine.strip("pi@")}"',
                             shell=True).decode("utf-8")
    except sub.CalledProcessError:
        x = ""

    # print(x)
    if "0% packet loss" not in x:
        raise Exception(f"Remote host {dest_machine} not found")

    for src in config["unsynced_paths"]:
        if ((Time.now() - t_start) * 24).value > 5:
            print("Ran out of time")
            outfig["last_sync"] = Time.now().isot[:10]
            if not args.dry_run:
                json.dump(outfig, config_path.open('w'))
            exit()

        source = Path(src)
        suffix_path = source.relative_to(source_flac_path)
        print(f"Starting {suffix_path}")

        if not source.is_dir():
            print(f"    Removing {source}, not a directory")
            outfig["unsynced_paths"].remove(src)
            if not args.dry_run:
                with config_path.open('w') as fil:
                    json.dump(outfig, fil)
            continue

        rargs = "n" if args.dry_run else ""

        rargs += "v" if args.verbose else  ""
        dest = (destination_flac_path / suffix_path).as_posix().replace(
                " ", "\\ ")
        cmd = (f'rsync -Pa{rargs}zh --ignore-existing "{source.as_posix()}/"'
               f' "{dest_machine}'
               f':{dest}/"')
        try:
            if args.verbose:
                print(cmd)
            cmd_output = sub.run(cmd, shell=True, check=False, capture_output=True)
            if args.verbose:
                print("stdout: ", cmd_output.stdout.decode("utf-8"))
                if cmd_output.stderr:
                    print("stderr: ", cmd_output.stderr.decode("utf-8"))
            
            if cmd_output.returncode == 0:
                print(f"    Completed {suffix_path}")
                outfig["unsynced_paths"].remove(src)
                if not args.dry_run:
                    with config_path.open('w') as fil:
                        json.dump(outfig, fil)
        # Originally I thought this could be used if the path
        # isn't found, but this only came up when shell=True
        # wasn't used in sub.run (ie. rsync is not found as a
        # file
        # except FileNotFoundError as e:
        #     print("    FileNotFoundError {e}")
        #     outfig["unsynced_paths"].remove(src)
        #     if not args.dry_run:
        #         with config_path.open('w') as fil:
        #             json.dump(outfig, fil)
        #     continue
        except Exception as e:
            print(f"    Failed: {e}")
            continue

    outfig["last_sync"] = Time.now().isot[:10]
    if not args.dry_run:
        json.dump(outfig, config_path.open('w'))


if __name__ == "__main__":
    main()

