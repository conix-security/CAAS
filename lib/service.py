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
from lib.misc import download_all_available_reports
from lib.misc import handle_analysis

log = logging.getLogger(__name__)

#
# main service
#
class service:

    db_client = None                # database handle
    is_initialized = False          # initialization boolean
    reports_autodl = 0              # autodownload reports ?

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
    # Init
    ################################
    
    # initializes service before running
    def init(self):
        log.info("Main service init")
        self.db_client = db()
        if not self.db_client:
            log.critical("DATABASE initialization failure")
            exit(1)
        if self.db_client.open_db(os.path.join(ROOT_DIR,"db","db.db")) == 0:
            log.critical("DATABASE opening failure")
            exit(1)
        conf = self.db_client.get_config()
        if not conf:
            log.critical("CONFIGURATION initialization failure")
            exit(1)
        self.reports_autodl = conf[1]
        log.debug("Initialization OK")
        self.is_initialized = True
        return
    
    # stop service
    def stop(self):
        if self.is_initialized == False:
            return
        log.info("Main service is stopping!")
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
    #   - update tasks each 5 seconds
    def run(self):
        self.init()
        log.info("Main service is running!")
        while True:
            analyses = self.db_client.get_new_analyses()
            for analysis in analyses:
                analysis_id = analysis[0]
                handle_analysis(self.db_client, analysis_id)
            if self.reports_autodl == 1:
                download_all_available_reports(self.db_client)
            time.sleep(5)
            
     
