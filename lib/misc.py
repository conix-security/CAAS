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
import hashlib
import time
from lib.ssh import ssh
from lib.constants import ROOT_DIR

try:
    import magic
    HAVE_MAGIC = True
except ImportError:
    HAVE_MAGIC = False

log = logging.getLogger(__name__)
last_server_id = 1




################################
# Reports
################################

# download reports (user/kernel) for a single task
#   - gets cuckoo identifiers and sample md5 hash
#   - initiate SSH connection
#   - download reports and move them to results folder
#   - set reported flag on task
def download_report_by_id(analysis_id, db_client):
    
    data = db_client.get_analysis_basic_information(analysis_id)
    if data == None:
        log.error("Analysis not found.")
        return 0
    
    cuckoo_id = data[1]
    kernel_analysis = data[2]
    state = data[3]
    server_id = data[5]
    md5 = data[7]

    if cuckoo_id == 0:
        log.warning("Cuckoo identifiers = zero")
        return 0
    
    server_info = db_client.get_server(server_id)
    if not server_info:
        log.error("Bad server information")
        return 0
   
    if server_info[1] == "localhost" or server_info[1] == "127.0.0.1":
        cuckoo_path = server_info[5]
        report_path = cuckoo_path+"/storage/analyses/"+str(cuckoo_id)+"/reports/report.json"
        stdin,stdout,stderr = os.popen3("ls "+report_path)
        stdout_l = ""
        stderr_l = ""
        if stdout:
            stdout_l = stdout.read()
        if stderr:
            stderr_l = stderr.read()
        log.debug("LS local STDOUT: "+stdout_l)
        log.debug("LS local STDERR: "+stderr_l)
        if stdout_l == "":
            log.warning("Analysis not finished yet.")
            return 0
        db_client.set_finished_analysis(analysis_id)
        report_name = os.path.join(ROOT_DIR, "results", md5 + "."+str(analysis_id)+".json")
        os.rename(report_path, report_name)
        log.info("Analysis #"+str(analysis_id)+" report downloaded")
        db_client.set_reported_analysis(analysis_id)
        update_score(db_client, report_name, analysis_id)
        return 1


    ssh_client = ssh()
    if ssh_client.create(server_info[1],server_info[2],server_info[3],server_info[4],server_info[5]) == 0:
        log.error("SSH connection error")
        return 0
    
    # if was not reported as finished, check if finished 
    if state < 2:
        state = ssh_client.check_report(cuckoo_id)
        # still running...
        if state == 0:
            log.warning("Analysis not finished yet.")
            return 0
        else:
            db_client.set_finished_analysis(analysis_id)
    
    temp_path = ssh_client.download_report(cuckoo_id)
    if not temp_path:
        log.error("Could not download "+str(analysis_id)+" report")
    else:
        report_name = os.path.join(ROOT_DIR, "results", md5 + "."+str(analysis_id)+".json")
        os.rename(temp_path, report_name)
        log.info("Analysis #"+str(analysis_id)+" report downloaded")
        db_client.set_reported_analysis(analysis_id)
        update_score(db_client, report_name, analysis_id)
    
    ssh_client.close()
    return 1

# update score
#   - parses json file
#   - update score in db (analysis total score + signatures)
def update_score(db_client,json_path,analysis_id):
    try:
        json_data = open(json_path)
        data = json.load(json_data)
    except Exception,e:
        if json_data:
            json_data.close()
        log.warning("JSON error")
        return 0

    score = 0
    if data["signatures"]:
        for signature in data["signatures"]:
            score = score + signature["severity"]
            db_client.add_analysis_signature(signature["severity"], signature["name"]+":"+signature["description"],analysis_id)
    json_data.close()

    return 1

# download all not previously reported taks reports
#   - list finished tasks (get ids)
#   - call download_report for each task
def download_all_available_reports(db_client):
    
    ids = db_client.get_active_cuckoo_analyses()
    for t in ids:
        task_id = t[0]
        analysis_id = t[1]
        log.info("Downloading task <"+str(task_id)+"> analysis #"+str(analysis_id)+" report")
        download_report_by_id(analysis_id, db_client)
    
    return 1
    
    
################################
# Checks
################################

