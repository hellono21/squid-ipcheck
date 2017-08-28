#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, logging, argparse, time
import redis

__version__ = '0.1.0'

LOGGING_FORMAT = '%(asctime)s - pid[%(process)d] - %(levelname)5s - %(name)s: %(message)s'
LOGGING_LEVEL = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

class IPCheckACL(object):
    def __init__(self, host='db', port=6379, prefix='squid:', ttl=3600):
        super(IPCheckACL, self).__init__()
        self.host = host
        self.port = port
        self.prefix = prefix
        self.ttl = ttl
        self.logger = logging.getLogger(self.__class__.__name__)

        try:
            self.redis = redis.StrictRedis(host = self.host, port = self.port)
            self.redis.ping()
        except Exception, e:
            self.logger.error(e)
            raise e
    pass

    def run(self):
        while True:
            line = sys.stdin.readline()
            line = line.strip()
            self.logger.debug('squid >> %s' % line)

            # parse the input line
            try:
                inputs = line.split(' ', 2)
                srcIP = inputs[0]
                uri = inputs[1]
            except Exception, e:
                self.logger.warning('get a unresolved line from squid [%s]' % line)
                sys.stdout.write('BH message="get a unresolved line from squid"\n')
                sys.stdout.flush()
                continue
            
            key = self.prefix + srcIP
            try:
                if None == self.redis.get(key):
                    self.logger.info('ip %s is not valid' % srcIP)
                    sys.stdout.write('ERR message="ip %s is not valid"\n' % srcIP)
                    sys.stdout.flush()
                else:
                    self.logger.info('ip %s is valid' % srcIP)
                    sys.stdout.write('OK\n')
                    sys.stdout.flush()

            except Exception, e:
                self.logger.error(e)
                raise e
    pass

def main():
    # setup logging config
    logfile = '/tmp/ipcheck.log'
    loglevel = LOGGING_LEVEL['INFO']
    logging.basicConfig(level = loglevel, filename = logfile, format = LOGGING_FORMAT)

    ipCheckACL = IPCheckACL()
    ipCheckACL.run()
    pass

if __name__ == '__main__':
    main()
