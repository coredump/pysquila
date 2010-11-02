#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import ConfigParser
from pysquila_agent import agent

config = ConfigParser.ConfigParser()
if len(sys.argv) > 1:
    # config file on the command line?
    try:
        config.readfp(open(sys.argv[1]))
    except:
        print "Problem reading the config file"
        sys.exit(3)
else:
    # try other places
    current_dir = os.path.dirname(os.path.realpath(__file__))
    local_file = os.path.join(current_dir, 'pysquilagent.cfg')
    result = config.read(['/etc/pysquilagent.cfg', local_file])
    if len(result) == 0:
        print "No config file. Unable to proceed."
        sys.exit(3)

access_log = config.get('Common', 'AccessLog')
mongo_host = config.get('DB', 'host')
mongo_db = config.get('DB', 'dbname')

a = agent.Agent(mongo_host, mongo_db, access_log)
a.process_log()
