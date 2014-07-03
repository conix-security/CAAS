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

# shred everything!
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "[-] cleaning results"
shred -uz $DIR/results/*
echo "[-] cleaning logs"
shred -un1 $DIR/log/*
echo "[-] cleaning samples"
shred -uz $DIR/binaries/*
echo "[-] cleaning database"
shred -uz $DIR/db/db.db
echo "[-] finished"
