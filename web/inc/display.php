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

$dt_menu_class = "menu";
$config_menu_class = "menu";
$search_menu_class = "menu";
$alerts_menu_class = "menu";
$sql_menu_class = "menu";
$meta_menu_class = "menu";
$main_menu_class = "menu";
if(isset($_GET['display_tasks']) || isset($_GET['display_task']) || isset($_GET['display_analysis']) || isset($_GET['display_json']))
	$dt_menu_class = "menu_selected";
elseif(isset($_GET['config']))
	$config_menu_class = "menu_selected";
elseif(isset($_GET['search']))
	$search_menu_class = "menu_selected";
elseif(isset($_GET['display_alerts']))
	        $alerts_menu_class = "menu_selected";
elseif(isset($_GET['sql_query']))
	$sql_menu_class = "menu_selected";
elseif(isset($_GET['meta_sign']))
	$meta_menu_class = "menu_selected";
else
	$main_menu_class = "menu_selected";

$header = '<html>
    <script language="javascript" type="text/javascript">function hidz(id){ obj=document.getElementById(id); if(obj.style.display == "none"){ obj.style.display="table";}else{obj.style.display="none"; }}
    </script>
    <style>
        .small{
            font-size: 10px;
        }
        body{
            background: #ffffff;
            color: #333333;
            font-family: "Lucida Sans","Lucida Grande",Lucida,sans-serif,Verdana;
            font-size: 12px;
            padding: 0px;
            margin: 0px;
        }
        h1{
            margin-bottom: 15px;
            padding: 5px;
            font-size: 12px;
            font-weight: bold;
            text-align: left;
            border: 1px solid #CCCCCC;
            background: #F2F2F2;
        }
        h2{
            font-weight: bold;
            font-size: 110%;
            text-align: left;
            padding: 2px;
	    border-top: solid 1px black;
	    border-bottom: solid 1px black;
        }
	div.container100{
	    width: 100%;
	}
	table{
	}
	table.inside_table{
	    width: 100%;
	}
        table.std{
	    min-width: 820px;
            background: #fcfcfc;
            color: #333333;
            border: 1px solid #e4e4e4;
            text-align:left;
            border-spacing: 0px;
	    margin: 5px;
         }
	table.center{
	    margin: auto;
	    width: auto;
	}
	th{
	}
        th.std{
            font-size:11px;
            color:#4A4948;
            font-weight:bold;
            text-align:center;
            min-height:20px;
	    min-width: 100px;
            background:#c4c0BB;
            padding: 2px;
        }
	td{
            margin: 0px;
            color:#333333;
            padding: 2px;
            font-size:11px;
	    text-align: center;
	}
        td.std{
	    min-width: 700px;
	    text-align: left;
        }
        tr:hover{
            background:#d4d0CC;
        }
        tr.selected{
            background:#c4c0BB;
        }
        div.center{
            text-align: center;
            margin: auto;
        }
	span.warning{
            color:orange;
            font-weigth:bold;
	}
	span.info{
            color:green;
            font-weigth:bold;
	}
	span.error{
            color:red;
            font-weigth:bold;
	}
	span.alert{
	    color:red;
	}
	span.okay{
	    color: green;
	}
	td.alert{
            color:red;
	}
	td.warning{
	    color: orange;
	}
	td.okay{
	    color: green;
	}
	a.menu{
	    color: black;   
	}
	a.menu_selected{
	    color: red;
	}
    </style> 
    <body id="body_scroll">
	<h1>
		<a href="'.$_SERVER['PHP_SELF'].'" class="'.$main_menu_class.'">HOME</a>&nbsp;
                <a href="'.$_SERVER['PHP_SELF'].'?display_alerts" class="'.$alerts_menu_class.'">ALERTS</a>&nbsp;
		<a href="'.$_SERVER['PHP_SELF'].'?display_tasks" class="'.$dt_menu_class.'">TASKS</a>&nbsp;
		<a href="'.$_SERVER['PHP_SELF'].'?config" class="'.$config_menu_class.'">CONFIG</a>&nbsp;
		<a href="'.$_SERVER['PHP_SELF'].'?search" class="'.$search_menu_class.'">SEARCH</a>&nbsp;
		<a href="'.$_SERVER['PHP_SELF'].'?sql_query" class="'.$sql_menu_class.'">SQL QUERY</a>
		<a href="'.$_SERVER['PHP_SELF'].'?meta_sign" class="'.$meta_menu_class.'">RULES</a>
	</h1>';
$footer = '
    </body>
</html>';
$notify_begin = "
	<h1>NOTIFY</h1>";
$notify_end = "<br />";
$notify_error = '
		<span class="error">ERROR:</span> ';
$notify_warning = '
		<span class="warning">WARNING:</span> ';
$notify_info = '
		<span class="info">INFO:</span> ';
$notify_message = "";
$notify_separator = "<br />";
$header_printed = False;
$footer_printed = False;
$tasks_header = "
	<h1>TASKS</h1>";
$tasks_footer = "
	<br />";
