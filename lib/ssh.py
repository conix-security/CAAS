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

import os, paramiko, logging

from lib.constants import ROOT_DIR

log = logging.getLogger(__name__)

#
# SSH operations class
#
class ssh:

    client = None                   # SSH client
    remote_cuckoo_path = None       # remote path



    ################################
    # Constructor / destructor
    ################################
    # constructor
    def  __init__(self):
        return

    # destructor
    def __del__(self):
        self.close()
        return



    ################################
    # Paramiko
    ################################
    
    # initiate paramiko client
    def create(self, server, port, user, password, remote_path):
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(server, port, user, password)
            self.remote_cuckoo_path = remote_path
        except Exception,e:
            log.debug("Create SSH connection failed: %s" %e)
            return 0
        return 1

    # close client
    def close(self):
        if self.client:
            try:
                self.client.close()
            except Exception,e:
                log.debug("Create SSH connection failed: %s" %e)

        self.client = None
        return



    ################################
    # File transfer
    ################################
    
    # upload file to remote server using SFTP client
    def upload_file(self,local_path, remote_path):
	if not self.client:
            return 0
        if not os.path.exists(local_path):
            return 0
        try:
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            sftp.put(local_path, remote_path)
            sftp.close()
        except Exception,e:
            log.debug("SFTP PUT command failed: %s" %e)
            return 0
	return 1
        
        
    
    ################################
    # Reports
    ################################
    
    # downloads a remote report file
    #   - generates the local temporary path
    #   - generates remote report path
    #   - get remote file using paramiko.SFTPClient
    #   - returns temporary path
    def download_report(self, cuckoo_task_id):
        if not self.client:
            return None

        local_path = "/tmp/report_" + str(cuckoo_task_id) + ".json.tmp"
        
        try:
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            sftp.get(self.remote_cuckoo_path + "/storage/analyses/" + str(cuckoo_task_id) + "/reports/report.json", local_path)
            sftp.close()
        except Exception,e:
            log.debug("SFTP GET command failed:: %s" %e)
            return None
        
        return local_path
    
    # checks a report state (returns 0 if not available, 1 if available)
    #   - generates remote report path
    #   - execute ls <path>
    #   - if stderr output, returns 0
    def check_report(self, cuckoo_task_id):
        if not self.client:
            return 0
        # LS remote report path
        remote_path = self.remote_cuckoo_path + "/storage/analyses/" + str(cuckoo_task_id) + "/reports/report.json"
        try:
            stdin, stdout, stderr = self.client.exec_command("ls "+remote_path)
        except Exception,e:
            log.debug("Execute LS command failed (SSH error): %s" %e)
            return 0
        stdout_line = ""
        stderr_line = ""
        if stdout:
            stdout_line = stdout.readlines()
            if len(stdout_line) > 0:
                stdout_line = stdout_line[0]
            else:
                stdout_line = ""
        if stderr:
            stderr_line = stderr.readlines()
            if len(stderr_line) > 0:
                stderr_line = stderr_line[0]
            else:
                stderr_line = ""
        log.debug("SSH STDOUT: "+stdout_line)
        log.debug("SSH STDERR: "+stderr_line)
        if stderr_line != "":
            return 0
        else:
            return 1



    ################################
    # Analyses
    ################################
    
    # starts a dual analysis (kernelmode/usermode)
    #   - uploads file to /tmp folder
    #   - starts kernelmode / usermode analyses
    #   - returns [id_usermode, id_kernelmode]
    def start_dual_analysis(self, file_path, kernelmode=False, usermode=False, kerneltimeout=300, usertimeout=300):
        if not os.path.exists(file_path):
            return [0,0]
        temp_path = "/tmp/"+os.path.basename(file_path)
        if self.upload_file(file_path, temp_path) == 0:
            return [0,0]
        cid = 0
        kcid = 0
        if kernelmode == True:
            kcid = self.start_remote_analysis(temp_path, kernelmode=True, timeout=kerneltimeout)
        if usermode == True:
            cid = self.start_remote_analysis(temp_path, kernelmode=False, timeout=usertimeout)
        return [cid, kcid]

    # starts a single analysis
    #   - uploads on /tmp folder
    #   - starts analysis
    #   - returns created id
    def start_single_analysis(self, file_path, kernelmode=False, timeout=300):
        if not os.path.exists(file_path):
           return 0
        temp_path = "/tmp/"+os.path.basename(file_path)
        if self.upload_file(file_path, temp_path) == 0:
            return 0
        cid = self.start_remote_analysis(temp_path,kernelmode,timeout)
        return cid

    # starts a cuckoo analysis and returns its ID
    #   - start command using SSH & remote submit.py script
    #   - parse output to get IDs
    #   - return 0 on error
    def start_remote_analysis(self, file_path, kernelmode=False, timeout=300):
        if int(timeout) <= 0:
            return 0
        id_task = 0
	command = self.remote_cuckoo_path + "/utils/submit.py " + file_path + " --timeout " + str(timeout)
	if kernelmode != False:
            command = command + " --options kernel_analysis=yes"
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
        except Exception,e:
            log.debug("Execute submit command failed (SSH error): %s" %e)
            return 0
	stdout_line = ""
        stderr_line = ""
        if stdout:
            stdout_line = stdout.readlines()
            if len(stdout_line) > 0:
                stdout_line = stdout_line[0]
            else:
                stdout_line = ""
        if stderr:
            stderr_line = stderr.readlines()
            if len(stderr_line) > 0:
                stderr_line = stderr_line[0]
            else:
                stderr_line = ""
        log.debug("SSH STDOUT: "+stdout_line)
        log.debug("SSH STDERR: "+stderr_line)
        if stdout_line != "":
            id_task = int(stdout_line.split(" ")[-1])
        else:
            log.error("SSH COMMAND ERROR, stderr: "+stderr_line)
        return id_task




   
