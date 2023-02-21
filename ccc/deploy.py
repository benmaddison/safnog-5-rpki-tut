#!/usr/bin/env python3
"""Config deployment script."""

import argparse
import multiprocessing
import os
import sys
import time

import jinja2
import napalm
import yaml

PARAMS = {"username": "root", "password": "safnog"}


def main():
    """Run dployment."""
    args = parse_args()
    inventory = read_inventory(args.policy)
    time.sleep(args.delay)
    with multiprocessing.Pool(len(inventory)) as pool:
        pool.map(deploy, inventory)
    try:
        while args.wait:
            time.sleep(1)
    except KeyboardInterrupt:
        print("ctrl-c caught. exiting...")
    return


def parse_args():
    """Parse command line args."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wait", action="store_true",
                        help="wait for ctrl-c instead of exiting immediately")
    parser.add_argument("-d", "--delay", type=int, default=0,
                        help="delay startup to ensure devices are ready")
    parser.add_argument("-p", "--policy", choices=("none", "report", "enforce"),  # noqa
                        help="rpki-ov policy to deploy",
                        default="none")
    args = parser.parse_args()
    return args


def read_inventory(policy):
    """Read inventory data from file."""
    inventory_path = os.path.join(os.path.dirname(__file__), "inventory.yml")
    with open(inventory_path) as f:
        data = yaml.safe_load(f)
    inventory = [{"my": i,
                  "other": [j for j in data if j["name"] != i["name"]],
                  "policy": policy} for i in data]
    return inventory


def deploy(context):
    """Render config and deploy."""
    driver = napalm.get_network_driver(context["my"]["vendor"])
    candidate = render(context)
    try:
        with driver(hostname=context["my"]["name"], **PARAMS) as device:
            device.load_replace_candidate(config=candidate)
            diff = device.compare_config()
            print("Diff for {}:\n{}".format(context["my"]["name"], diff))
            device.commit_config()
    except Exception as e:
        print("Error while deploying config to {}:\n{}".format(context["my"]["name"],  # noqa
                                                               candidate))
        raise e
    print("Changes committed to {}".format(context["my"]["name"]))
    return


def render(context):
    """Render the device config."""
    loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),
                                                  "templates"))
    env = jinja2.Environment(loader=loader)
    template = env.get_template("{}.j2".format(context["my"]["vendor"]))
    config = template.render(**context)
    return config


if __name__ == "__main__":
    sys.exit(main())
