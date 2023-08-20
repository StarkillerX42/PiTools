#!/usr/bin/env python3
import os
import socket
import click
import logging
import influxdb_client

from pathlib import Path
from influxdb_client.client.write_api import SYNCHRONOUS

from pitools.x86_hwinfo import get_ups


def get_token() -> tuple[str, str, str]:
    here = Path(__file__).absolute().parent
    token_path = here / f".{socket.gethostname()}.key"
    if not token_path.exists():
        logging.error(f"No token file at .{socket.gethostname()}.key")
    with token_path.open("r") as fil:
        host = fil.readline().rstrip("\n")
        org_id = fil.readline().rstrip("\n")
        token = fil.readline().rstrip("\n")
    return host, org_id, token


@click.command()
@click.option("-v", "--verbose", count=True)
def main(verbose: int = 0):
    if os.geteuid() != 0:
        raise PermissionError(
            "You need to have root privileges to run this script.\nPlease try"
            " again, this time using 'sudo'. Exiting."
        )

    host, org_id, token = get_token()
    client = influxdb_client.InfluxDBClient(url=host, token=token, org=org_id)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    ups = get_ups()
    for n, u in zip(("load", "capacity", "runtime"), ups):
        write_api.write(
            bucket="home",
            org=org_id,
            record=influxdb_client.Point("ups")
            .tag("device", socket.gethostname())
            .field(n, u),
        )


if __name__ == "__main__":
    main()

