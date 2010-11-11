#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import ConfigParser
import cherrypy
from pysquila_server import server


config = ConfigParser.ConfigParser()
current_dir = os.path.dirname(os.path.realpath(__file__))
local_file = os.path.join(current_dir, 'pysquilaserver.cfg')
result = config.read(['/etc/pysquilaserver.cfg', local_file])
if len(result) == 0:
    print "No config file. Unable to proceed."
    sys.exit(3)

debug = config.getint('Common', 'Debug')
tz_offset = config.getint('Common', 'TzOffset')
mongo_host = config.get('DB', 'host')
mongo_db = config.get('DB', 'dbname')

s = server.PySquiLAServer(debug, tz_offset, mongo_db, mongo_host)
cherrypy.quickstart(s, config=result[0])
