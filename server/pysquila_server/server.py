#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cherrypy
import logging
import json
from datetime import datetime, timedelta
from cherrypy import tools, log
from pymongo import Connection, json_util

class PySquiLAServer:

    def __init__(self, debug, tz_offset, dbname, host):
        self.host = host.strip("'")
        self.dbname = dbname.strip("'")
        self.debug_enabled = debug
        self.tz_offset = timedelta(seconds = tz_offset * 3600)

    def get_collection(self):
        """
        Returns a collection object to insert data
        """
        try:
            log("Connecting to %s, db %s" % (self.host, self.dbname))
            conn = Connection(self.host)
            db = conn[self.dbname]
            logs = db.logs
        except Exception, e:
            log("Problems while getting the collection: %s" % e)
            logs = None
        return logs

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('/static/index.html')

    @cherrypy.expose
    def topusers(self, *args, **kw):
        logs = self.get_collection()
        log(str(kw))

        start_date = self.gen_date(float(kw['initial_date']))
        end_date = self.gen_date(float(kw['final_date']))

        log('Query')
        query = { 't' : { '$gte' : start_date, '$lte' : end_date } }

        map_function = """function m() {
                             emit(this.c, {duration: this.d, 
                                           size: this.s, 
                                           conn: 1});
                          }"""

        reduce_function = """function r(key, val) {
                                var total_duration = 0;
                                var total_size = 0;
                                var total_conn = 0;
                                for (var i = 0; i < val.length; i++) {
                                   total_duration += val[i].duration;
                                   total_size += val[i].size;
                                   total_conn += 1;
                                }
                                return {duration: total_duration, 
                                        size: total_size, 
                                        total_conn : total_conn };
                             }"""
       
        result = logs.map_reduce(map_function, 
                                 reduce_function, 
                                 query = query)

        aaData = { 'aaData' : [] } 
        total_size = 0
        total_dura = 0

        for res in result.find():
            total_size += res['value']['size']
            total_dura += res['value']['duration']
        
        for res in result.find():
            aaData['aaData'].append([res['_id'], 
                                    res['value']['total_conn'],
                                    res['value']['size'],
                                    (res['value']['size'] / total_size) * 100,
                                    res['value']['duration'],
                                    (res['value']['duration'] / total_size) * 100,
                                   ])
        
        res_json = json.dumps(aaData)
        
        return res_json

    def gen_date(self, timestamp):
        original_date = datetime.fromtimestamp(timestamp)
        correct_date = original_date + self.tz_offset
        return correct_date
