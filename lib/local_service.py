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

import os, time, logging

from lib.constants import ROOT_DIR
from lib.db import db
from lib.misc import handle_new_file

log = logging.getLogger(__name__)

#
# local folders service
#
class local_service:
    conf = None                 # configuration
    db_client = None            # database handle
    is_initialized = False      # initialization flag


    ################################
    # Constructor / destructor
    ################################
    
    # constructor
    def __init__(self):
        return
    
    # destructor
    def __del__(self):
        self.stop()
        return
    

    ################################
    # Init / close
    ################################
    
    # initializes service before running
    def init(self):
        log.info("Local service init") 
        self.db_client = db()
        if not self.db_client:
            log.critical("DATABASE initialization failure")
            exit(1)
        if self.db_client.open_db(os.path.join(ROOT_DIR,"db","db.db")) == 0:
            log.critical("DATABASE opening failure")
            exit(1)
        self.conf = self.db_client.get_config()
        if not self.conf:
            log.critical("CONFIGURATION initialization failure")
            exit(1)
        log.debug("Initialization OK")
        self.is_initialized = True
        return

    
    # stop service
    #   - close database connections
    def stop(self):
        if self.is_initialized == False:
            return
        log.info("Local service is stopping!")
        if self.db_client:
            self.db_client.close()
        self.is_initialized = False
        return



    ################################
    # Main
    ################################
    
    # main service loop
    #   - init DB connection
    #   - monitor for new files in submit folder
    def run(self):
        self.init()
        log.info("Local service is running!")
        while True:
            folders = self.db_client.get_active_local_sources()
            for folder_info in folders:
                if not os.path.exists(folder_info[1]):
                    log.critical(folder_info[1] + " does not exist.")
            for folder_info in folders:
                for file_name in os.listdir(folder_info[1]):
                    basename = os.path.join(folder_info[1], file_name)
                    if self.conf[0] == 1:
                        if basename[-5:] == ".meta":
                            continue
                    handle_new_file(self.db_client, basename, True, 1, folder_info[0])
                time.sleep(5)

