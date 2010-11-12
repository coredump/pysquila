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

        start = int(kw['iDisplayStart'])
        end = start + int(kw['iDisplayLength'])
        sort_col = int(kw['iSortCol_0'])
        start_date = self.gen_date(float(kw['initial_date']))
        end_date = self.gen_date(float(kw['final_date']))
        sort_dir = kw['sSortDir_0']
        search = kw['sSearch']

        results = logs.find( { 't' : { '$gte' : start_date }, 
                               't' : { '$lte' : end_date } }, 
                              {'d' : 1, 'c' : 1, 's' : 1 },
                              ).limit(10)

        total_size = 0
        total_duration = 0
        temp_dic = {}

        
        out_json = json.dumps(t_res, default=json_util.default)
        
        return out_json

    def gen_date(self, timestamp):
        original_date = datetime.fromtimestamp(timestamp)
        correct_date = original_date + self.tz_offset
        return correct_date
