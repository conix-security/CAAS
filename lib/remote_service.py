# Copyright 2013 Conix Security, Nicolas Correia, Adrien Chevalier
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

import os, time, logging, socket, threading, struct, hashlib, binascii

from lib.constants import ROOT_DIR
from lib.db import db
from lib.misc import download_all_available_reports
from lib.misc import add_suricata_metadata_to_task
from lib.misc import handle_new_file

log = logging.getLogger(__name__)

#
#   Single connection thread handler
#
class service_thread(threading.Thread):
    s = None
    ip = ""
    port = 0
    db_client = None
    remote_source_id = 0
    must_stop = False

    # state machine parameters
    file_type = 0
    file_size = 0
    file_md5 = ""
    meta_size = 0
    meta_crc32 = 0
    file_has_meta_info = False
    state_file_download_authorized = False
    state_file_received = False
    state_meta_received = False
    file_temp_path = ""
    meta_temp_path = ""

    # Thread constructor
    def __init__(self, remote_ip, remote_port, socket, src_id):
        threading.Thread.__init__(self)
        self.ip = remote_ip
        self.s = socket
        self.remote_source_id = src_id
        self.port = remote_port
        return
    
    # Stop service
    #   - sends 0xFF control code
    #   - close connection
    def stop(self):
        log.info("Closing connection from "+self.ip+":"+str(self.port))
        try:
            self.s.send("\xFF")
        except Exception,e:
            log.error("Abort message send error")
            log.debug("Exception %s" % e)
        self.s.close()
        self.db_client.close()
        # fix multithreading sqlite3 warning
        # message when thread's objects are
        # destroyed by parent thread
        del self.db_client
        return

    # checks file size
    def authorized_file_size(self, value):
        return True

    # checks file type
    def authorized_file_type(self, value):
        return True

    # Handles new task request
    #   - recv 1 byte: type
    #   - recv 1 dword: file size
    #   - recv 32 byte: printable MD5 hash
    #   - recv 1 byte: has metadata file (.meta file) 
    #       recv 1 dword: meta file size
    #       recv 1 dword: meta file crc32
    #
    #   - sends 1 byte:
    #       0x00 : don't send nothing
    #       0x01 : only send file metadata
    #       0x02 : send file and metadata (if any)
    def new_task(self):
        self.state_meta_received = False
        self.state_file_received = False
        self.state_download_authorized = False
        self.file_has_meta_info = False
        try:
            self.file_type = self.s.recv(1)
            self.file_size = self.s.recv(4)
            self.file_md5 = self.s.recv(32)
            meta_flag = self.s.recv(1)
            if len(self.file_type) == 0 or len(self.file_size) == 0 or len(self.file_md5) == 0 or len(meta_flag) == 0:
                raise Exception("Received empty data")
            if meta_flag == "\x01":
                self.file_has_meta_info = True
                self.meta_size = self.s.recv(4)
                self.meta_crc32 = self.s.recv(4)
                if len(self.meta_size) == 0 or len(self.meta_crc32) == 0:
                    raise Exception("Received empty data")
        except Exception,e:
            log.error("Network reception error")
            log.debug("Exception %s" % e)
            self.must_stop = True
            return
        
        self.file_type = ord(self.file_type)
        self.file_size = struct.unpack("<L",self.file_size)[0]
        if self.authorized_file_size(self.file_size) == True and self.authorized_file_type(self.file_type) == True:
            self.state_file_download_authorized = True
        if self.db_client.get_task_id_by_md5(self.file_md5) != 0:
            self.state_file_download_authorized = False 
        try:
            if self.state_file_download_authorized:
                self.s.send("\x02")
                log.info("New task command from remote source "+str(self.remote_source_id)+", accepted")
            elif self.file_has_meta_info:
                self.s.send("\x01")
                log.info("New task command from remote source "+str(self.remote_source_id)+", metadata only")
            else:
                self.s.send("\x00")
                log.info("New task command from remote source "+str(self.remote_source_id)+", dropped")
        except Exception,e:
            log.error("Network send error")
            log.debug("Exception %s" % e)
            self.must_stop = True
        log.debug("\tNEGO INFO: type "+hex(self.file_type)+"; size "+hex(self.file_size)+" bytes; md5 "+self.file_md5)
        
        if self.file_has_meta_info:
            self.meta_size = struct.unpack("<L",self.meta_size)[0]
            self.meta_crc32 = struct.unpack("<l",self.meta_crc32)[0]
            log.debug("\tMETA INFO:"+hex(self.meta_size)+"b:"+hex(self.meta_crc32))
        return
    
    # Receives file
    #   - recv 1 dword: file size in bytes
    #   - recv file_size bytes: file
    #
    #   - checks MD5 value
    #   - store in /tmp
    def file_receive(self):
        if self.state_file_download_authorized == False:
            log.warning("File sent before negociation")
            self.must_stop = True
            return
        if self.state_file_received == True:
            log.warning("Dual file send attempt")
            self.must_stop = True
            return
        try:
            size_r = self.s.recv(4)
        except Exception,e:
            log.error("Network recv error")
            log.debug("Exception (file size rcv) %s" % e)
            self.must_stop = True
            return
        log.debug("Receiving file")

        size = struct.unpack("<L",size_r)[0]
        if size != self.file_size:
            log.error("File sizes do not match")
            log.debug("Size : "+hex(size)+" (vs "+hex(self.file_size)+")")
            self.must_stop = True
            return
        
        try:
            recv_sz = 0
            file_content = ""
            while recv_sz < self.file_size:
                to_recv = 1024
                if self.file_size - recv_sz < 1024:
                    to_recv = self.file_size - recv_sz
                file_content = file_content+self.s.recv(to_recv)
                recv_sz = len(file_content)
        except Exception,e:
            log.error("Network file recv error")
            log.debug("Exception (file size) %s" % e)
            self.must_stop = True
            return
        
        m = hashlib.md5()
        m.update(file_content)
        md5 = m.hexdigest()
        
        if md5 != self.file_md5:
            log.error("File MD5 does not match")
            log.debug("MD5 : "+md5+" (vs "+self.file_md5+")")
            self.must_stop = True
            return
        
        self.file_temp_path = os.path.join("/tmp/",self.file_md5)
        fHandle = open(self.file_temp_path,"w")
        fHandle.write(file_content)
        fHandle.close()
        
        self.state_file_received = True
        code = handle_new_file(self.db_client,self.file_temp_path,True,2,self.remote_source_id)
        if code == 0:
            log.warning("File could not been queued, returning error code to remote client")
        code = chr(code)
        try:
            self.s.send(code)
        except Exception,e:
            log.error("Network send error")
            log.debug("Exception %s" % e)
            self.must_stop = True
            return

        return
    
    # Receives metadata
    #   - recv 1 dword: meta file size
    #   - recv file_size bytes: meta file
    #  
    #   - checks crc32 value
    #
    #   - sends 1 byte:
    #       0x00 : an error occured, try again
    #       0x01 : file received OK
    def meta_receive(self):
        if self.state_meta_received == True:
            log.warning("Dual meta send attempt")
            self.must_stop = True
            return
        if self.file_has_meta_info == False:
            log.warning("Metadata sent but meta flag was not set")
            self.must_stop = True
            return
        try:
            size = self.s.recv(4)
        except Exception,e:
            log.error("Network recv error")
            log.debug("Exception (meta size rcv) %s" % e)
            self.must_stop = True
            return
        log.debug("Receiving metadata information")
        size = struct.unpack("<L",size)[0]
        if size != self.meta_size:
            log.error("File sizes do not match")
            log.debug("Size : "+hex(size)+" (vs "+hex(self.meta_size)+")")
            self.must_stop = True
            return
        
        try:
            recv_sz = 0
            file_content = ""
            while recv_sz < self.meta_size:
                to_recv = 1024
                if self.meta_size - recv_sz < 1024:
                    to_recv = self.meta_size - recv_sz
                file_content = file_content+self.s.recv(to_recv)
                recv_sz = len(file_content)
        except Exception,e:
            log.error("Network meta recv error")
            log.debug("Exception (meta size) %s" % e)
            self.must_stop = True
            return
       
        crc32 = binascii.crc32(file_content)
        if crc32 != self.meta_crc32:
            log.error("Meta CRC32 does not match")
            log.debug("CRC32 : "+hex(crc32)+" (vs "+hex(self.meta_crc32)+")")
            self.must_stop = True
            return
        
        self.meta_temp_path = os.path.join("/tmp/",self.file_md5+".meta")
        fHandle = open(self.meta_temp_path,"w")
        fHandle.write(file_content)
        fHandle.close()
        
        self.state_meta_received = True
        tid = self.db_client.get_task_id_by_md5(self.file_md5)
        
        code = 1
        if tid == 0:
            tid = self.db_client.create_task(self.file_md5)
            if tid == 0:
                log.warning("New task could not been created, returning error code to remote client")
                code = 0 
	
        if tid != 0:
            code = add_suricata_metadata_to_task(self.db_client,self.meta_temp_path,tid,2,self.remote_source_id)
            if code != 0:
                log.info("Metadata added to task <"+str(tid)+">")
            else:
                log.warning("Metadata could not been added, returning error code to remote client")
        code = chr(code)
        
        try:
            self.s.send(code)
        except Exception,e:
            log.error("Network send error")
            log.debug("Exception %s" % e)
            self.must_stop = True
            return
        return
    
    # Thread main loop, handles connection / messages
    def run(self):
        self.db_client = db()
        if not self.db_client:
            log.critical("DATABASE initialization failure")
            exit(1)
        if self.db_client.open_db(os.path.join(ROOT_DIR,"db","db.db")) == 0:
            log.critical("DATABASE opening failure")
            exit(1)
        log.info("New connection from "+self.ip+":"+str(self.port))
        
        while(True):
            try:
                command = self.s.recv(1)
            except Exception, e:
                log.error("Network receive command error")
                log.debug("Exception %s" % e)
                self.must_stop = True
                self.stop()
                return
            if len(command) == 0:
                command = 0xFF
            else:
                command = ord(command)
            
            if command == 0x01:
                self.new_task()
            elif command == 0x02:
                self.file_receive()
            elif command == 0x03:
                self.meta_receive()
            elif command == 0x0F:
                log.info("Client has finished")
                self.must_stop = True
            elif command == 0xFF:
                log.warning("Remote connection closed")
                self.must_stop = True
            else:
                log.error("Invalid command received: "+hex(command))
                self.must_stop = True
            
            if self.must_stop == True:
                self.stop()
                return
        
        self.stop() 
        return

