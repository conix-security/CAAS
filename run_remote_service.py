#!/usr/bin/env python
#  Copyright 2013 Conix Security, Nicolas Correia, Adrien Chevalier
#
#  This file is part of CAAS.
#
#  CAAS is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  CAAS is distibuted in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with CAAS.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import logging
import argparse

try:
    from lib.remote_service import remote_service
    from lib.log import init_log
except ImportError, e:
    print "ERROR : Missing dependency: %s" % e
    exit(1)

log = logging.getLogger()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quiet", help="Display only error messages", action="store_true", required=False)
    parser.add_argument("-d", "--debug", help="Display debug messages", action="store_true", required=False)
    args = parser.parse_args()

    init_log("remote_service")

    if args.quiet:
        log.setLevel(logging.WARN)
    elif args.debug:
        log.setLevel(logging.DEBUG)
    s = remote_service()
    try:
        s.run()
    except KeyboardInterrupt:
        log.warning("Keyboard interrupt, stopping...")
        s.stop()

if __name__ == "__main__":
    try:
        main()
    except Exception,e:
        if len(log.handlers) > 0:
            log.critical("Critical error, aborting: %s" % e)
        else:
            sys.stderr.write("Critical error, aborting: %s\n" % e)

        exit(1)

