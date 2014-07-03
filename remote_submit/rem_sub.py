#!/usr/bin/python
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
import os,sys,struct,socket,hashlib,argparse,binascii

# file types : [(MAGIC,ID),(MAGIC,ID),...]
file_types = [("PE32",1),("PDF",2),("DOC",3)]

parser = argparse.ArgumentParser()
parser.add_argument("-s","--server",help="Remote C.A.A.S server",action="store",required=True)
parser.add_argument("-p","--port",help="Remote C.A.A.S port",action="store",type=int,required=True)
parser.add_argument("-f","--file",help="Binary file to be analyzed",action="store",required=True)
parser.add_argument("-m","--meta",help="Metadata .meta file present",action="store_true",required=False)
args = parser.parse_args()

host = args.server
port = args.port
sample_path = args.file
meta_present = False
meta_path = sample_path+".meta"
meta_crc32 = 0
mdata = ""
meta_size = 0
meta_flag = 0

if not os.path.isfile(sample_path):
    print "File not found"
    exit(1)

if args.meta:
    meta_present = True
    if not os.path.isfile(meta_path):
        print "Meta file not found"
        exit(1)
    fHandle = open(meta_path,"r")
    mdata = fHandle.read()
    fHandle.close()
    meta_crc32 = binascii.crc32(mdata)
    meta_size = len(mdata)
    meta_flag = 0x01

file_type = 0xFF
output = os.popen("file \""+sample_path+"\"").read()
for ftype in file_types:
    if ftype[0] in output:
        file_type = ftype[1]

fHandle = open(sample_path,"r")
fdata = fHandle.read()
fHandle.close()

size = len(fdata)
m = hashlib.md5()
m.update(fdata)
file_md5 = m.hexdigest()

# message :
#   BYTE : operation type
#   BYTE : file type
#   DWORD : file size
#   char[32] : file MD5
#   BYTE : metadata flag (1 => is present)
message = "\x01"+chr(file_type)+struct.pack("<L",size)+file_md5+chr(meta_flag)

try:
    print "[-] Connecting to server"
    s = socket.socket()
    s.connect((host,port))
    print "[-] Sending task info"
    s.send(message)
    order = s.recv(1)
except Exception,e:
    print "[!] Network exception occured\n\t%s" % e
    exit(1)

send_file = False
order = ord(order)
if order == 0:
    print "[-] Task dropped by remote server"
    exit(1)
elif order == 1:
    print "[-] Metadata only mode"
    exit(1)
elif order == 2:
    print "[-] Task accepted by remote server"
    send_file = True
else:
    print "[!] Unknown response code: "+hex(order)
    exit(1)

if send_file:
    # send file message
    #   BYTE : operation ID
    #   DWORD : file size
    #   BYTE[] : file data
    message = "\x02"+struct.pack("<L",size)+fdata
    try:
        print "[-] Sending file to remote server"
        s.send(message)
        response = s.recv(1)
        if len(response) == 0:
            raise Exception("Received empty data")
    except Exception,e:
        print "[!] Network exception occured\n\t%s" % e
        exit(1)
    response = ord(response)
    if response == 1:
        print "[-] File successfully received by server"
    else:
        print "[!] Server could not handle the file properly (MD5 mismatch || error while processing task)"
        exit(1)

if meta_present:
    # send file meta info
    #   BYTE : operation ID
    #   DWORD : meta file size
    #   BYTE[] : file data
    message = "\x03"+struct.pack("<L",meta_size)+mdata
    try:
        print "[-] Sending meta file to remote server"
        s.send(message)
        response = s.recv(1)
        if len(response) == 0:
            raise Exception("Received empty data")
    except Exception,e:
        print "[!] Network exception occured\n\t%s" % e
        exit(1)
    response = ord(response)
    if response == 1:
        print "[-] Meta file successfully received by server"
    else:
        print "[!] Server could not handle the file properly (CRC32 mismatch || error while processing metadata)"
        exit(1)

print "[-] Closing connection"
try:
    s.send("\x0F")
    data = s.recv(1)
    s.close()
except Exception,e:
    print "[!] Network exception occured\n\t%s" % e
    exit(1)