#
# Multi-threaded server
#
class remote_service:
    s = None
    conf = None
    hostname = ""
    port = 6666
    is_initialized = False
    threadz = []
    remote_sources = []

    # constructor
    #   - loads configuration
    def __init__(self):
        return
    
    
    # destructor
    #   - close service
    def __del__(self):
        self.stop()
        return
    
    
    # initializes service before running
    #   - initialize db, config
    def init(self):
        
        log.info("Remote service init") 

        db_client = db()
        if not db_client:
            log.critical("DATABASE initialization failure")
            exit(1)
        if db_client.open_db(os.path.join(ROOT_DIR,"db","db.db")) == 0:
            log.critical("DATABASE opening failure")
            exit(1)
        self.remote_sources = db_client.get_active_remote_sources()
        if len(self.remote_sources) == 0:
            log.critical("No available remote sources")
            exit(1)
        db_client.close()
        log.debug("Initialization OK")
        #self.hostname = socket.gethostname()
        self.hostname = "0.0.0.0"
        self.port = 6666
        self.is_initialized = True
        
        return

    
    # stop service
    #   - close database connections
    def stop(self):
        if self.is_initialized == False:
            return

        log.info("Remote service is stopping!")
        cpt = 0
        for thread in self.threadz:
            if thread.isAlive():
                thread.must_stop = True
                cpt = cpt+1        
        
        if cpt != 0:
            log.info("Killing "+str(cpt)+" active connections")
            alive = True 
            while alive == True:
                alive = False
                for thread in self.threadz:
                    if thread.isAlive():
                        alive = True
        
        log.info("All connections were closed")
        self.is_initialized = False
        self.s.close()
        return


    # main service loop
    #   - listen()
    #   - 
    def run(self):
        
        self.init()

        log.info("Remote service is running!")
        try:
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.hostname,self.port))
            self.s.listen(5)
        except Exception,e:
            log.critical("Cannot listen on "+self.hostname+":"+str(self.port)+": %s" % e)
            return

        while True:
            connection, addr = self.s.accept()
            auth = 0
            for src in self.remote_sources:
                if src[1] == addr[0]:
                    newThread = service_thread(addr[0],addr[1],connection,src[0])
                    self.threadz.append(newThread)
                    newThread.start()
                    auth = 1
           
            if auth == 0:
                log.warning("Dropping unauthorized connection from "+addr[0]+":"+str(addr[1]))
                connection.close()
        return 
