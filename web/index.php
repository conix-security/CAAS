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
define("__INCLUDED__",1);
require_once("./inc/base.php");


///////////////////////////////////////////
// DOWNLOAD OPERATIONS
///////////////////////////////////////////

// download json report
if(isset($_GET["download_json"]))
{
	$aid = $_GET["download_json"];
	$aid_s = secure_display($aid);
	$mode="usermode";
	if(isset($_GET["k"]))
		$mode="kernelmode";

	$req = get_analysis_info($aid);
	$line = $req->fetchArray();
	if($line)
	{
		$md5_hash = $line["md5"];
		$path = $results_path.$md5_hash.".".$line["analysis_id"].".json";
		if(file_exists($path))
		{
			header("Content-disposition: attachment; filename=".$md5_hash.".".$line["analysis_id"].".json");
			header("Content-type: text/json");
			readfile($path);
			exit(0);
		}
		error("Cannot find json report file ".$path,"ERROR");
	}
	else
		error("Cannot find analysis &lt;".$aid_s."&gt;","ERROR");
}
// download sample
if(isset($_GET["download_sample"]))
{
	$tid = $_GET["download_sample"];
	
	$req = get_task_md5($tid);
	$line = $req->fetchArray();
	if($line)
	{
		$md5_hash = $line["md5"];
		$path = $bin_path.$md5_hash.".bin";
		if(file_exists($path))
		{
			header("Content-disposition: attachment; filename=".$md5_hash.".bin");
			header("Content-type: application/bin");
			readfile($path);
			exit(0);
		}
	}
	$error .= "Cannot find sample<br />";
}
// pull report from remote server
if(isset($_GET["pull_report"]))
{
	$tid = $_GET["download_sample"];
	
	$req = get_task_md5($tid);
	$line = $req->fetchArray();
	if($line)
	{
		$name = "usermode";
		if(isset($_GET["k"]))
			$name = "kernelmode";
		
		// close DB so the script can write it
		close_db();	
		$error .= system($download_cmd." ".$line["task_id"],$retval);
		if($retval == 0)
			$error .= "Download error: System command error<br />";
		
		// reopen it!
		open_db();
		
		$md5_hash = $line["md5"];
		$path = $results_path.$md5_hash.".".$name.".json";
		if(!file_exists($path))
			$error.="Download error: file not found<br />";
	}
	else
		$error .= "Error: Cannot find report file for task &lt;".$tid."&gt;";
}



///////////////////////////////////////////
// HTML HEADER
///////////////////////////////////////////

display_header();


if(isset($_GET["display_task"]))
{
	$tid = $_GET["display_task"];
	display_task($tid);
	
}
elseif(isset($_GET["display_json"]))
{
	$tid = $_GET["display_json"];
	display_analysis($tid,True);
}
elseif(isset($_GET["display_analysis"]))
{
	$tid = $_GET["display_analysis"];
	display_analysis($tid);
}
elseif(isset($_GET["config"]))
{
	display_config();
}
elseif(isset($_GET["search"]))
{
	display_search();
}
elseif(isset($_GET["meta_sign"]))
{
	display_meta_sign();
}
elseif(isset($_GET["sql_query"]))
{
	display_sql_query();
}
elseif(isset($_GET["display_tasks"]))
{
	display_tasks();
}
else
{
	display_main();
}

///////////////////////////////////////////
// TASKS LISTING
///////////////////////////////////////////

display_footer();
?>
