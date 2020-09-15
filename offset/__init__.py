#!/usr/bin/env python

import yaml
import logging

from json import load, dumps
from sys import modules
from os import path
from logging.config import dictConfig as _dictConfig
from pkg_resources import resource_filename

from etcd import Client

__author__ = "Samuel Marks"
__version__ = "0.0.1"


def get_logger(name=None):
    with open(path.join(path.dirname(__file__), "_data", "logging.yml"), "rt") as f:
        data = yaml.load(f)
    _dictConfig(data)
    return logging.getLogger(name=name)


root_logger = get_logger()


def set_node(username, password, identity_file, hostname, etcd, name, purpose):
    with open(
        path.join(
            path.dirname(
                resource_filename(modules[__name__].__package__, "__init__.py")
            ),
            "_config",
            "new_node.json",
        )
    ) as f:
        d = load(f)

    d["name"] = d["uuid"] = d["id"] = d["extra"]["ssh_config"]["Host"] = name
    d["public_ips"] = d["private_ips"] = d["extra"]["ssh_config"]["HostName"] = [
        hostname
    ]
    d["extra"]["user"] = d["extra"]["ssh_config"]["User"] = username
    d["extra"]["user_hostname_port"] = "{user}@{hostname}:22".format(
        user=username, hostname=hostname
    )
    if identity_file:
        d["extra"]["ssh_config"]["IdentityFile"] = identity_file
    if password:
        d["extra"]["ssh_config"]["PasswordAuthentication"] = "yes"
        d["extra"]["password"] = password
        if not identity_file:
            d["extra"]["no_key_filename"] = True

    key = "{purpose}/{name}".format(purpose=purpose, name=name)
    host, port = etcd.split(":")
    Client(host=host, port=int(port)).set(key, dumps(d, indent=4))

    root_logger.info("Set: {key}".format(key=key))