function display_header()
{
	global $header,$notify_begin,$notify_end,$notify_message,$header_printed;
	if($header_printed)
		return;
	echo $header;
	if($notify_message != "")
		echo $notify_begin.$notify_message.$notify_end;
	$header_printed = True;
}
function display_footer()
{
	global $footer,$footer_printed;
	if($footer_printed)
		return;
	echo $footer;
	$footer_printed = True;
}
function append_message($msg,$type="NOTIFY")
{
	global $notify_message,$notify_separator,$notify_error,$notify_warning,$notify_info;
	
	if($notify_message != "")
		$notify_message .= $notify_separator;
	if($type == "ERROR" || $type == "CRITICAL")
		$notify_message .= $notify_error;
	elseif($type == "WARNING")
		$notify_message .= $notify_warning;
	else
		$notify_message .= $notify_info;
	$notify_message .= $msg;
}
function secure_display($data)
{
	return htmlentities($data);
}
function display_task($task_id)
{
	global $task_header_1,$task_header_2,$task_footer;
	
	$task_id_s = secure_display($task_id);	
	$req = get_task_md5($task_id);
	if(!$req)
		return;
	$res = $req->fetchArray();
	echo '<h1>TASK #'.$task_id_s.' : '.secure_display($res['md5']).'</h1>';
	echo '<h2>TASK INFO</h2>
	<div class="container100">
	<table class="std">
		<tr><th class="std">MD5</th><td class="std">'.secure_display($res['md5']).'</td></tr>
		<tr><th class="std">DOWNLOAD</th><td class="std"><a href="'.$_SERVER['PHP_SELF'].'?download_sample='.$task_id_s.'">download sample</a></td></tr>
	</table>
	</div>
	<h2>METADATA</h2>';
	display_metadata($task_id,False);
	echo '<h2>ANALYSES</h2>';
	display_task_analyses($task_id,False);
}
function display_metadata($task_id,$display_header)
{
	global $metadata_footer,$metadata_header_1,$metadata_header_2;
	$task_id_s = secure_display($task_id);
	
	$req = get_task_metadata($task_id);
	if(!$req)
		return;
	while($line = $req->fetchArray())
	{
		echo '
<div class="container100"><table class="std">
	<tr><th class="std">TIME</th><td class="std">'.secure_display($line['time']).'</td></tr>';
	if($line['src_ip']!='')
		echo '
	<tr><th class="std">SRC ip:port</th><td class="std">'.secure_display($line['src_ip']).':'.secure_display($line['src_port']).'</td></tr>';
	if($line['dst_ip']!='')
		echo '
	<tr><th class="std">DST ip:port</th><td class="std">'.secure_display($line['dst_ip']).':'.secure_display($line['dst_port']).'</td></tr>';
	if($line['host']!='')
		echo '
	<tr><th class="std">HOST</th><td class="std">'.secure_display($line['host']).'</td></tr>';
	if($line['uri']!='')
		echo '
	<tr><th class="std">DOWNLOAD URI</th><td class="std">'.secure_display($line['uri']).'</td></tr>';
	if($line['filename']!='')
		echo '
	<tr><th class="std">FILENAME</th><td class="std">'.secure_display($line['filename']).'</td></tr>';
	if($line['referer']!='')
		echo '
	<tr><th class="std">REFERER</th><td class="std">'.secure_display($line['referer']).'</td></tr>';
	if($line['user_agent']!='')
		echo '
	<tr><th class="std">USER AGENT</th><td class="std">'.secure_display($line['user_agent']).'</td></tr>';
	if($line['proto']!=0)
		echo '
	<tr><th class="std">PROTOCOL</th><td class="std">'.secure_display($line['proto']).'</td></tr>';
	if($line['magic']!='')
		echo '
	<tr><th class="std">SURICATA MAGIC</th><td class="std">'.secure_display($line['magic']).'</td></tr>';
	if($line['sz']!=0)
		echo '
	<tr><th class="std">SIZE</th><td class="std">'.secure_display($line['sz']).'bytes</td></tr>';

	$source_data = get_source_info($line['source_type'],$line['source_id']);
	echo '
	<tr><th class="std">SOURCE</th><td class="std">'.$source_data.'</td></tr>';
	echo '
</table></div>';
	}
}
function get_source_info($source_type,$source_id,$raw=FALSE)
{
	$source_type_data = get_source_type_title($source_type);
	if($source_type_data)
	{
		$source_type_info = $source_type_data->fetchArray();
		if($source_type_info)
		{
			if($source_type_info['title'] == "manual")
			{
				if(!$raw)
					return "MANUAL SUBMISSION";
				else
					return "MANUAL";
			}
			if($source_type_info['title'] == "local")
			{
				$source_data = get_local_source($source_id);
				if($source_data)
				{
					$source_info = $source_data->fetchArray();
					if($source_info)
					{
						if(!$raw)
							return "LOCAL SUBMISSION FROM ".secure_display($source_info["lookup_folder"]);
						else
							return "LOCAL: ".secure_display($source_info["lookup_folder"]);
					}
				}
			}
			elseif($source_type_info['title'] == "remote")
			{
				$source_data = get_remote_source($source_id);
				if($source_data)
				{
					$source_info = $source_data->fetchArray();
					if($source_info)
					{
						if(!$raw)
							return "REMOTE SUBMISSION FROM ".secure_display($source_info["remote_ip_addr"]);
						else
							return "REMOTE: ".secure_display($source_info["remote_ip_addr"]);
					}
				}
			}
		}
	}
	return "UNDEFINED";
}
function display_json_info($path)
{
        $report = @file_get_contents($path,NULL,NULL,0,10000000);
        if(!$report)
	{
		error('report file not found <'.$path.'>',"ERROR");
		return;
	}
	$json = json_decode($report,true);
        if($json == NULL)
        {
                error('json decoding error',"ERROR");
                return;
        }
	
        foreach($json as $key => $val)
        {
                if(is_array($val) && $key!="debug" && $key!="strings")
                {
                        echo '
    <h2 onclick="hidz(\''.strtoupper(secure_display($key)).'\');">'.strtoupper(secure_display($key)).'</h2>
        <table id="'.strtoupper(secure_display($key)).'" style="display: none;">';
                        recursive_json_print($val,0,$key);
                        echo '
        </table>';
                }
        }

}
function recursive_json_print($value,$nbspaces,$category)
{
	$decz = "";
        for($i=0;$i<$nbspaces;$i++)
                $decz.='<td></td>';

        foreach($value as $key => $val)
        {
                if(is_array($val) && !empty($val))
                {
                        if($category == "behavior" && ($key == "processes" || $key == "processtree"))
                                continue;

                        if(is_int($key))
                        {
                                if($category == "signatures")
                                        echo '
            <tr><td>&nbsp;</td></tr>';

                                recursive_json_print($val,$nbspaces,$category);

                        }
                        else
                        {
                                echo '
            <tr>'.$decz.'<td>'.secure_display($key).'</td></tr>';
                                recursive_json_print($val,$nbspaces+1,$category);
                        }
                }
                elseif(!empty($val) && $val!="")
                {
                        echo '
            <tr>'.$decz.'<td>'.secure_display($key).'</td><td>'.secure_display($val).'</td></tr>';
                }
        }

}
function display_main()
{
	$task_id = 0;
	if(isset($_FILES["sample"]))
	{
		if ($_FILES["sample"]["error"] > 0)
			error("[display_main] File upload error","ERROR");
		else
		{
			$new_path = '/tmp/caas_upload_tmp/'.md5_file($_FILES["sample"]["tmp_name"]);
			if(!is_dir('/tmp/caas_upload_tmp/'))
				@mkdir('/tmp/caas_upload_tmp/');
			if(!@move_uploaded_file($_FILES["sample"]["tmp_name"],$new_path))
				error("[display_main] move file error","ERROR");
			else
				$task_id = new_task($new_path);
		}
	}

	echo '
	<h1>MANUAL SUBMISSION</h1>';
	if($task_id != 0)
		echo '
	New task with ID #'.secure_display($task_id).' created.';
	echo '<form action="" method="POST" enctype="multipart/form-data">'.gen_csrf().'<input type="file" name="sample" /><input type="submit" value="Submit" /></form>';
}
function display_alerts()
{
        global $tasks_header,$tasks_footer;
        echo $tasks_header;

        $start = 0;
        $count = 10;
        $start_s = 0;
        $count_s = 10;
        if(isset($_GET["st"]) && isset($_GET["nb"]))
        {
                $start = $_GET["st"];
                $count = $_GET["nb"];
                $start_s = intval($_GET["st"]);
                $count_s = intval($_GET["nb"]);
        }
        $alert_count = get_alerts_count();
        $nb_pages = $alert_count / $count_s;
        $alertz = get_alertz($start,$count); // security checks done in db.php :]
        echo '
            <div class="container100">
                <table class="std">
                <tr><th class="std">CRITICITY</th><th class="std">LABEL</th><th class="std">DESCRIPTION</th><th class="std">TASK</th></tr>';
        while($alert = $alertz->fetchArray())
        {
                $criticity = '<span style="color:green">Low</span>';
                if($alert['criticity'] == 2)
                        $criticity = '<span style="color:orange">Medium</span>';
                elseif($alert['criticity'] == 1)
                        $criticity = '<span style="color:red">High</span>';
                echo '<tr><td>'.$criticity.'</td><td>'.secure_display($alert['label']).'</td><td>'.secure_display($alert['description']).'</td><td><a href="'.$_SERVER['PHP_SELF'].'?display_task='.intval($alert['task_id']).'">'.secure_display($alert['task_id']).'</a></td></tr>';
        }
        echo '
                </table>
                <a href="'.$_SERVER['PHP_SELF'].'?display_alerts&st='.($start_s - $count_s).'&nb='.$count_s.'">&lt;--</a>&nbsp;
                <a href="'.$_SERVER['PHP_SELF'].'?display_alerts&st='.($start_s + $count_s).'&nb='.$count_s.'">&gt;--</a>
                <br />
                <form action="'.$_SERVER['PHP_SELF'].'" method="GET">
                        <input type="hidden" name="display_alerts" />
                        PAGE <select name="st" />';
        for($i = 0; $i < $nb_pages; $i++)
        {
                $sel = '';
                if($i*$count_s == $start_s)
                        $sel = " selected ";
                echo '<option value="'.$i*$count_s.'"'.$sel.'>'.($i + 1).'</option>';
        }

        echo '</select><input type="submit" value="OK" />
                        Display <select name="nb">';
        if($count_s != 10)
                echo '
                                <option value="'.$count_s.'">'.$count_s.'</option>';
        echo '
                                <option value="10">10</option>
                                <option value="20">20</option>
                                <option value="50">50</option>
                                <option value="100">100</option>
                        </select> results.
                </form>
         </div>';
}
function display_analysis($analysis_id,$display_json=False)
{
	global $states,$results_path;
	$analysis_id_s = secure_display($analysis_id);
		
	$get_analysis_info_result = get_analysis_info($analysis_id);
	if(!$get_analysis_info_result)
		return;
	$analysis_info = $get_analysis_info_result->fetchArray();
	
	display_task($analysis_info["task_id"]);
	
	echo '<h2>#'.$analysis_id_s.' ANALYSIS INFO</h2>';

	$cuckoo_server_id = $analysis_info["cuckoo_server_id"];
	$get_cuckoo_server_info_result = get_cuckoo_server_info($cuckoo_server_id);
	$cuckoo_server = "NOT FOUND";
	if($get_cuckoo_server_info_result)
	{
		$cuckoo_server_info = $get_cuckoo_server_info_result->fetchArray();
		$cuckoo_server = '#'.secure_display($cuckoo_server_info["cuckoo_server_id"]).' '.$cuckoo_server_info["name"].' '.$cuckoo_server_info["server_addr"];
	}
	$kernl = intval($analysis_info["kernel_analysis"]);
	$mode = "usermode";
	if($kernl == 1)
		$mode = "kernelmode";
	$score = intval($analysis_info["total_score"]);
	$state = intval($analysis_info["state"]);
	echo '
	<div class="container100"><table class="std">
		<tr><th class="std">STATE</th><td class="std">'.$states[$state].'</td></tr>
		<tr><th class="std">MODE</th><td class="std">'.$mode.'</td></tr>
		<tr><th class="std">CUCKOO SERVER</th><td class="std">'.$cuckoo_server.'</td></tr>
		<tr><th class="std">TOTAL SCORE</th><td class="std"><span class="'.get_score_class($score,$kernl).'">'.$score.'</span></td></tr>
		<tr><th class="std">SIGNATURES (score)</th><td class="std">';
	$get_matched_signatures_result = get_matched_signatures($analysis_id);
	if($get_matched_signatures_result)
	{
		while($signature_info = $get_matched_signatures_result->fetchArray())
		{
			echo secure_display($signature_info['title']).' ('.secure_display($signature_info['score']).')<br />';
		}
	}
	echo '</td></tr>
		<tr><td colspan="2"><a href="'.$_SERVER['PHP_SELF'].'?download_json='.$analysis_id_s.'">Download JSON report</a></td></tr>
		<tr><td colspan="2"><a href="'.$_SERVER['PHP_SELF'].'?display_json='.$analysis_id_s.'">Display JSON data</a></td></tr>
	</table></div>';
	if($display_json)
	{
		echo '
	<div class="container100">';
		$json_path = $results_path.$analysis_info["md5"].".".$analysis_info["analysis_id"].".json";
		display_json_info($json_path);
		echo '
	</div>';
	}
}
function display_config()
{
	global $enable_usermode_analysis,$enable_kernelmode_analysis,$parse_metadata,$autodownload_reports,$kernelmode_score_medium,$kernelmode_score_high,$usermode_score_medium,$usermode_score_high,$kernelmode_timeout,$usermode_timeout,$sampling;
	echo '
	<h1>CONFIGURATION</h1>
        <h2 style="color:red;">NOT FUNCTIONAL</h2>';
	$form_b = '';
	$form_e = '<a href="'.$_SERVER['PHP_SELF'].'?config&edit_main">EDIT</a>';
	if(!isset($_GET["edit_main"]))
	{
			$usermode = "Disabled";
		if($enable_usermode_analysis == 1)
			$usermode = "Enabled";
		$usermode .= ", ".$usermode_timeout.' seconds timeout (scoring rules: <span style="color:orange">'.$usermode_score_medium.'</span> / <span style="color:red;">'.$usermode_score_high."</span>)";
		$krnlmode = "Disabled";
		if($enable_kernelmode_analysis == 1)
			$krnlmode = "Enabled";
		$krnlmode .= ", ".$kernelmode_timeout.' seconds timeout (scoring rules: <span style="color:orange">'.$kernelmode_score_medium.'</span> / <span style="color:red;">'.$kernelmode_score_high."</span>)";
		$autodl = "Disabled";
		if($autodownload_reports == 1)
			$autodl = "Enabled";
		$meta = "Disabled";
		if($parse_metadata)
			$meta = "Enabled";
	}
	else
	{
		$form_b = '<form action="'.$_SERVER["PHP_SELF"].'?config" method="POST">'.gen_csrf();
		$form_e = '<input type="submit" name="main_modif" value="OK" /></form>';
		if($autodownload_reports == 1)
			$autodl = '<select name="autodl"><option value="enabled">Enabled</option><option value="disabled">Disabled</option></select>';
		else
			$autodl = '<select name="autodl"><option value="disabled">Disabled</option><option value="enabled">Enabled</option></select>';
		if($enable_usermode_analysis == 0)
			$usermode = '<select name="enable_user"><option value="disabled">Disabled</option><option value="enabled">Enabled</option></select>';
		else
			$usermode = '<select name="enable_user"><option value="enabled">Enabled</option><option value="disabled">Disabled</option></select>';
		$usermode.= '<input type="text" size="1" name="user_timeout" value="'.$usermode_timeout.'" />s timeout (<input type="text" size="2" name="user_warn_limit" value="'.$usermode_score_medium.'" style="color:orange;" /> / <input type="text" size="2" name="user_alert_limit" value="'.$usermode_score_high.'" style="color:red;" />)';
		if($enable_kernelmode_analysis == 0)
			$krnlmode = '<select name="enable_krnel"><option value="disabled">Disabled</option><option value="enabled">Enabled</option></select>';
		else
			$krnlmode = '<select name="enable_krnel"><option value="enabled">Enabled</option><option value="disabled">Disabled</option></select>';
		$krnlmode.= '<input type="text" size="1" name="user_timeout" value="'.$kernelmode_timeout.'" />s timeout (<input type="text" size="2" name="user_warn_limit" style="color:orange" value="'.$kernelmode_score_medium.'" /> / <input type="text" size="2" name="user_alert_limit" style="color:red;" value="'.$kernelmode_score_high.'"/>)';
		if(!$parse_metadata)
			$meta = '<select name="parse_meta"><option value="disabled">Disabled</option><option value="enabled">Enabled</option></select>';
		else
			$meta = '<select name="parse_meta"><option value="enabled">Enabled</option><option value="disabled">Disabled</option></select>';
	}
	echo '
	<h2>Main config</h2>
	<div class="container100">'.$form_b.'<table class="std">
		<tr><th class="std">SETTING</th><th class="std">VALUE</th></tr>
		<tr><td>USERMODE ANALYSIS</td><td>'.$usermode.'</td></tr>
		<tr><td>KERNELMODE ANALYSIS</td><td>'.$krnlmode.'</td></tr>
		<tr><td>SAMPLING RATE</td><td>'.$sampling.'%</td></tr>
		<tr><td>REPORTS AUTODOWNLOAD</td><td>'.$autodl.'</td></tr>
		<tr><td>METADATA</td><td>'.$meta.'</td></tr>
		<tr><td colspan="2">'.$form_e.'</td></tr>
	</table></div>';

	echo '
	<h2>Cuckoo servers</h2>
	<div class="container100"><table class="std">
		<tr><th class="std">ADDRESS:PORT</th><th class="std">USERNAME</th><th class="std">CUCKOO PATH</th><th class="std">ACTIVE</th><th class="std">ACTION</th></tr>';
	$req = get_cuckoo_servers();
	while($res = $req->fetchArray())
	{
		$active = 'No';
		$link = "enable";
		if($res["is_active"]==1)
		{
			$active = "Yes";
			$link = "disable";
		}
		echo '<tr><td>'.secure_display($res["server_addr"]).':'.secure_display($res["ssh_port"]).'</td><td>'.secure_display($res["username"]).'</td><td>'.secure_display($res["cuckoo_path"]).'</td><td>'.$active.'</td><td><a href="'.$_SERVER["PHP_SELF"].'?config&'.$link.'_cuckoo_server='.secure_display($res["cuckoo_server_id"]).'">'.$link.'</a></td></tr>';
	}	
	echo '<form action="'.$_SERVER['PHP_SELF'].'?config" method="POST">'.gen_csrf().'<tr><td><input type="text" name="ip_addr" size="11" />:<input type="text" name="port" size="4" /></td><td><input type="text" name="username" value="username" size="7"/>:<input type="password" name="pass" value="********************" /></td><td><input type="text" name="path" value="/path/to/cuckoo" /></td><td colspan="2"><input type="submit" name="add_cuckoo_server" value="Add" /></td></tr></form>
	</table></div>
	<h2>Local sources</h2>
	<div class="container100"><table class="std">
		<tr><th class="std">FOLDER</th><th class="std">ACTIVE</th><th class="std">ACTION</th></tr>';
	$req = get_local_sources();
	while($res = $req->fetchArray())
	{
		$active = "No";
		$link = "enable";
		if($res["is_active"]==1)
		{
			$active = "Yes";
			$link = "disable";
		}
		echo '<tr><td>'.secure_display($res["lookup_folder"]).'</td><td>'.$active.'</td><td><a href="'.$_SERVER["PHP_SELF"].'?config&'.$link.'_cuckoo_server='.secure_display($res["local_source_id"]).'">'.$link.'</a></td></tr>';
	}	
	echo '<form action="'.$_SERVER['PHP_SELF'].'?config" method="POST">'.gen_csrf().'<tr><td><input type="text" name="lookup_folder" size="11" value="/lookup/folder" /></td><td colspan="2"><input type="submit" name="add_local_source" value="Add" /></td></tr></form>
	</table></div>
	<h2>Remote sources</h2>
	<div class="container100"><table class="std">
		<tr><th class="std">ADDRESS</th><th class="std">ACTIVE</th><th class="std">ACTION</th></tr>';
	$req = get_remote_sources();
	while($res = $req->fetchArray())
	{
		$active = "No";
		$link = "enable";
		if($res["is_active"]==1)
		{
			$active = "Yes";
			$link = "disable";
		}
		echo '<tr><td>'.secure_display($res["remote_ip_addr"]).'</td><td>'.$active.'</td><td><a href="'.$_SERVER["PHP_SELF"].'?config&'.$link.'_cuckoo_server='.secure_display($res["remote_source_id"]).'">'.$link.'</a></td></tr>';
	}	
	echo '<form action="'.$_SERVER['PHP_SELF'].'?config" method="POST">'.gen_csrf().'<tr><td><input type="text" name="remote_ip_addr" size="11" /></td><td colspan="2"><input type="submit" name="add_remote_source" value="Add" /></td></tr></form>
	</table></div>';
}
function display_search()
{

	$md5 = "";
	$signature = "";
	$score_k = "";
	$score_u = "";
	$time_start = "";
	$time_end = "";
	$src_ip = "";
	$dst_ip = "";
	$src_port = "";
	$host = "";
	$uri = "";
	$filename = "";
	$referer = "";
	$user_agent = "";
	$proto = "";
	$source = "";
	$score_op_k = "";
	$score_op_u = "";
	$score_op_k_msg = "";
	$score_op_u_msg = "";
	$results = "";
	if(isset($_POST["SEARCH"]))
	{
		$sql_request_select = "SELECT t.task_id,t.md5";
		$sql_request_from = " FROM task t";
		$sql_request_where = "";
		$analysis_table = False;
		$signature_table = False;
		$metadata_table = False;
		if(isset($_POST["md5"]) && !empty($_POST["md5"]))
		{
			$md5 = secure_display($_POST["md5"]);
			$sql_request_where .= "AND t.md5 LIKE '".secure_sql($_POST['md5'])."' ";
		}		
	
		if(isset($_POST["score_op_u"]) && !empty($_POST["score_op_u"]) && isset($_POST["score_u"]) && !empty($_POST["score_u"]))
		{
			$score_op_u = secure_display($_POST["score_op_u"]);
			if($score_op_u == "less_or_equal")
				$op = "<=";
			elseif($score_op_u == "higher_or_equal")
				$op = ">=";
			else
				$op = "=";
			$analysis_table = True;
			$signature_table = True;
			$sql_request_where .= "AND s.score ".$op." '".secure_sql($_POST["score_u"])."' AND a.kernel_analysis = '0' ";
		}
		if(isset($_POST["score_op_k"]) && !empty($_POST["score_op_k"]) && isset($_POST["score_k"]) && !empty($_POST["score_k"]))
		{
			$score_op_k = secure_display($_POST["score_op_k"]);
			if($score_op_k == "less_or_equal")
				$op = "<=";
			elseif($score_op_k == "higher_or_equal")
				$op = ">=";
			else
				$op = "=";
			$analysis_table = True;
			$signature_table = True;
			$sql_request_where .= "AND s.score ".$op." '".secure_sql($_POST["score_k"])."' AND a.kernel_analysis = '1' ";
		}
		if(isset($_POST["score_op_u"]) && !empty($_POST["source_op_u"]))
			$score_op_u = secure_display($_POST["score_op_u"]);
		if(isset($_POST["signature"]) && !empty($_POST["signature"]))
		{
			$analysis_table = True;
			$signature_table = True;
			$signature = secure_display($_POST["signature"]);
			$sql_request_where .= "AND s.title LIKE '".secure_sql($_POST["signature"])."' ";
		}		
		if(isset($_POST["score_k"]) && !empty($_POST["score_k"]))
			$score_k = secure_display($_POST["score_k"]);
		if(isset($_POST["score_u"]) && !empty($_POST["score_u"]))
		{
			$analysis_table = True;
			$score_u = secure_display($_POST["score_u"]);
			$sql_request_where .= "AND s.score = '".secure_sql($_POST["score_u"])."' AND a.kernel_analysis = '0' ";
		}
		if(isset($_POST["time_start"]) && !empty($_POST["time_start"]))
			$time_start = secure_display($_POST["time_start"]);
		if(isset($_POST["time_end"]) && !empty($_POST["time_end"]))
			$time_end = secure_display($_POST["time_end"]);
		if(isset($_POST["src_ip"]) && !empty($_POST["src_ip"]))
		{
			$metadata_table = True;
			$src_ip = secure_display($_POST["src_ip"]);
			$sql_request_where .= "AND m.src_ip LIKE '".secure_sql($_POST["src_ip"])."' ";
		}		
		if(isset($_POST["dst_ip"]) && !empty($_POST["dst_ip"]))
		{
			$metadata_table = True;
			$dst_ip = secure_display($_POST["dst_ip"]);
			$sql_request_where .= "AND m.dst_ip LIKE '".secure_sql($_POST["dst_ip"])."' ";
		}		
		if(isset($_POST["src_port"]) && !empty($_POST["src_port"]))
		{
			$metadata_table = True;
			$src_port = secure_display($_POST["src_port"]);
			$sql_request_where .= "AND m.src_port LIKE '".secure_sql($_POST["src_port"])."' ";
		}		
		if(isset($_POST["host"]) && !empty($_POST["host"]))
		{
			$metadata_table = True;
			$host = secure_display($_POST["host"]);
			$sql_request_where .= "AND m.host LIKE '".secure_sql($_POST["host"])."' ";
		}
		if(isset($_POST["uri"]) && !empty($_POST["uri"]))
		{
			$metadata_table = True;
			$uri = secure_display($_POST["uri"]);
			$sql_request_where .= "AND m.uri LIKE '".secure_sql($_POST["uri"])."' ";
		}
		if(isset($_POST["fname"]) && !empty($_POST["fname"]))
		{
			$metadata_table = True;
			$filename = secure_display($_POST["fname"]);
			$sql_request_where .= "AND m.filename LIKE '".secure_sql($_POST["fname"])."' ";
		}
		if(isset($_POST["referer"]) && !empty($_POST["referer"]))
		{
			$metadata_table = True;
			$referer = secure_display($_POST["referer"]);
			$sql_request_where .= "AND m.referer LIKE '".secure_sql($_POST["referer"])."' ";
		}
		if(isset($_POST["user_agent"]) && !empty($_POST["user_agent"]))
		{
			$metadata_table = True;
			$user_agent = secure_display($_POST["user_agent"]);
			$sql_request_where .= "AND m.user_agent LIKE '".secure_sql($_POST["user_agent"])."' ";
		}
		if(isset($_POST["proto"]) && !empty($_POST["proto"]))
		{
			$metadata_table = True;
			$proto = secure_display($_POST["proto"]);
			$sql_request_where .= "AND m.proto LIKE '".secure_sql($_POST["proto"])."' ";
		}
		if(isset($_POST["source"]) && !empty($_POST["source"]))
		{
			$metadata_table = True;
			$source = secure_display($_POST["source"]);
			$sql_request_where .= "AND m.source_type LIKE '".secure_sql($_POST["source"])."' ";
		}
		if(substr($sql_request_where,0,4) == "AND ")
			$sql_request_where = substr($sql_request_where,3,-1);
		if($metadata_table == True)
		{
			$sql_request_where = "t.task_id = m.task_id AND ".$sql_request_where;
			$sql_request_from.=",metadata m";
		}
		if($analysis_table == True)
		{
			$sql_request_where = "t.task_id = a.task_id AND ".$sql_request_where;
			$sql_request_from.=",analysis a";
		}
		if($signature_table == True)
		{
			$sql_request_where = "s.analysis_id = a.analysis_id AND ".$sql_request_where;
			$sql_request_from.=",signature s";
		}
		
		$sql_request_end = " GROUP BY t.task_id ORDER BY t.task_id ASC LIMIT 0,10";		
		if(trim($sql_request_where) != "")
			$sql_request_where = ' WHERE '.$sql_request_where;
		$sql_request_full = $sql_request_select.$sql_request_from.$sql_request_where.$sql_request_end;
		$data = query_db($sql_request_full);
		$results .= '<h2>RESULTS</h2>
		<table class="std">
			<tr><th class="std">ID</th><th class="std">MD5</th></tr>';
		while($res = $data->fetchArray())
			$results .= '
			<tr><td>'.secure_display($res['task_id']).'</td><td>'.secure_display($res["md5"]).'</td></tr>';
		$results .= '
		</table>';
	}

	echo '<h1>SEARCH FOR TASKS</h1>
	NB: input data is in LIKE SQL statements, use "%" as wildcards.<br />
	<form action="'.$_SERVER['PHP_SELF'].'?search" method="POST">'.gen_csrf().'
	<table>
		<tr><td colspan="2"><input type="submit" name="SEARCH" value="SEARCH" /></td></tr>
		<tr><th class="std">MD5</td><td class="std"><input type="TEXT" name="md5" value="'.$md5.'" /></td></tr>
		<tr><th class="std">SIGNATURE</td><td class="std"><input type="TEXT" name="signature" value="'.$signature.'" /></td></tr>
		<tr><th class="std">KERNELMODE SIGN SCORE</td><td class="std">
			<select name="score_op_k">'.$score_op_k_msg.'
				<option value="higher_or_equal">&gt;=</option>
				<option value="less_or_equal">&lt;=</option>
				<option value="equal">=</option>
			</select>
			<input type="TEXT" name="score_k" value="'.$score_k.'" /></td></tr>
		<tr><th class="std">USERMODE SIGN SCORE</td><td class="std">'.$score_op_u_msg.'
			<select name="score_op_u">
				<option value="higher_or_equal">&gt;=</option>
				<option value="less_or_equal">&lt;=</option>
				<option value="equal">=</option>
			</select>
			<input type="TEXT" name="score_u" value="'.$score_u.'" /></td></tr>
		<tr><th class="std">TIME</td><td class="std">From <input type="TEXT" name="time_start" value="'.$time_start.'" /> to <input type="TEXT" name="time_end" value="'.$time_end.'" /> (dd/mm/yyyy)</td></tr>
		<tr><th class="std">SRC IP</td><td class="std"><input type="TEXT" name="src_ip" value="'.$src_ip.'" /></td></tr>
		<tr><th class="std">DST IP</td><td class="std"><input type="TEXT" name="dst_ip" value="'.$dst_ip.'" /></td></tr>
		<tr><th class="std">SRC PORT</td><td class="std"><input type="TEXT" name="src_port" value="'.$src_port.'" /></td></tr>
		<tr><th class="std">HOST</td><td class="std"><input type="TEXT" name="host" value="'.$host.'" /></td></tr>
		<tr><th class="std">URI</td><td class="std"><input type="TEXT" name="uri" value="'.$uri.'" /></td></tr>
		<tr><th class="std">FILENAME</td><td class="std"><input type="TEXT" name="fname" value="'.$filename.'" /></td></tr>
		<tr><th class="std">REFERER</td><td class="std"><input type="TEXT" name="referer" value="'.$referer.'" /></td></tr>
		<tr><th class="std">USER AGENT</td><td class="std"><input type="TEXT" name="user_agent" value="'.$user_agent.'" /></td></tr>
		<tr><th class="std">PROTOCOL</td><td class="std"><input type="TEXT" name="proto" value="'.$proto.'" /></td></tr>
		<tr><th class="std">SOURCE</td><td class="std"><input type="TEXT" name="source" value="'.$source.'" /></td></tr>
		<tr><th colspan="2"><input type="submit" name="SEARCH" value="SEARCH" /></th></tr>
	</table>
	</form>'.$results;
}
function display_meta_sign()
{
	echo '<h1>RULES LIST</h1>';
	if(isset($_GET['remove_trigger']))
	{
		if(!check_csrf(TRUE))
			error('[display_meta_sign] REMOVE TRIGGER CSRF ATTEMPT','SECURITY');

		remove_trigger($_GET['remove_trigger']);
	}
	if(isset($_POST['CREATE']) && isset($_POST['field']) && isset($_POST['description']) && isset($_POST['label']) && isset($_POST['criticity']) && isset($_POST['match']))
	{
		$table = "";
		$field = $_POST['field'];
		$description = $_POST['description'];
		$label = $_POST['label'];
		$criticity = $_POST['criticity'];
		$match = $_POST['match'];
		create_trigger($field,$description,$label,$criticity,$match);
	}
	$triggerz = get_triggerz();
	echo '<table>';
        while($res = $triggerz->fetchArray())
        {
		$disp = '<a href="'.$_SERVER['PHP_SELF'].'?meta_sign&view_trigger='.secure_display($res['name']).'">VIEW SQL TRIGGER</a>';
		if(isset($_GET['view_trigger']) && $_GET['view_trigger'] == $res['name'])
			$disp = secure_display($res['sql']);
		echo '<tr><th class="std">'.secure_display($res['name']).'</th><td>'.$disp.'</td><td><a href="'.$_SERVER['PHP_SELF'].'?meta_sign&crt='.gen_csrf(TRUE).'&remove_trigger='.secure_display($res['name']).'" onclick="return confirm(\'Are you sure?\');">REMOVE</a></td></tr>';
	}
	echo '</table>';

	echo '<h1>CREATE RULE</h1>
	<form action="'.$_SERVER['PHP_SELF'].'?meta_sign" method="POST">
		'.gen_csrf().'
	<table>
		<tr><th class="std">LABEL</th><td class="std"><input type="text" name="label" value=""></td></tr>
		<tr><th class="std">DESCRIPTION</th><td class="std"><input type="text" name="description" value=""></td></tr>
		<tr><th class="std">CRITICITY</th><td class="std"><select name="criticity"><option value="1">High</option><option value="2">Medium</option><option value="3">Low</option></select></td></tr>
		<tr><th class="std">
			<select name="field">
				<option value="md5">MD5</option>
				<option value="sign">SIGNATURE</option>
				<option value="src_ip">SRC IP</option>
				<option value="dst_ip">DST_IP</option>
				<option value="host">HOSTNAME</option>
				<option value="uri">URI</option>
				<option value="filename">FILENAME</option>
				<option value="user_agent">USER AGENT</option>
				<option value="referer">REFERER</option>
			</select>
		matches</th><td class="std"><input type="text" name="match" /> (input data is in LIKE SQL statements, use "%" as wildcards)</td></tr>
		
		<tr><th colspan="2"><input type="submit" name="CREATE" value="CREATE"/></th></tr>
	</table>
	</form>';
}
function display_sql_query()
{
	$default = "";
	if(isset($_POST['query']))
		$default = secure_display($_POST["query"]);

	echo '<h1>SQL QUERY</h1>
	NB: read-only access.<br />
	<form method="POST" action="'.$_SERVER['PHP_SELF'].'?sql_query">
		<textarea name="query" cols="120" rows="5">'.$default.'</textarea>'.gen_csrf().'<br />
		<input type="submit" name="RUN" value="RUN" />
	</form>';
	if(isset($_POST["query"]))
	{
		$ret = query_db($_POST["query"]);
		if($ret)
		{
			echo '<h1>QUERY RESULTS</h1>
			<table>';
			$header_displayed = FALSE;
			while($result = $ret->fetchArray(SQLITE3_ASSOC))
			{
				if(!$header_displayed)
				{
					echo '<tr>';
					foreach($result as $field=>$value)
						echo '<th class="std">'.secure_display($field).'</th>';
					echo '</tr>';
					$header_displayed = TRUE;
				}
				echo '<tr>';
				foreach($result as $field=>$value)
					echo '<td>'.secure_display($value).'</td>';
				echo '</tr>';
			}
			echo '</table>';
		}	
		
		
	}
}
function get_score_class($score,$kernelmode=0)
{
	global $usermode_score_high,$kernelmode_score_high,$usermode_score_medium,$kernelmode_score_medium;
	if(!is_int($score) || !is_int($score))
		return "";
	if($kernelmode==1)
	{
		if($score > $kernelmode_score_high)
			return "alert";
		elseif($score > $kernelmode_score_medium)
			return "warning";
	}
	else
	{
		if($score > $usermode_score_high)
			return "alert";
		elseif($score > $usermode_score_medium)
			return "warning";
	}
	return "okay";
}
function display_task_analyses($task_id)
{
	global $states,$usermode_score_medium,$usermode_score_high,$kernelmode_score_medium,$kernelmode_score_high;
	$req = get_task_analyses($task_id);
	if(!$req)
		return;
	echo '
	<div class="container100"><table class="std">
		<tr><th class="std">#</th><th class="std">State</th><th class="std">Type</th><th class="std">Score</th><th class="std">View</th></tr>';
	
	while($res = $req->fetchArray())
	{	
		$score = intval($res["total_score"]);
		$state = intval($res["state"]);
		$kernl = intval($res["kernel_analysis"]);
		echo '
		<tr onclick="document.location.href=\''.$_SERVER['PHP_SELF'].'?display_analysis='.secure_display($res["analysis_id"]).'\'"><td>'.secure_display($res["analysis_id"]).'</td><td>'.$states[$state].'</td>';
		if($kernl == 1)
			echo '<td>kernelmode</td><td class="';
		else
			echo '<td>usermode</td><td class="';
		echo get_score_class($score,$kernel).'">'.$score.'</td><td><a href="'.$_SERVER["PHP_SELF"].'?display_analysis='.secure_display($res["analysis_id"]).'">view analysis</a></td></tr>';
	}
	echo '
	</table></div>';
}
function display_task_analyses_short($task_id)
{
	global $states,$usermode_score_medium,$usermode_score_high,$kernelmode_score_medium,$kernelmode_score_high;
	$req = get_task_analyses($task_id);
	if(!$req)
		return;
	echo '
	<table class="inside_table">';
	while($res = $req->fetchArray())
	{
		$score = intval($res["total_score"]);
		$state = intval($res["state"]);
		$kernl = intval($res["kernel_analysis"]);
		echo '
		<tr><td>';
		if($kernl == 1)
			echo 'Kernelmode (';
		else
			echo 'Usermode (';
		echo $states[$state].')</td><td><span class="'.get_score_class($score,$kernl).'">'.$score.'</span></td></tr>';
	}
	echo '
	</table>';
}
function display_tasks()
{
	global $tasks_header,$tasks_footer;
	echo $tasks_header;
	
	$start = 0;
	$count = 10;
	$start_s = 0;
	$count_s = 10;
	if(isset($_GET["st"]) && isset($_GET["nb"]))
	{
		$start = $_GET["st"];
		$count = $_GET["nb"];
		$start_s = intval($_GET["st"]);
		$count_s = intval($_GET["nb"]);
	}
	$task_count = get_tasks_count();
	$nb_pages = $task_count / $count_s;
	$req = get_tasks($start,$count); // security checks done in db.php :]
	echo '
	    <div class="container100">
		<table class="std">
	        <tr><th class="std">#</th><th class="std">MD5</th><th class="std">ANALYSES :: SCORE</th><th class="std">SOURCES</th><th class="std">VIEW TASK</th></tr>';

	while ($res = $req->fetchArray()) 
	{
		$alerts_msg = "";
		$alerts = get_task_alerts($res["task_id"]);
		while($alert = $alerts->fetchArray())
		{
			$criticity = 'green';
			if($alert['criticity'] == 2)
				$criticity = 'orange';
	                elseif($alert['criticity'] == 1)
	                        $criticity = 'red';
			
			$alerts_msg.='<br /><span style="color:'.$criticity.'">'.secure_display($alert['label']).': '.secure_display($alert['description']).'</span>';
		}

		$metadata_matches = get_task_metadata($res["task_id"]);
		$counts = Array();
		$signs = Array();
		while($meta = $metadata_matches->fetchArray())
		{
			$source_info = get_source_info($meta["source_type"],$meta["source_id"],TRUE);
			if(in_array($source_info,$signs))
				$counts[array_search($source_info,$signs)]++;
			else
			{
				$counts[] = 1;
				$signs[] = $source_info;
			}
		}
		$source_data = '';
		for($i = 0; $i<count($counts); $i++)
		{
			if($signs[$i]!='MANUAL' && $counts[$i]!=1)
				$counts[$i]--;
			$source_data .= $signs[$i].' ('.$counts[$i].')<br />';
		}
		echo '
	        <tr onclick="document.location.href=\''.$_SERVER['PHP_SELF'].'?display_task='.$res["task_id"].'\'"><td>'.$res['task_id'].'</td><td>'.$res['md5'].$alerts_msg.'</td><td>';
		display_task_analyses_short($res["task_id"]);
		echo '</td><td>'.$source_data.'</td><td><a href="'.$_SERVER['PHP_SELF'].'?display_task='.$res["task_id"].'" style="color:blue;">display info</a></td></tr>';
		
	
	}
	echo '
                </table>
                <a href="'.$_SERVER['PHP_SELF'].'?display_tasks&st='.($start_s - $count_s).'&nb='.$count_s.'">&lt;--</a>&nbsp;
                <a href="'.$_SERVER['PHP_SELF'].'?display_tasks&st='.($start_s + $count_s).'&nb='.$count_s.'">&gt;--</a>
                <br />
                <form action="'.$_SERVER['PHP_SELF'].'" method="GET">
                        <input type="hidden" name="display_tasks" />
                        PAGE <select name="st" />';
        for($i = 0; $i < $nb_pages; $i++)
        {
                $sel = '';
                if($i*$count_s == $start_s)
                        $sel = " selected ";
                echo '<option value="'.$i*$count_s.'"'.$sel.'>'.($i + 1).'</option>';
        }

        echo '</select><input type="submit" value="OK" />
                        Display <select name="nb">';
        if($count_s != 10)
                echo '
                                <option value="'.$count_s.'">'.$count_s.'</option>';
        echo '
                                <option value="10">10</option>
                                <option value="20">20</option>
                                <option value="50">50</option>
                                <option value="100">100</option>
                        </select> results.
                </form>
         </div>';
	echo $tasks_footer;
}
?>
