#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

"""
pySquiLA agent 
==============

Responsible to get data from the squid server log to the mongodb server where
the pySquiLA interface can deal with it.  Run it from a crontab, tune the
frequency according to how much data your log generates between runs: the more
data it generates per time, the more times you will want to run the agent.

The agent will search for a configuration file in three places: as its first
argument in the command line, in /etc/pysquilagent.cfg or in the same place
as the pysquilagent binary. The configuration file is very simple and points
to the access.log file::

  [Logs]
  AccessLog=/var/log/squid/access.log

If you are doing an initial load of older logs, you will need to change the
configuration file to point to each log and run the client manually, from
the older log to the newer, before pointing it to your normal access.log.
"""

LOG = logging.getLogger('pysquila')
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)
LOG.setLevel(logging.DEBUG)
