#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cherrypy
import logging
from datetime import datetime, timedelta
from cherrypy import tools, log
from pymongo import Connection

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
    def test(self):
        logs = self.get_collection()
