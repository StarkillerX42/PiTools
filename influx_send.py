#!/usr/bin/env python3
import socket
import click
import logging
import influxdb_client

from pathlib import Path
from influxdb_client.client.write_api import SYNCHRONOUS

from pitools.hw import get_temp, get_ip, get_cpu, get_mem


def get_token() -> tuple[str]:
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
    logging.basicConfig(
        filename=Path.home() / ".cache/log/influx_archiver/influx_archive.log",
        encoding="utf-8",
    )
    host, org_id, token = get_token()
    client = influxdb_client.InfluxDBClient(url=host, token=token, org=org_id)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Write temp
    write_api.write(
        bucket="home",
        org=org_id,
        record=influxdb_client.Point("temperature")
        .tag("device", socket.gethostname())
        .field("cpu_temp", get_temp()),
    )

    # CPU/RAM
    # Write temp
    cpu_usage = get_cpu()
    names = ("user", "nice", "system", "total")
    for n, u in zip(names, cpu_usage):
        write_api.write(
            bucket="home",
            org=org_id,
            record=influxdb_client.Point("cpu")
            .tag("device", socket.gethostname())
            .field(n, u),
        )
    ram = get_mem()
    names = ("memory_used", "memory_total", "swap_used", "swap_total")
    for n, u in zip(names, ram):
        write_api.write(
            bucket="home",
            org=org_id,
            record=influxdb_client.Point("memory")
            .tag("device", socket.gethostname())
            .field(n, u),
        )

    # IP address
    if socket.gethostname() == "cherrypi":
        write_api.write(
            bucket="home",
            org=org_id,
            record=influxdb_client.Point("ip_address")
            .tag("device", socket.gethostname())
            .field("ip_address", get_ip()),
        )

    return 0


if __name__ == "__main__":
    main()
