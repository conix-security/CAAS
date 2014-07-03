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

import os
import logging
import json

from lib.db import db
from lib.constants import ROOT_DIR
from lib.misc import download_all_available_reports
from lib.misc import download_report_by_id

log = logging.getLogger(__name__)

#
# "client" commands
# 
class cmdline:
    
    db_client = None

    ################################
    # Constructor / destructor
    ################################
    
    # constructor:
    #   - init db
    def __init__(self):
        self.db_client = db()
        if not self.db_client:
            log.critical("DATABASE inititialization failure")
        if self.db_client.open_db(os.path.join(ROOT_DIR,"db","db.db")) == 0:
            log.critical("DATABASE opening failure")
        return

    # destructor:
    #   - close db connection
    def __del__(self):
        if self.db_client:
            self.db_client.close()
        return

    ################################
    # Tasks
    ################################

    # print a single task
    #   - using db.print_task
    def print_task(self,task_id):
        self.db_client.print_task(task_id)
        return 1
    
    
    ################################
    # Reports
    ################################
    
    # download reports (user/kernel) for a single task
    def download_report(self, task_id):
        s = download_report_by_id(task_id, self.db_client)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1

    # download all reports
    #   - list finished tasks (get ids)
    #   - call download_report for each task
    def download_all_reports(self):
        s = download_all_available_reports(self.db_client)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    
    
    ################################
    # Configuration
    ################################
   
    # print config
    def print_configuration(self):
        conf = self.db_client.get_config()
        if conf == None:
            log.critical("Configuration not found")
            return

        m1 = "disabled"
        parse_metadata = conf[0]
        if parse_metadata == 1:
            m1 = "enabled"
        m2 = "disabled"
        autodl_reports = conf[1]
        if autodl_reports == 1:
            m2 = "enabled"
        kernel_score_m = conf[2]
        kernel_score_h = conf[3]
        user_score_m = conf[4]
        user_score_h = conf[5]
        m3 = "disabled"
        user_enabled = conf[6]
        if user_enabled == 1:
            m3 = "enabled"
        m4 = "disabled"
        kernel_enabled = conf[7]
        if kernel_enabled == 1:
            m4 = "enabled"
        user_timeout = conf[8]
        kernel_timeout = conf[9]
        sampling = conf[10]
        print " [-] Parse metadata :\t\t"+m1
        print " [-] Autodownload reports :\t"+m2
        print " [-] Sampling rate :\t\t"+str(sampling)+"%%"
        print " [-] Usermode analysis :\t"+m3+" "+str(user_timeout)+"s timeout, scoring limit (warning/alert) "+str(user_score_m)+"/"+str(user_score_h)
        print " [-] Kernelmode analysis :\t"+m4+" "+str(kernel_timeout)+"s timeout, scoring limit (warning/alert) "+str(kernel_score_m)+"/"+str(kernel_score_h)
        return

    def set_reports_autodownload(self, state):
        if state == "on":
            s = self.db_client.enable_reports_autodownload()
        elif state == "off":
            s = self.db_client.disable_reports_autodownload()
        else:
            s = 0
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    def set_usermode_analysis(self, state):
        if state == "on":
            s = self.db_client.enable_usermode_analysis()
        elif state == "off":
            s = self.db_client.disable_usermode_analysis()
        else:
            s = 0
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    def set_kernelmode_analysis(self, state):
        if state == "on":
            s = self.db_client.enable_kernelmode_analysis()
        elif state == "off":
            s = self.db_client.disable_kernelmode_analysis()
        else:
            s = 0
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    def set_usermode_warn_limit(self, score):
        s = self.db_client.set_usermode_warn_limit(score)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    def set_kernelmode_warn_limit(self, score):
        s = self.db_client.set_kernelmode_warn_limit(score)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    def set_usermode_alert_limit(self, score):
        s = self.db_client.set_usermode_alert_limit(score)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    def set_kernelmode_alert_limit(self, score):
        s = self.db_client.set_kernelmode_alert_limit(score)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    def set_usermode_timeout(self, timeout):
        s = self.db_client.set_usermode_timeout(timeout)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    def set_kernelmode_timeout(self, timeout):
        s = self.db_client.set_kernelmode_timeout(timeout)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    def set_sampling(self, rate):
        s = self.db_client.set_sampling(rate)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1

    ################################
    # Cuckoo servers
    ################################
    
    # display servers
    def list_servers(self):
        results = self.db_client.get_servers()
        for r in results:
            act = "disabled"
            if r[6] == 1:
                act = "enabled"
            print "#"+str(r[0])+" "+r[5]+" on "+r[3]+"@"+r[1]+":"+str(r[2])+" "+act
        return
    
    # add new cuckoo server
    #   params[] = (addr,port,login,password,path)
    def add_server(self, params):
        if len(params) != 5:
            return 0
        addr = params[0]
        port = params[1]
        login = params[2]
        password = params[3]
        path = params[4]
        name = ""
        s = self.db_client.add_server(name,addr,port,login,password,path)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1

    # set cuckoo server state
    #   params[0] : server id
    #   params[1] : state (on / off)
    def set_server(self, params):
        if len(params) != 2:
            return 0
        server_id = params[0]
        state = params[1]
        if state == "on":
            s = self.db_client.enable_server(server_id)
        elif state == "off":
            s= self.db_client.disable_server(server_id)
        else:
            s= 0
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    
    
    ################################
    # Remote sources
    ################################
    
    # display remote sources
    def list_remote_src(self):
        results = self.db_client.get_remote_sources()
        for r in results:
            act = "disabled"
            if r[2] == 1:
                act = "enabled"
            print "#"+str(r[0])+" : "+r[1]+" "+act
        return

    # create new remote source
    def add_remote_src(self, ip_addr):
        s = self.db_client.create_remote_source(ip_addr)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    
    # set remote source state
    #   params = (id, state)
    def set_remote_src(self, params):
        if len(params) != 2:
            return 0
        src_id = params[0]
        state = params[1]
        if state == "on":
            s = self.db_client.enable_remote_source(src_id)
        elif state == "off":
            s = self.db_client.disable_remote_source(src_id)
        else:
            s = 0
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
            
    
    ################################
    # Local sources
    ################################
    
    # display local sources
    def list_local_src(self):
        results = self.db_client.get_local_sources()
        for r in results:
            act = "disabled"
            if r[2] == 1:
                act = "enabled"
            print "#"+str(r[0])+" : "+r[1]+" "+act
        return

    # create new local source
    def add_local_src(self, folder):
        s = self.db_client.create_local_source(folder)
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1
    
    # set local source state
    #   params = (id, state)
    def set_local_src(self, params):
        if len(params) != 2:
            return 0
        src_id = params[0]
        state = params[1]
        if state == "on":
            s = self.db_client.enable_local_source(src_id)
        elif state == "off":
            s = self.db_client.disable_local_source(src_id)
        else:
            s = 0
        if s == 0:
            log.error("Operation failed")
            return 0
        else:
            log.info("Operation succeeded")
            return 1


