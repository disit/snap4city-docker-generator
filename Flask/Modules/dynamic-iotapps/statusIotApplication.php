<?php
/* Dashboard Builder.
  Copyright (C) 2018 DISIT Lab https://www.disit.org - University of Florence

  This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Affero General Public License for more details.
   You should have received a copy of the GNU Affero General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>. */

require '../sso/autoload.php';

use Jumbojett\OpenIDConnectClient;
include '../config.php';
error_reporting(E_ERROR | E_NOTICE);
date_default_timezone_set('Europe/Rome');

session_start();

$response = [];

if(!isset($_REQUEST['id'])) {
  echo '{ "details":"Ko", "error":"missing id"}';
  exit;
}

if (isset($_SESSION['refreshToken'])) {
  $oidc = new OpenIDConnectClient($ssoEndpoint, $ssoClientId, $ssoClientSecret);
  $oidc->providerConfigParam(array('token_endpoint' => $ssoTokenEndpoint));

  $tkn = $oidc->refreshToken($_SESSION['refreshToken']);

  $accessToken = $tkn->access_token;
  $_SESSION['refreshToken'] = $tkn->refresh_token;

  $curl = curl_init();
  curl_setopt_array($curl, array(
    CURLOPT_URL => 'http://client:2880/get_status_of_container',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_ENCODING => '',
    CURLOPT_MAXREDIRS => 10,
    CURLOPT_TIMEOUT => 0,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
    CURLOPT_CUSTOMREQUEST => 'GET',
    CURLOPT_POSTFIELDS => 'name='.$_REQUEST['id'],
    CURLOPT_HTTPHEADER => array(
        'Content-Type: application/x-www-form-urlencoded'
    ),
  ));

    $response = curl_exec($curl);

    $httpCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        curl_close($curl);
    // Check for cURL errors
    if (curl_errno($curl)) {
        echo "cURL error: " . curl_error($curl);
        exit;
    }
    // Handle the response based on the HTTP status code
  if ($httpCode == 200) {
    $r2 = substr($response,0,-1);
    $r3=json_decode($r2, true);
    $finalvalue=(strpos($r3["status"], 'Up') !== false) ? $r3["status"] : false;
    echo json_encode(array("result"=>array("healthiness"=>$finalvalue), "detail" => "Ok"));
  } else {
    echo json_encode(["status" => $response, "detail" => "Ko"]);
  }
} else {
  echo json_encode(["status" => "No access token", "detail" => "Ko"]);
}

function http_get($url) {
  $opts = array('http' =>
      array(
          'method' => 'GET',
      )
  );

  # Create the context
  $context = stream_context_create($opts);
  # Get the response (you can use this for GET)
  $result = file_get_contents($url, false, $context);
  $json_result = json_decode($result);
  if($json_result===null || $json_result===false)
    $json_result = json_encode($result);
  //var_dump($http_response_header);
  return array("httpcode" => explode(" ", $http_response_header[0])[1], "result" => $json_result, "url"=>$url);
}