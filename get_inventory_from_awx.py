#!/usr/bin/env python3

"""
Creates a local inventory file from an inventory in AWX
Usage:
python ../get_inventory_from_awx.py \
  --url https://awx.domain.com \
  -u admin \
  -p "topsecret" \
  "my-ec2-dev-inventory"
"""

import argparse
import sys
import requests

parser = argparse.ArgumentParser(
    description="Convert Ansible AWX Inventory to standard inventory"
)

parser.add_argument("--url", required=True, help="base url of AWX/Tower")
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("inventory", nargs=1, help="inventory name")

args = parser.parse_args()

all_inventories = requests.get(
    f"{args.url}/api/v2/inventories/", auth=(args.username, args.password)
)
inventory_id = -1
for inventory in all_inventories.json()["results"]:
    if inventory["name"] == args.inventory[0]:
        inventory_id = inventory["id"]
        break

if inventory_id == -1:
    print(f"Inventory {args.inventory[0]} not found ")
    sys.exit(1)

inventory_url = (
    f"{args.url}/api/v2/inventories/{inventory_id}"
    "/script/?hostvars=1&towervars=1&all=1"
)

inventory = requests.get(inventory_url, auth=(args.username, args.password))

hosts = inventory.json()
for key in sorted(hosts):
    if key == "all":
        continue
    if key == "_meta":
        continue
    if "hosts" in hosts[key]:
        print(f"[{key}]")
        for host in hosts[key]["hosts"]:
            print(host)
        print("")
    if "children" in hosts[key]:
        print("[{key}:children]")
        for child in hosts[key]["children"]:
            print(child)
        print("")
    if "vars" in hosts[key]:
        print("[{key}:vars]")
        for var in hosts[key]["vars"]:
            print("{var}={hosts[key]['vars'][var]}")
        print("")
    print("")

