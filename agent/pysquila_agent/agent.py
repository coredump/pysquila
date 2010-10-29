#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from pymongo import Connection

class Agent(object):

    def __init__(self, host = None, log = None):
        self.host = host
        self.log = log

    def get_collection(self):
        """
        Returns a collection object to insert data
        """
        try:
            conn = Connection(self.host)
            db = conn.pysquila
            logs = db.logs
        except Exception:
            print >> sys.stderr, e
            sys.exit(120)
        return logs
        
    def get_time(self, timestamp):
        return (datetime.utcfromtimestamp(timestamp))

    def process_line(self, line):
        """
        Splits the log line, converts timestamps to datetime objects and
        returns a dictionary to be inserted into the DB.
        """
        time, duration, client_address, result, size, method, url,\
                                    ident, hier, content_type = line.split() 
        doc = {'time': self.get_time(float(time)),
               'duration' : int(duration),
               'client_address': client_address,
               'result': result,
               'size': int(size),
               'method': method,
               'url': url,
               'ident': ident,
               'hierarchy': hier,
               'content_type': content_type,
              }
        return doc

    def process_log(self):
        """
        Opens the log and does the hard work
        """
        logs = self.get_collection()
        with open(self.log) as log:
            for line in log:
                doc = self.process_line(line)
                logs.insert(doc, safe=True)
