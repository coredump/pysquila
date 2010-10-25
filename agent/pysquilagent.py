#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import ConfigParser
import pysquila_agent

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
print access_log
