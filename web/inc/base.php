<?php
//  Copyright 2013 Conix Security, Nicolas Correia, Adrien Chevalier
//
//  This file is part of CAAS.
//
//  CAAS is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  CAAS is distibuted in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with CAAS.  If not, see <http://www.gnu.org/licenses/>.
if(!defined("__INCLUDED__"))
	exit(0);

@session_start();
///////////////////////////////////////////
// CONFIG
///////////////////////////////////////////
$BASE_DIR = dirname(dirname(pathinfo(__FILE__,PATHINFO_DIRNAME)));
$db_path = $BASE_DIR."/db/db.db";
$results_path = $BASE_DIR."/results/";
$bin_path = $BASE_DIR."/binaries/";
$download_cmd = $BASE_DIR."/query.py --download_report";
$error_message = "";

require_once("inc/functions.php");
if($_SERVER["REQUEST_METHOD"]=="POST")
{
	if(check_csrf() == False)
		error("CSRF POST ATTEMPT","SECURITY");	
}

require_once("inc/db.php");
init_db();
require_once("inc/display.php");
?>