# check for supplied file type (PE / PDF / OFFICE DOC)
#   - uses magic methods
#   - on exceptions, returns True
def is_file_type_ok(file_path):
    if not HAVE_MAGIC:
        file_type = os.popen("file \""+file_path+"\"").read()
    try:
        ms = magic.open(magic.MAGIC_NONE)
        ms.load()
        file_type = ms.file(file_path)
    except:
        try:
            file_type = magic.from_file(file_path)
        except Exception:
            return True
    
    if "PE32" in file_type or "MS-DOS" in file_type or \
            "PDF" in file_type or "Rich Text Format" in file_type or \
            "Microsoft Word" in file_type or "Microsoft Office Word" in file_type or \
            "Microsoft Office Excel" in file_type or "Zip archive" in file_type:
        return True

    log.debug("Not supported extension : "+file_type)
    return False




################################
# Servers
################################

# get server information
#   - if server_id is supplied, returns server information
#   - if server_id is not supplied, returns next server information
def get_server_info(db_client, server_id=None):
    global last_server_id
    first_server = None
    servers = db_client.get_servers()
    for server_data in servers:
        if server_data[6] == 0:
            continue
        
        if first_server == None:
            first_server = server_data

        if server_data[0] > last_server_id:
            last_server_id = server_data[0]
            return server_data

    last_server_id = 0
    return first_server




################################
# New file handler
################################

# handle new case
#   - checks for file, md5, type
#   - creates new db entry
#   - creates analyses
def handle_new_file(db_client,file_path,check_type,source_type,source_id):
    global last_server_id

    if not os.path.exists(file_path):
        log.warning("File \""+file_path+"\": not found")
        return 0

    conf = db_client.load_conf()
    parse_metadata = conf[0]
    auto_download_reports = conf[1]
    enable_usermode_analysis = conf[6]
    enable_kernelmode_analysis = conf[7]
    usermode_timeout = conf[8]
    kernelmode_timeout = conf[9]

    fhandle = open(file_path, "rb")
    fdata = fhandle.read()
    fhandle.close()
    
    m = hashlib.md5()
    m.update(fdata)
    md5 = m.hexdigest()
    
    tid = db_client.get_task_id_by_md5(md5)
    if tid == 0:
        new_name = md5+".bin"
        new_path = os.path.join(ROOT_DIR, "binaries", new_name)
        log.debug("New file : "+file_path+" > "+new_path)
        fhandle = open(new_path, "wb")
        fhandle.write(fdata)
        fhandle.close()
        
    	if check_type == True and is_file_type_ok(file_path) == False:
            task_id = db_client.create_task(md5)
            if task_id == 0:
                log.error("Could not create new task.")
                return 0
            log.warning("\""+file_path+"\": incorrect file type, analyses not created. Task ID <"+str(task_id)+">")
	else:
            # Create task + analyses into db
            kid = -1
            uid = -1
            if enable_usermode_analysis != 0:
                uid = 0
            if enable_kernelmode_analysis != 0:
                kid = 0
            task_id = db_client.create_task_and_analyses(uid,kid,0,0,md5,0)
            if task_id == 0:
                log.error("Could not create new task.")
                return 0
            log.info("New task with ID <"+str(task_id)+"> created")
        
        # Add metadata
        if parse_metadata == 1:
            meta_path = file_path+".meta"
            if os.path.exists(meta_path):
                add_suricata_metadata_to_task(db_client, meta_path, task_id, source_type, source_id)
            else:
                db_client.add_meta_info(task_id,  time=time.time(), source_type=source_type, source_id=source_id)
        else:
            db_client.add_meta_info(task_id,  time=time.time(), source_type=source_type, source_id=source_id)
        
    else:
        log.warning("Ignoring already known file with \""+md5+"\" hash")
        if parse_metadata == 1:
            log.info("Adding metadata to existing task...")
            meta_path = file_path+".meta"
            if os.path.exists(meta_path):
                add_suricata_metadata_to_task(db_client, meta_path, tid, source_type, source_id)
            else:
                db_client.add_meta_info(tid,  time=time.time(), source_type=source_type, source_id=source_id)
        else:
            db_client.add_meta_info(tid,  time=time.time(), source_type=source_type, source_id=source_id)
    
    #os.remove(file_path)
    if parse_metadata == 1:
        meta_path = file_path+".meta"
        if os.path.exists(meta_path):
            os.remove(meta_path)
    return 1




