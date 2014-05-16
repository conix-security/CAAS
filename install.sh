#!/bin/bash
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

echo "EDIT ME"
exit 0

echo "[-] adding remote sources"
#./query.py --add_remote_src XX.XX.XX.XX
#./query.py --set_remote_src 1 on

echo "[-] adding cuckoo servers"
#./query.py --add_server XX.XX.XX.XX 22 username password /remote/path/

echo "[-] creating folders"
mkdir log
mkdir results
mkdir binaries

echo "[-] setting www-data proper access rights"
# deny access to anyone
chmod -R 600 ./*
# chmod +x any directories & py files to owner
find ./ -type d -exec chmod 700 {} \;
chmod 700 ./*.py
chmod 700 ./*.sh

chgrp www-data ./
chmod 750 ./

# web => www-data read only
chgrp -R www-data web
chmod -R 740 web
find ./web -type d -exec chmod 750 {} \;

# binaries => www-data read write
chgrp www-data binaries
chmod 770 binaries

# db => www-data read write
chgrp www-data db
chgrp www-data db/db.db
chmod 770 db
chmod 660 db/db.db
# log => www-data read only
chgrp www-data log
chmod -R 750 log
# results => www-data read only
chgrp www-data results
chmod 750 results

