# /usr/bin/python
import argparse
import json
import logging
import requests
import speedtest_cli

from ast import literal_eval
from ConfigParser import SafeConfigParser

TEST_SERVERS = {
    'wom': '7631',
    'entel': '1858',
    'movistar': '939'
}


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose output')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug output')
    parser.add_argument('-p', '--post', action='store_true',
                        help='post data on API server')
    args = parser.parse_args()

    # Logging configuration
    logging_level = logging.DEBUG if args.debug else logging.INFO
    if not args.verbose:
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s %(levelname)s: %(message)s.',
            filename='./log/bandwidth-logger.log',
        )
    else:
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s %(levelname)s: %(message)s.'
        )
    logging.getLogger('requests').setLevel(logging.WARNING)

    verbose = True if args.verbose else False

    results = speedtest_cli.speedtest(
        server=TEST_SERVERS['movistar'], verbose=verbose)

    if args.post:
        config = SafeConfigParser()
        config.read('./bandwidth_logger.ini')
        api_url = config.get('server', 'api_url')
        api_token = config.get('server', 'api_token')
        device_id = config.get('device', 'device_id')
        device_url = '%s/devices/%s/' % (api_url, device_id)
        datastreams = literal_eval(config.get('device', 'datastreams'))
        api_hdrs = {'Content-Type': 'application/json',
                    'Authorization': 'Token token="%s"' % api_token}
        datastream_ids = [ds['id'] for ds in datastreams]
        logging.debug("Results: {}".format(results))
        payload = {'values': dict(zip(datastream_ids, results))}
        logging.debug(payload)
        try:
            r = requests.post(device_url, data=json.dumps(payload),
                              headers=api_hdrs)
        except requests.ConnectionError:
            logging.error('Connection error. Values were not logged')
        else:
            logging.debug('Values registered on server')
