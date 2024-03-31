# -*- coding: utf-8 -*-

"""
SDK interface for `offset`
"""

import logging
from json import dumps, load
from logging.config import dictConfig as _dictConfig
from operator import methodcaller
from os import path
from sys import modules, version

import etcd3
import yaml
from pkg_resources import resource_filename

__author__ = "Samuel Marks"
__version__ = "0.0.3-beta"
__description__ = "Offset is the offscale tool for setting values (e.g.: nodes). Currently just used for manually settings nodes, which can then be used by `offregister`."


if version[0] == "2":
    to_bytes = methodcaller("encode")
else:
    to_bytes = methodcaller("encode", "utf8")


def get_logger(name=None):
    """
    Create logger—with optional name—with the logging.yml config

    :param name: Optional name of logger
    :type name: ```Optional[str]```

    :return: instanceof Logger
    :rtype: ```Logger```
    """
    with open(path.join(path.dirname(__file__), "_data", "logging.yml"), "rt") as f:
        data = yaml.safe_load(f)
    _dictConfig(data)
    return logging.getLogger(name=name)


root_logger = get_logger()


def set_node(username, password, os, identity_file, hostname, etcd, name, purpose):
    """
    Set the node (str->JSON mapping saved in etcd)

    :param username: Username (to login to instance)
    :type username: ```Optional[str]```

    :param password: Password (to login to instance)
    :type password: ```Optional[str]```

    :param os: Operating System to store in `extra.os` property of LibCloud's `Node`. If unspecified OS is inferred from `--user`.
    :type os: ```Optional[str]```

    :param identity_file: Identity file (to login to instance)
    :type identity_file: ```Optional[str]```

    :param hostname: Hostname of instance (e.g., public IP address, public DNS name)
    :type hostname: ```str```

    :param etcd: "host:port" connection string for etcd
    :type etcd: ```str```

    :param name: name of node (etcd key becomes "${name}/${purpose}")
    :type name: ```str```

    :param purpose: purpose of node (etcd key becomes "${name}/${purpose}")
    :type purpose: ```str```
    """
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

    if purpose is None:
        raise TypeError("purpose must be set")
    elif name is None:
        raise TypeError("name must be set")

    if os:
        d["extra"]["os"] = os

    key = "{purpose}/{name}".format(purpose=purpose, name=name)
    host, port = etcd.split(":")
    etcd3.client(host=host, port=int(port)).put(key, to_bytes(dumps(d, indent=4)))

    root_logger.info("Set: {key}".format(key=key))


__all__ = ["set_node", "__version__"]
