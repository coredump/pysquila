#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from datetime import datetime
from pymongo import Connection
from pysquila_agent import LOG

class Agent(object):

    def __init__(self, host = None, dbname = None, log = None, debug = 0):
        self.host = host
        self.log = log
        self.dbname = dbname
        self.log = LOG
        self.debug = int(debug)

    def get_collection(self):
        """
        Returns a collection object to insert data
        """
        try:
            if self.debug: self.log.debug("Connecting to %s", self.host)
            conn = Connection(self.host)
            db = conn[self.dbname]
            logs = db.logs
        except Exception, e:
            print >> sys.stderr, e
            sys.exit(120)
        return logs
        
    def get_time(self, timestamp):
        return (datetime.utcfromtimestamp(timestamp))

    def process_log(self):
        """
        Opens the log and does the hard work
        """
        # if there's already data, try to find the date of the last object
        logs = self.get_collection()
        over_last_date = False

        if logs.count() > 0:
            last_time = logs.find_one(limit=1, sort=[('_id', -1)])['t']
            timestamp_last_time = time.mktime(last_time.timetuple())
        else:
            over_last_date = True

        try:
            log = open(self.log)
            for line in log:
                timestamp, duration, client_address, result, size, \
                     method, url, ident, hier, content_type = line.split()

                if not over_last_date:
                    if float(timestamp) <= timestamp_last_time:
                        continue
                    else:
                        over_last_date = True

                doc = {'t': self.get_time(float(timestamp)),
                       'd' : int(duration),
                       'c': client_address,
                       'r': result,
                       's': int(size),
                       'm': method,
                       'u': url.split('?')[0],
                       'i': ident,
                       'h': hier,
                       'o': content_type,
                      }

                logs.insert(doc, safe=True)
        
        except Exception, e:
            print >> sys.stderr, e
            sys.exit(120)
