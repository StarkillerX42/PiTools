import json
import argparse
import subprocess as sub
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Passed on to rsync for testing")
    return parser.parse_args()


def main(args=parse_args()):
    here = Path(__file__).absolute().parent
    config_path = here / "to_sync.json"
    
    config = json.load(config_path.open('r'))
    
    source_flac_path = config["source_flac_path"]
    destination_flac_path = config["destination_flac_path"]
    dest_machine = config["destination_machine"]

    if sub.run(["ping", "-c", "1", dest_machine]).returncode != 0:
        raise Exception(f"Remote host {dest_machine} not found")

    for source in config["unsynced_paths"]:
        if not source.is_dir():
            print(f"    Removing {source}, not a directory")
            config["unsynced_paths"].remove(source)
            json.dump(config, config_path.open('w'))
            continue

        source = Path(source)
        suffix_path = source.relative_to(source_flac_path)
        kwargs = " --dry-run" if args.dry_run else ""
        cmd = (f'rsync -Pavzh --ignore-existing{kwargs} "{source.as_posix()}/"'
               f' "{dest_machine}'
               f':{destination_flac_path / suffix_path}/"')
        try:
            print(cmd)
            cmd_output = sub.run(cmd, check=False, capture_output=True)
            # print(cmd_output.stdout)
            if cmd_output.returncode == 0:
                print(f"    Completed {suffix_path}")
                config["unsynced_paths"].remove(source)
                json.dump(config,config_path.open('w'))

        except FileNotFoundError as e:
            print("    Removing {source}, path not found")
            config["unsynced_paths"].remove(source)
            json.dump(config,config_path.open('w'))
            continue


if __name__ == "__main__":
    main()

