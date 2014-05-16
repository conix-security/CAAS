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

function error($message,$type,$custom_message="")
{
	$msg = "UNSPECIFIED ERROR OCCURED";
	if($custom_message != "")
		$msg = $custom_message;
	
	//append_message($msg,$type);	
	
	// TODO : DEGAGER LE PRINT ET FOUTRE CA DANS UN FIC. DE LOG
	echo htmlentities($message);	
	
	if($type == "SECURITY")
		exit(1);
	if($type == "CRITICAL")
	{
		display_header();
		display_footer();
		exit(1);
	}
	
}
function secure($str)
{
	return htmlentities(addslashes($str));
}
$csrf_called = False;
function gen_csrf($raw = FALSE)
{
	global $csrf_called;
	if(!isset($_SESSION["csrf"]) || $csrf_called == False)
	{
		$strong = True;
		$random = openssl_random_pseudo_bytes(32,$strong);
		$hash = hash('sha512','d1sIzAgr3ATtOk3n'.$random);
		$token = '___'.$hash.'___';
		$_SESSION["csrf"] = $token;
		$csrf_called = True;
	}
	else
		$token = $_SESSION["csrf"];
	if(!$raw)
		return '<input type="hidden" name="crt" value="'.$token.'" />';
	else
		return $token;
}
function check_csrf($get=FALSE)
{
	/*
	if(!isset($_SERVER["HTTP_REFERER"]) || !isset($_SESSION["csrf"]) || !isset($_POST["crt"]))
		return False;
	// check referer value	
	$server_name = strtolower($_SERVER["HTTP_HOST"]);
	$referer = strtolower(trim($_SERVER["HTTP_REFERER"]));
	$arr = explode("://",$referer);
	if($arr[0] != "http" && $arr[0] != "https")
		return False;
	if(count($arr)==1)
		return False;
	$hostname = explode("/",$arr[1])[0];
	if(strcmp($hostname,$server_name) != 0)
		return False;
	*/
	// check csrf token
	if(!$get)
		$token_provd = $_POST["crt"];
	else
		$token_provd = $_GET["crt"];

	$token_savd = $_SESSION["csrf"];
	if(strcmp($token_savd,$token_provd)==0)
		return True;

	return False;
}
?>