# parses suricata metadata and adds to task
#   - suricata metadata lines follow this scheme: KEYWORD: description
#   - only parses several key words
def add_suricata_metadata_to_task(db_client, metadata_path, task_id, source_type, source_id):
    if not os.path.exists(metadata_path):
        log.error(metadata_path+" meta file does not exist")
        return 0
    
    fhandle = open(metadata_path, "r")
    fdata = fhandle.read()
    fhandle.close()

    time = ""
    proto = ""
    src_ip = ""
    dst_ip = ""
    src_port = ""
    dst_port = ""
    uri = ""
    filename = ""
    magic = ""
    proto = 0
    host = ""
    referer = ""
    user_agent = ""
    sz = 0
    lines = fdata.split("\n")
    for line in lines:
        words = line.split(":",1)
        if len(words) >= 2:
            command = words[0].strip()
            data = words[1].strip()
            if command == "TIME":
                time = data
            elif command == "SRC IP":
                src_ip = data
            elif command == "DST IP":
                dst_ip = data
            elif command == "PROTO":
                proto = data
            elif command == "SRC PORT":
                src_port = data
            elif command == "DST PORT":
                dst_port = data
            elif command == "HTTP URI":
                uri = data
            elif command == "FILENAME":
                filename = data
            elif command == "MAGIC":
                magic = data
            elif command == "HTTP HOST":
                host = data
            elif command == "HTTP REFERER":
                referer = data
            elif command == "HTTP USER AGENT":
                user_agent = data
            elif command == "SIZE":
                sz = data
    
    return db_client.add_meta_info(task_id, time, src_ip, dst_ip, proto, src_port, dst_port, uri, filename, magic, source_type, source_id, host, referer, user_agent, sz) 





################################
# Analysis dispatcher
################################

# Dispatch new analysis / update analysis info
def handle_analysis(db_client,analysis_id):
    
    global last_server_id

    data = db_client.get_analysis_basic_information(analysis_id)
    md5 = data[7]
    cuckoo_id = data[1]
    kernelmode_analysis = data[2]

    if cuckoo_id != 0:
        log.warning("Already started analysis")
        return 0

    file_path = os.path.join(ROOT_DIR,"binaries",md5+".bin")
    if not os.path.exists(file_path):
        log.warning("File \""+file_path+"\": not found")
        return 0

    conf = db_client.load_conf()
    parse_metadata = conf[0]
    auto_download_reports = conf[1]
    enable_usermode_analysis = conf[6]
    enable_kernelmode_analysis = conf[7]
    usermode_timeout = conf[8]
    kernelmode_timeout = conf[9]

    fhandle = open(file_path, "rb")
    fdata = fhandle.read()
    fhandle.close()
    
    state = 0
    state_k = 0
    ssh_client = ssh()
        
    # get server
    original_server_id = last_server_id
    server_info = get_server_info(db_client)
    if not server_info:
        log.error("Cannot get server information.")
        return 0

    # local server ?
    if server_info[1] == "127.0.0.1" or server_info[1] == "localhost":
        is_available = 2
    else:
        is_available = ssh_client.create(server_info[1],server_info[2],server_info[3],server_info[4],server_info[5])
        
   #  Every server down
    if is_available == 0:
        log.error("No available servers found.")
        return 0
    
    if is_available == 1:
        # Start remote analyses
        if kernelmode_analysis == 1:
            cuckoo_id = ssh_client.start_single_analysis(file_path, True, kernelmode_timeout)
        else:
            cuckoo_id = ssh_client.start_single_analysis(file_path, False, usermode_timeout)
        ssh_client.close()
    else:
        # Localhost, start local analysis
        if kernelmode_analysis == 1:
            cuckoo_id = start_local_analysis(file_path, server_info[5], True, kernelmode_timeout)
        else:
            cuckoo_id = start_local_analysis(file_path, server_info[5], False, usermode_timeout)
    
    if cuckoo_id == 0 :
        log.error("Could not start cuckoo task")
        return 0

    # Update analysis info
    db_client.set_analysis_dispatched(analysis_id, cuckoo_id, server_info[0]) 
    log.info("New analysis for task ID "+str(analysis_id)+" created (server "+str(server_info[0])+":"+str(cuckoo_id)+")")
        
    return

# local cuckoo analysis creation
def start_local_analysis(file_path, cuckoo_path, kernel_analysis=False, timeout=300):
    command = cuckoo_path+"/utils/submit.py "+file_path+" --timeout "+str(timeout)
    if kernel_analysis != False:
        command = command + " --options kernel_analysis=yes"
    stdin,stdout,stderr = os.popen3(command)
    is_task = 0

    if stdout:
        stdout_line = stdout.read()
    if stderr:
        stderr_line = stderr.read()
   
    log.debug("Local command output STDOUT: "+stdout_line)
    log.debug("Local command output STDERR: "+stderr_line)
    
    if stdout_line != "":
        id_task = int(stdout_line.split(" ")[-1])
    else:
        log.err("Local submit failed, stderr: "+stderr_line)

    return id_task





