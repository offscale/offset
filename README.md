offset
======
[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech)
![Python version range](https://img.shields.io/badge/python-2.7%20|%203.4%20|%203.5%20|%203.6%20|%203.7%20|%203.8-blue.svg)
[![License](https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Offset is the offscale tool for setting values (e.g.: nodes). Currently just used for manually settings nodes, which can then be used by `offregister`.

## Install dependencies

    pip install -r requirements.txt

## Install package

    pip install .

## Usage

    usage: python -m offset [-h] (-p PASSWORD | -i IDENTITY_FILE) --dns-name HOSTNAME
                            -u USERNAME [-n NAME] [--version] [--etcd ETCD]
                            [--purpose PURPOSE]
    
    Offset CLI. Set nodes manually.
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PASSWORD, --password PASSWORD
                            Password for login
      -i IDENTITY_FILE, --identity-file IDENTITY_FILE
                            pem file for login
      --dns-name HOSTNAME, --ip HOSTNAME
                            Location of node
      -u USERNAME, --user USERNAME
                            Login username
      -n NAME, --name NAME  Name for node. Used for bookkeeping, and other
                            packages may set the hostname to this.
      --version             show program's version number and exit
      --etcd ETCD           Server location [127.0.0.1:4001]
      --purpose PURPOSE, --cluster PURPOSE
                            Purpose of the node. Groups all together
                            (hierarchically). Defaults to: 'unclustered'

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.
