#!/usr/bin/env python


import sys
import os
from yaml import safe_load
from netmiko import Netmiko, file_transfer


def main(argv):

    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    platform_map = {"ios": "cisco_ios", "iosxr": "cisco_xr"}

    for host in host_root["host_list"]:
        platform = platform_map[host["platform"]]

        conn = Netmiko(
            host=host["name"],
            username="developer",
            password="C1sco12345",
            device_type=platform,
            port=22,
        )

        print(f" Uploading {argv[1]}")

        result = file_transfer(
            conn,
            source_file=argv[1],
            dest_file=argv[1],
            file_system=host.get("file_system"),
        )
        print(f" Details: {result}\n")

        conn.disconnect()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} <file_to_upload>")
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]):
        print(f"error: file {sys.argv[1]} not found")
        sys.exit(2)
    main(sys.argv)
