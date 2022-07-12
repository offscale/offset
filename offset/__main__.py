#!/usr/bin/env python
"""
Command-line interface to `offset`
"""

from argparse import ArgumentParser
from sys import modules

from offset import __version__, set_node


def _build_parser(parser):
    """
    Parser builder

    :param parser: instanceof ArgumentParser
    :type parser: ```ArgumentParser```

    :return: instanceof ArgumentParser
    :rtype: ```ArgumentParser```
    """
    parser.add_argument("-p", "--password", help="Password for login")
    parser.add_argument("-i", "--identity-file", help="pem file for login")

    parser.add_argument(
        "--dns-name", "--ip", dest="hostname", help="Location of node", required=True
    )
    parser.add_argument(
        "-u", "--user", help="Login username", dest="username", required=True
    )
    parser.add_argument(
        "--os",
        help="Operating System to store in `extra.os` property of LibCloud's `Node`. If unspecified OS is inferred from `--user`.",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Name for node. Used for bookkeeping, and other packages may set the hostname to this.",
        required=True,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="{} {}".format(modules[__name__].__package__, __version__),
    )
    parser.add_argument(
        "--etcd", help="Server location\t[127.0.0.1:2379]", default="127.0.0.1:2379"
    )
    parser.add_argument(
        "--purpose",
        "--cluster",
        dest="purpose",
        help="Purpose of the node. Groups all together (hierarchically). Defaults to: 'unclustered'",
        default="unclustered",
    )
    return parser


if __name__ == "__main__":
    pa = ArgumentParser(description="Offset CLI. Set nodes manually.")
    args = _build_parser(pa).parse_args()

    if args.password is None and args.identity_file is None:
        pa.error("at least one of --identity-file and --password required")
    set_node(**dict(args._get_kwargs()))
