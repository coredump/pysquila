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
        
        log('Query')
        results = logs.find({ 't' : { '$gte' : start_date, '$lte' : end_date } }, 
                              {'d' : 1, 'c' : 1, 's' : 1 },
                              )
        log('Apos query')
        total_size = 0
        total_duration = 0
        temp_dic = {}

        for res in results:
            duration = res['d']
            client = res['c']
            size = res['s']

            total_size += size
            total_duration += duration

            if not temp_dic.has_key(client):
                temp_dic[client] = {}
                temp_dic[client]['connections'] = 0
                temp_dic[client]['duration'] = 0
                temp_dic[client]['size'] = 0
            else:
                temp_dic[client]['duration'] += duration
                temp_dic[client]['size'] += size
                temp_dic[client]['connections'] += 1

        result_dic = {'aaData' : [],
                      'iTotalRecords' : 0,
                      'iTotalDisplayRecords' : len(temp_dic),
                     }

        for key in keys(temp_dic):
            percent_data = (temp_dic[key]['size'] / total_size) * 100
            percent_time = (temp_dic[key]['duration'] / total_duration) * 100
            result_dic['aaData'].append([ key, temp_dic['connections'], 
                                      temp_dic['size'], percent_data,
                                      temp_dic['duration'], percent_time ])
        
        out_json = json.dumps(result_dic)
        
        return out_json

    def gen_date(self, timestamp):
        original_date = datetime.fromtimestamp(timestamp)
        correct_date = original_date + self.tz_offset
        return correct_date
