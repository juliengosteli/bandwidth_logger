# Bandwidth Performance Logger

### Install requirements:

    $ pip install -r requirements.pip

### Usage:

    $ bandwidth_logger.py [-h] [-v] [-d] [-p]

### Optional arguments:

    -h, --help     show this help message and exit
    -v, --verbose  enable verbose output
    -d, --debug    enable debug output
    -p, --post     post data on API server

### Configuration file

Before submitting data, set the API endpoint corresponding
to the datastreams on the bandwidth.ini configuration file.
The API token should also be provided in this file. An example
is provided on bandwidth_logger.ini.example.
