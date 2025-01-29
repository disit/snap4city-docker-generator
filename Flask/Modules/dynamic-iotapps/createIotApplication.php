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

$name = filter_input(INPUT_GET, 'name');
if($name===NULL) {
  exit;
}

$type = filter_input(INPUT_GET, 'type', FILTER_SANITIZE_STRING);
if($type===NULL) {
  $type = 'basic';
}

if (isset($_SESSION['refreshToken'])) {
  $oidc = new OpenIDConnectClient($ssoEndpoint, $ssoClientId, $ssoClientSecret);
  $oidc->providerConfigParam(array('token_endpoint' => $ssoTokenEndpoint));

  $tkn = $oidc->refreshToken($_SESSION['refreshToken']);

  $accessToken = $tkn->access_token;
  $_SESSION['refreshToken'] = $tkn->refresh_token;
  //echo $_SESSION['refreshToken'];

  if ($type == 'portia') {
    $json = http_get($iotAppApiBaseUrl . "/v1/?op=new_portia&name=" . urlencode($name) . "&accessToken=" . $accessToken);
  } else {
    $json = http_get($iotAppApiBaseUrl . "/v1/?op=new_nodered&name=" . urlencode($name) . "&type=" . urlencode($type) . "&accessToken=" . $accessToken);
  }
  if ($json['httpcode'] == 200 && !isset($json['result']["error"])) {
    $response['detail'] = 'Ok';
    $response['result'] = $json['result'];
  } else {
    $response['detail'] = 'Ko';
    if (isset($json['result']["error"]["error"])) {
      $response['error'] = $json['result']["error"]["error"];
    } else {
      $response['error'] = $json;
    }
  }
} else {
  $response['detail'] = 'Ko';
  $response['error'] = 'no refresh token';
}

echo json_encode($response);

function http_get($url) {
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET');
  curl_setopt($ch, CURLOPT_FAILONERROR, false);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  $response = curl_exec($ch);
  $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
  curl_close($ch);
  return array("httpcode" => $httpCode, "result" => $response, "url"=>$url);
}