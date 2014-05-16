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
import copy
import logging
import logging.handlers

from lib.constants import ROOT_DIR

log = logging.getLogger()

#
# logging stuff, mostly copied on the cuckoo lib/cuckoo/core/startup.py :]
#

def color(text, color_code):
   return "\x1b[%dm%s\x1b[0m" % (color_code, text)

def red(text):
    return color(text, 31)

def green(text):
    return color(text, 32)

def yellow(text):
    return color(text, 33)

def cyan(text):
    return color(text, 36)

class ConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        colored = copy.copy(record)
        if "Secsh channel" in record.msg:
            return
        if record.levelname == "WARNING":
            colored.msg = yellow(record.msg)
        elif record.levelname == "ERROR" or record.levelname == "CRITICAL":
            colored.msg = red(record.msg)
        elif record.levelname == "DEBUG":
            colored.msg = record.msg
        else:
            if "New task with" in record.msg or "eport downloaded" in record.msg or "finished!" in record.msg:
                colored.msg = cyan(record.msg)
            elif "Operation succeeded" in record.msg:
                colored.msg = green(record.msg)
            else:
                colored.msg = record.msg
        logging.StreamHandler.emit(self, colored)

def init_log(name):
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    fh = logging.handlers.WatchedFileHandler(os.path.join(ROOT_DIR, "log", name+".log"))
    fh.setFormatter(formatter)
    log.addHandler(fh)
    ch = ConsoleHandler()
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(logging.INFO)
