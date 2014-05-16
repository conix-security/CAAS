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

import sqlite3, os
import logging
from lib.constants import ROOT_DIR

log = logging.getLogger(__name__)

#
# sqlite3 database connection
#
class db:

    connection = None   # connection handle
    cursor = None       # cursor handle

    ################################
    # Constructor / destructor
    ################################
    
    # constructor
    def __init__(self):
        return

    # destructor
    def __del__(self):
        self.close()
        return
   
    ################################
    # Database
    ################################
   
    # close database
    def close(self):
        if self.connection:
            self.connection.close()
        return

    # open sqlite3 database, returns 0 on error
    # if file not found => creates database
    def open_db(self, file_name):
        if not os.path.exists(file_name):
            if self.create_db(file_name) == 0:
                log.critical("Cannot create database.")
                return 0
        else:
            try:
                self.connection = sqlite3.connect(file_name)
                self.cursor = self.connection.cursor()
            except sqlite3.Error,e:
                if self.connection:
                    self.connection.rollback()
                    self.connection.close()
                log.critical("Cannot connect to database")
                log.debug("SQLITE exception: %s" % e)
                return 0
        return 1
  
    # create database
    #   - opens create.sql file
    #   - reads its content then execute it line by line
    def create_db(self, file_name):
        schema_path = os.path.join(ROOT_DIR, "db", "create.sql")
        if not os.path.exists(schema_path):
            print("Database schema not found")
            return 0
        fHandle = open(schema_path,"r")
        fData = fHandle.read()
        fHandle.close()
        lines = fData.split("\n")
        try:
            self.connection = sqlite3.connect(file_name)
            self.cursor = self.connection.cursor()
            for create_request in lines:
                self.cursor.execute(create_request)
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
                self.connection.close()
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1
        
    ################################
    # Configuration
    ################################
  
    # set sampling setting
    def set_sampling(self, state):
        if state < 0 or state > 100:
            return 0
        request = "UPDATE configuration SET sampling = ?"
        try:
            self.cursor.execute(request, [state])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update sampling setting")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1


    # set kernelmode timeout setting
    def set_kernelmode_timeout(self, state):
        request = "UPDATE configuration SET kernelmode_timeout = ?"
        try:
            self.cursor.execute(request, [state])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update kernelmode timeout setting")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1


    # set kernelmode alert limit setting
    def set_kernelmode_alert_limit(self, state):
        request = "UPDATE configuration SET kernelmode_score_high = ?"
        try:
            self.cursor.execute(request, [state])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update kernelmode alert limit setting")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1


    # set kernelmode warn limit setting
    def set_kernelmode_warn_limit(self, state):
        request = "UPDATE configuration SET kernelmode_score_medium = ?"
        try:
            self.cursor.execute(request, [state])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update kernelmode warn limit setting")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1


    # set usermode timeout setting
    def set_usermode_timeout(self, state):
        request = "UPDATE configuration SET usermode_timeout = ?"
        try:
            self.cursor.execute(request, [state])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update usermode timeout setting")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1


    # set usermode alert limit setting
    def set_usermode_alert_limit(self, state):
        request = "UPDATE configuration SET usermode_score_high = ?"
        try:
            self.cursor.execute(request, [state])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update usermode alert limit setting")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1


    # set usermode warn limit setting
    def set_usermode_warn_limit(self, state):
        request = "UPDATE configuration SET usermode_score_medium = ?"
        try:
            self.cursor.execute(request, [state])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update usermode warn limit setting")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1


    # set kernelmode analysis setting
    def set_kernel_analysis(self, state):
        request = "UPDATE configuration SET enable_kernelmode_analysis = ?"
        try:
            self.cursor.execute(request, [state])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update kernelmode setting")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1
    def enable_kernelmode_analysis(self):
        return self.set_kernelmode_analysis(1)
    def disable_kernelmode_analysis(self):
        return self.set_kernelmode_analysis(0)


    # set usermode analysis setting
    def set_usermode_analysis(self, state):
        request = "UPDATE configuration SET enable_usermode_analysis = ?"
        try:
            self.cursor.execute(request, [state])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update usermode setting")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1
    def enable_usermode_analysis(self):
        return self.set_usermode_analysis(1)
    def disable_usermode_analysis(self):
        return self.set_usermode_analysis(0)
    # set autodownload setting
    def set_reports_autodownload(self, state):
        request = "UPDATE configuration SET auto_download_reports = ?"
        try:
            self.cursor.execute(request, [state])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update report autodownload setting")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1
    def enable_reports_autodownload(self):
        return self.set_reports_autodownload(1)
    def disable_reports_autodownload(self):
        return self.set_reports_autodownload(0)


    # load configuration raw (select *); be careful while db updates...
    def load_conf(self):
        request = "SELECT * FROM configuration LIMIT 0,1"
        try:
            self.cursor.execute(request)
            result = self.cursor.fetchone()
        except sqlite3.Error, e:
            log.error("Cannot get configuration.")
            log.debug("SQLITE exception: %s" % e)
            return None
        return result

    # get configuration (safe, not select *)
    def get_config(self):
        request = "SELECT parse_metadata, auto_download_reports, kernelmode_score_medium, kernelmode_score_high, usermode_score_medium, usermode_score_high, enable_usermode_analysis, enable_kernelmode_analysis, usermode_timeout, kernelmode_timeout, sampling FROM configuration LIMIT 0,1"
        try:
            self.cursor.execute(request)
            result = self.cursor.fetchone()
        except sqlite3.Error, e:
            log.error("Cannot get config.")
            log.debug("SQLITE exception: %s" % e)
            return None
        return result
   
   
    ################################
    # Signatures
    ################################
    
    # add analysis signature
    def add_analysis_signature(self, score, title, analysis_id):
        request = "INSERT INTO signature(title, score, analysis_id) VALUES(?,?,?)"
        try:
            self.cursor.execute(request,[title,score,analysis_id])
            lastid = self.cursor.lastrowid
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot create signature")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return lastid
    
    # get matched signatures
    def get_matched_signatures(self, analysis_id):
        request = "SELECT title, score FROM signature WHERE analysis_id = ? ORDER BY score ASC"
        try:
            self.cursor.execute(request,[analysis_id])
            results = self.connection.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot select signatures")
            log.debug("SQLITE exception: %s" % e)
            return []
        return results
        
        
    
    ################################
    # Analysis
    ################################
    
    # create analysis, returns created analysis ID
    #   - create analysis with basic information (cuckoo ID, state, kernelmode, cuckoo server id, associated task)
    #   - returns analysis ID
    def create_analysis(self, cuckoo_id, state, is_kernelmode, task_id, server_id=1):
        request_a = "INSERT INTO analysis (cuckoo_id, kernel_analysis, state, cuckoo_server_id, task_id) VALUES (?,?,?,?,?)"
        try:
            if is_kernelmode == True:
                self.cursor.execute(request_a,[cuckoo_id,1,state,server_id,task_id])
            else:
                self.cursor.execute(request_a,[cuckoo_id,0,state,server_id,task_id])
            lastid = self.cursor.lastrowid
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot create task")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return lastid
        
    # get not new cuckoo analyses
    #   - where identifier == 0 and state = 0 (not started)
    #   - returns [ [task_id, cuckoo_id], ... ]
    def get_new_analyses(self):
        request = "SELECT analysis_id, task_id FROM analysis WHERE state = 0 AND cuckoo_id = 0 ORDER BY analysis_id ASC"
        try:
            self.cursor.execute(request)
            results = self.cursor.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot select new analyses")
            log.debug("SQLITE exception: %s" % e)
            return []
        return results
    
    # get active cuckoo analyses
    #   - where identifier != 0 and state = 0 (still running)
    #   - returns [ [task_id, cuckoo_id], ... ]
    def get_active_cuckoo_analyses(self):
        request = "SELECT task_id, analysis_id, cuckoo_id, cuckoo_server_id, kernel_analysis FROM analysis WHERE state = 1 ORDER BY task_id, cuckoo_id ASC"
        try:
            self.cursor.execute(request)
            results = self.cursor.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot select active analyses")
            log.debug("SQLITE exception: %s" % e)
            return []
        return results
    
    # change task status
    #   - update request
    def update_analysis_status(self, analysis_id, state):
        request = "UPDATE analysis SET state = ? WHERE analysis_id = ?"
        try:
            self.cursor.execute(request, [state, analysis_id])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update task status")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1
  
    # set analysis to "dispatched" (started on remote server)
    def set_analysis_dispatched(self, analysis_id, cuckoo_id, cuckoo_server_id):
        request = "UPDATE analysis SET cuckoo_id = ?, cuckoo_server_id = ?, state = 1 WHERE analysis_id = ?"
        try:
            self.cursor.execute(request, [cuckoo_id, cuckoo_server_id, analysis_id])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot update task status")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1

    # set task to "finished" state (finished, report not downloaded)
    def set_finished_analysis(self, analysis_id):
        return self.update_analysis_status(analysis_id, 2)

    # set analysis to "report downloaded" state
    def set_reported_analysis(self, analysis_id):
        return self.update_analysis_status(analysis_id, 3)

    # get analysis basic information
    def get_analysis_basic_information(self, analysis_id):
        request = "SELECT a.analysis_id, a.cuckoo_id, a.kernel_analysis, a.state, SUM(s.score) as 'total_score', a.cuckoo_server_id, a.task_id, t.md5 FROM analysis a, task t, (SELECT analysis_id,score FROM signature UNION SELECT analysis_id,0 FROM analysis) s WHERE s.analysis_id = a.analysis_id AND a.analysis_id = ? AND a.task_id = t.task_id"
        try:
            self.cursor.execute(request,[analysis_id])
            data = self.cursor.fetchone()
            return data
        except sqlite3.Error, e:
            log.error("Cannot select analysis information")
            log.debug("SQLITE exception: %s" % e)
            return None

        return None

    # get finished analyses identifiers array
    def get_finished_analysis_ids(self):
        request = "SELECT analysis_id FROM analysis WHERE state > 1 ORDER BY analysis_id ASC"
        tasks = []
        try:
            self.cursor.execute(request)
            data = self.cursor.fetchall()
        except sqlite3.Error,e:
            log.error("Cannot select analyses")
            log.debug("SQLITE exception: %s" % e)
            return tasks
        for result in data:
            tasks.append(result[0])
        return tasks
    
    ################################
    # Servers
    ################################
    
    # enables a server
    def enable_server(self, server_id):
        request = "UPDATE cuckoo_server SET is_active = 1 where cuckoo_server_id = ?"
        try:
            self.cursor.execute(request,[server_id])
            self.connection.commit()
        except sqlite3.Error, e:
            return 0
        return 1
        
    # disables a server
    def disable_server(self, server_id):
        request = "UPDATE cuckoo_server SET is_active = 0 where cuckoo_server_id = ?"
        try:
            self.cursor.execute(request,[server_id])
            self.connection.commit()
        except sqlite3.Error, e:
            return 0
        return 1
    
    # add a server
    def add_server(self, name, addr, port, username, password, path):
        request = "INSERT INTO cuckoo_server(name, server_addr, ssh_port, username, password, cuckoo_path, is_active) VALUES(?,?,?,?,?,?,1)"
        try:
            self.cursor.execute(request,[name,addr,port,username,password,path])
            lastid = self.cursor.lastrowid
            self.connection.commit()
        except sqlite3.Error, e:
            return 0
        return lastid
            
    # get servers
    def get_servers(self):
        request = "SELECT cuckoo_server_id, server_addr, ssh_port, username, password, cuckoo_path, is_active, vms_count FROM cuckoo_server ORDER BY cuckoo_server_id ASC"
        try:
            self.cursor.execute(request)
            results = self.cursor.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot get server.")
            log.debug("SQLITE exception: %s" % e)
            return []
        return results
    
    # get single server information
    def get_server(self, server_id):
        request = "SELECT cuckoo_server_id, server_addr, ssh_port, username, password, cuckoo_path, is_active, vms_count FROM cuckoo_server WHERE cuckoo_server_id = ?"
        try:
            self.cursor.execute(request,[server_id])
            result = self.cursor.fetchone()
        except sqlite3.Error, e:
            log.error("Cannot get server.")
            log.debug("SQLITE exception: %s" % e)
            return None
        return result
    
    
    
    ################################
    # Metadata
    ################################
    
    # print task metadata information
    def print_task_metadata(self, task_id):
        request = "SELECT time, src_ip, src_port, dst_ip, dst_port, uri, filename, magic FROM metadata WHERE task_id = ?"
        try:
            self.cursor.execute(request,[int(task_id)])
            results = self.cursor.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot find task <"+str(task_id)+">")
            log.debug("SQLITE exception: %s" % e)
            return 0
        if len(results) == 0:
            return 1
        for data in results:
            print "\tMetadata information:"
            if data[0] != "":
                print "\t\tTime: "+data[0]
            if data[1] != "":
                print "\t\tSRC IP: "+data[1]
            if data[2] != "":
                print "\t\tSRC PORT: "+data[2]
            if data[3] != "":
                print "\t\tDST IP: "+data[3]
            if data[4] != "":
                print "\t\tDST PORT: "+data[4]
            if data[5] != "":
                print "\t\tDOWNLOAD URI: "+data[5]
            if data[6] != "":
                print "\t\tFILENAME: "+data[6]
            if data[7] != "":
                print "\t\tMAGIC: "+data[7]
        return 1
    
    # add meta information to an existing task
    def add_meta_info(self, task_id, time="", src_ip="", dst_ip="", proto="", src_port="", dst_port="", uri="", filename="", magic="", source_type=0, source_id=0, host="", referer="", user_agent="", size=0):
        request = "INSERT INTO metadata(task_id,time,src_ip,dst_ip,src_port,dst_port,uri,filename,magic,source_type,source_id,proto,host,referer,user_agent,sz) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        try:
            self.cursor.execute(request,[task_id,time,src_ip,dst_ip,src_port,dst_port,uri,filename,magic,source_type,source_id,proto,host,referer,user_agent,size])
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot add task meta information")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1

    ################################
    # Tasks
    ################################
    
    # print all tasks information
    def print_all_tasks(self):
        request = "SELECT task_id FROM task ORDER BY task_id ASC"
        try:
            self.cursor.execute(request)
            data = self.cursor.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot list tasks")
            log.debug("SQLITE exception: %s" % e)
            return 0
        for task in data:
            self.print_task(task[0])
        return 1

    # print the task basic information (task + analyses)
    def print_task(self, task_id):
        # get info
        request = "SELECT task_id, md5 FROM task WHERE task_id = ?"
        try:
            self.cursor.execute(request,[int(task_id)])
            results = self.cursor.fetchone()
        except sqlite3.Error, e:
            log.error("Cannot find task <"+str(task_id)+">")
            log.debug("SQLITE exception: %s" % e)
            return 0
        print "Task <"+str(results[0])+"> (MD5 "+results[1]+") status"
        
        # get analyses
        request = "SELECT analysis_id FROM analysis WHERE task_id = ?"
        try:
            self.cursor.execute(request,[int(task_id)])
            results = self.cursor.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot find task <"+str(task_id)+">")
            log.debug("SQLITE exception: %s" % e)
            return 0
        if len(results) == 0:
            return 1
        
        # for each analysis, print information
        for m in results:
            data = self.get_analysis_basic_information(m[0])
            if data == None:
                continue
            print ""
            print "Analysis <"+str(data[0])+"> status"
            print "\tServer:Cuckoo ID <"+str(data[5])+":"+str(data[1])+">"
            if data[3] == 0:
                print "\t\tStatus: not started"
            elif data[3] == 1:
                print "\t\tStatus: in progress"
            elif data[3] == 2:
                print "\t\tStatus: finished"
            elif data[3] == 3:
                print "\t\tStatus: downloaded, total scored: "+str(data[4])
            ret = self.print_task_metadata(task_id)
            print ""
        return ret
       
    # create task along with 2 analyses, returns created task ID
    #   - create 2 analyses (usermode + kernelmode) if their cuckoo_id <> -1
    #   - returns task ID
    def create_task_and_analyses(self, cuckoo_id, cuckoo_id_k, state, state_k, md5, server_id=1):
        lastid = self.create_task(md5)
        if lastid == 0:
            return 0
        if cuckoo_id != -1:
            self.create_analysis(cuckoo_id,state,False,lastid,server_id)
        if cuckoo_id_k != -1:
            self.create_analysis(cuckoo_id_k,state_k,True,lastid,server_id)
        return lastid
    
    # create task, returns created task ID
    #   - create task and analyses with basic information (cuckoo IDs, states, md5 hash)
    #   - returns task ID
    def create_task(self, md5):
        request_t = "INSERT INTO task (md5) VALUES (?)"
        try:
            self.cursor.execute(request_t,[md5])
            lastid = self.cursor.lastrowid
            self.connection.commit()
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
            log.error("Cannot create task")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return lastid
  
    # check if a md5 hash is present on database
    #   - return its ID or 0
    def get_task_id_by_md5(self, md5):
        request = "SELECT task_id FROM task WHERE md5 = ?"
        task_id = 0
        try:
            self.cursor.execute(request, [md5])
            result = self.cursor.fetchone()
            if result:
                task_id = result[0]
        except sqlite3.Error, e:
            if self.connection:
                self.connection.rollback()
                log.error("Cannot execute md5 search request")
                log.debug("SQLITE exception: %s" % e)
                return 0
        return task_id

    # get tasks identifiers
    #   - select or return empty list
    def get_tasks_ids(self):
        request = "SELECT task_id FROM task ORDER BY task_id ASC"
        tasks = []
        try:
            self.cursor.execute(request)
            data = self.cursor.fetchall()
        except sqlite3.Error,e:
            log.error("Cannot select tasks")
            log.debug("SQLITE exception: %s" % e)
            return tasks
        for result in data:
            tasks.append(result[0])
        return tasks
        


    ################################
    # Remote sources
    ################################
    
    #disable remote source
    def disable_remote_source(self, source_id):
        return self.update_remote_source_status(0,source_id)
        
    # activate remote source
    def enable_remote_source(self, source_id):
        return self.update_remote_source_status(1,source_id)
        
    # update remote source status
    def update_remote_source_status(self, status, source_id):
        request = "UPDATE remote_source SET is_active = ? WHERE remote_source_id = ?"
        try:
            self.cursor.execute(request,[status, source_id])
            self.connection.commit()
        except sqlite3.Error, e:
            log.error("Cannot update remote source status")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1

    # create remote source
    def create_remote_source(self, ip_addr):
        request = "INSERT INTO remote_source(remote_ip_addr) VALUES(?)"
        try:
            self.cursor.execute(request,[ip_addr])
            lastid = self.cursor.lastrowid
            self.connection.commit()
        except sqlite3.Error, e:
            log.error("Cannot create remote source")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return lastid
        
    # get remote sources
    def get_remote_sources(self):
        request = "SELECT remote_source_id, remote_ip_addr, is_active FROM remote_source ORDER BY remote_source_id ASC"
        try:
            self.cursor.execute(request)
            results = self.cursor.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot select remote sources")
            log.debug("SQLITE exception: %s" % e)
            return []
        return results
        
    # get active remote sources
    def get_active_remote_sources(self):
        request = "SELECT remote_source_id, remote_ip_addr FROM remote_source WHERE is_active = 1"
        try:
            self.cursor.execute(request)
            results = self.cursor.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot select active remote sources")
            log.debug("SQLITE exception: %s" % e)
            return []
        return results



    ################################
    # Local sources
    ################################
    
    # disable local source
    def disable_local_source(self, source_id):
        return self.update_local_source_status(0,source_id)
    
    # activate local source
    def enable_local_source(self, source_id):
        return self.update_local_source_status(1,source_id)
    
    # update local source status
    def update_local_source_status(self, status, source_id):
        request = "UPDATE local_source SET is_active = ? WHERE local_source_id = ?"
        try:
            self.cursor.execute(request,[status, source_id])
            self.connection.commit()
        except sqlite3.Error, e:
            log.error("Cannot create local source")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return 1

    # create local source
    def create_local_source(self, folder):
        request = "INSERT INTO local_source (lookup_folder) VALUES(?)"
        try:
            self.cursor.execute(request,[folder])
            lastid = self.cursor.lastrowid
            self.connection.commit()
        except sqlite3.Error, e:
            log.error("Cannot create local source")
            log.debug("SQLITE exception: %s" % e)
            return 0
        return lastid

    # get local sources
    def get_local_sources(self):
        request = "SELECT local_source_id, lookup_folder, is_active FROM local_source ORDER BY local_source_id ASC"
        try:
            self.cursor.execute(request)
            results = self.cursor.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot select local sources")
            log.debug("SQLITE exception: %s" % e)
            return []
        return results
    
    # get active local sources
    def get_active_local_sources(self):
        request = "SELECT local_source_id, lookup_folder FROM local_source WHERE is_active = 1"
        try:
            self.cursor.execute(request)
            results = self.cursor.fetchall()
        except sqlite3.Error, e:
            log.error("Cannot select active local sources")
            log.debug("SQLITE exception: %s" % e)
            return []
        return results
    
    


   
    
