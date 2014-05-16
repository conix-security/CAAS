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
import string
import argparse
import logging

try:
    from lib.cmdline import cmdline
    from lib.log import init_log
except ImportError, e:
    print "ERROR : Missing dependency : %s" % e
    exit(1)

log = logging.getLogger()


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-p","--print_config",help="Print current config", action="store_true", required=False)
    parser.add_argument("-ls","--list_servers",help="List all cuckoo servers information", action="store_true", required=False)
    parser.add_argument("-lr","--list_remote_src",help="List all remote sources", action="store_true", required=False)
    parser.add_argument("-ll","--list_local_src",help="List all local sources", action="store_true", required=False)
    parser.add_argument("-r","--download_report",metavar="<report_id>",type=int,help="Download task reports (overwrite existing)", action="store", required=False)
    parser.add_argument("-s","--submit_task",metavar="<task_id>",type=str,help="Submit new file for analysis", action="store", required=False)
    parser.add_argument("-t","--print_task_status",metavar="<task_id>",type=int,help="Display task information", action="store", required=False)
    parser.add_argument("-d","--debug",help="Display debug messages", action="store_true", required=False)
    
    parser.add_argument("--add_remote_src",metavar="<remote ip address>",type=str,help="Add remote source", action="store", required=False)
    parser.add_argument("--set_remote_src",nargs=2,metavar=("<src id>","<on/off>"),type=str,help="Set remote source state", action="store", required=False)

    parser.add_argument("--add_local_src",metavar="<local folder>",type=str,help="Add local source (folder)", action="store", required=False)
    parser.add_argument("--set_local_src",nargs=2,metavar=("<src id>","<on/off>"),type=str,help="Set local source state (on/off)", action="store", required=False)
    
    parser.add_argument("--add_server",metavar=("<ip address>","<ssh port>","<login>","<password>","<cuckoo path>"),nargs=5,type=str,help="Add cuckoo server", action="store", required=False)
    parser.add_argument("--set_server",metavar=("<server id>","<on/off>"),type=str,nargs=2,help="Set cuckoo server state", action="store", required=False)

    parser.add_argument("--set_reports_autodownload",type=str,metavar="<on/off>",choices=["on","off"],help="Set reports autodownload", action="store", required=False)

    parser.add_argument("--set_usermode_analysis",type=str,metavar="<on/off>",choices=["on","off"],help="Set usermode analysis", action="store", required=False)
    parser.add_argument("--set_kernelmode_analysis",metavar="<on/off>",type=str,choices=["on","off"],help="Set kernelmode analysis (on/off)", action="store", required=False)
    parser.add_argument("--set_usermode_warn_limit",metavar="<score>",type=int,help="Set usermode analysis warning score", action="store", required=False)
    parser.add_argument("--set_kernelmode_warn_limit",metavar="<score>",type=int,help="Set kernelmode analysis warning score", action="store", required=False)
    parser.add_argument("--set_usermode_alert_limit",metavar="<score>",type=int,help="Set usermode analysis alert score", action="store", required=False)
    parser.add_argument("--set_kernelmode_alert_limit",metavar="<score>",type=int,help="Set kernelmode analysis alert score", action="store", required=False)
    parser.add_argument("--set_usermode_timeout",metavar="<timeout, seconds>",type=int,help="Set usermode analysis timeout (seconds)", action="store", required=False)
    parser.add_argument("--set_kernelmode_timeout",metavar="<timeout, seconds>",type=int,help="Set kernelmode analysis timeout (seconds)", action="store", required=False)

    parser.add_argument("--set_sampling",metavar="<rate, percent>",type=int,help="Set sampling feature (analyze only x percent files)", action="store", required=False)
    parser.add_argument("--download_all_reports",help="Download all tasks reports (overwrite existing)", action="store_true", required=False)

    args = parser.parse_args()

    init_log("query")

    obj = cmdline()

    if args.debug:
        log.setLevel(logging.DEBUG)

    if args.print_config:
        obj.print_configuration()
    elif args.list_remote_src:
        obj.list_remote_src()
    elif args.add_remote_src:
        obj.add_remote_src(args.add_remote_src)
    elif args.set_remote_src:
        obj.set_remote_src(args.set_remote_src)
    elif args.list_local_src:
        obj.list_local_src()
    elif args.add_local_src:
        obj.add_local_src(args.add_local_src)
    elif args.set_local_src:
        obj.set_local_src(args.set_local_src)
    elif args.list_servers:
        obj.list_servers()
    elif args.add_server:
        obj.add_server(args.add_server)
    elif args.set_server:
        obj.set_server(args.set_server)
    elif args.set_reports_autodownload:
        obj.set_reports_autodownload(args.set_reports_autodownload)
    elif args.set_usermode_analysis:
        obj.set_usermode_analysis(args.set_usermode_analysis)
    elif args.set_usermode_warn_limit:
        obj.set_usermode_warn_limit(args.set_usermode_warn_limit)
    elif args.set_usermode_alert_limit:
        obj.set_usermode_alert_limit(args.set_usermode_alert_limit)
    elif args.set_usermode_timeout:
        obj.set_usermode_timeout(args.set_usermode_timeout)
    elif args.set_kernelmode_analysis:
        obj.set_kernelmode_analysis(args.set_kernelmode_analysis)
    elif args.set_kernelmode_warn_limit:
        obj.set_kernelmode_warn_limit(args.set_kernelmode_warn_limit)
    elif args.set_kernelmode_alert_limit:
        obj.set_kernelmode_alert_limit(args.set_kernelmode_alert_limit)
    elif args.set_kernelmode_timeout:
        obj.set_kernelmode_timeout(args.set_kernelmode_timeout)
    elif args.submit_task:
        obj.submit_task(args.submit_task)
    elif args.set_sampling:
        obj.set_sampling(args.set_sampling)
    elif args.download_all_reports:
        obj.download_all_reports()
    elif args.download_report:
        obj.download_report(args.download_report)
    elif args.print_task_status:
        obj.print_task(args.print_task_status)

if __name__ == "__main__":
    try:
        main()
    except Exception,e:
        if len(log.handlers) > 0:
            log.critical("Critical error, aborting: %s" % e)
        else:
            sys.stderr.write("Critical error, aborting: %s\n" % e)

        exit(1)

    exit(0)
