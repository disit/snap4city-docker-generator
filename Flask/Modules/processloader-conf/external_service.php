<?php
/* Resource Manager - Process Loader
   Copyright (C) 2018 DISIT Lab http://www.disit.org - University of Florence

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

//EXTERNAL SERVICES//
$host= '$#datamanager-db-host#$';
$username= '$#datamanager-db-user#$';
$password= '$#datamanager-db-pwd#$';
$dbname= 'profiledb';
$snap4city_API='localhost';

//PHOTO SERVICE//
$host_photo= '$#servicemap-db-host#$';
$username_photo= '$#servicemap-db-user#$';
$password_photo= '$#servicemap-db-pwd#$';
$dbname_photo= 'ServiceMap';
$photo_api='$#base-url#$/ServiceMap/api/v1/photo/thumbs/';
$default_longitude = 11.252;
$default_latitude = 43.773;
$default_serviceUri = '$#base-url#$/ServiceMap/api/v1/?serviceUri=';
$photo_service_api = '$#base-url#$/ServiceMap/ajax/';

//KPI EDITOR//
$host_kpi= '$#dashboard-db-host#$';
$username_kpi= '$#dashboard-db-user#$';
$password_kpi= '$#dashboard-db-pwd#$';
$dbname_kpi= 'processloader_db';

//heatmap server
$host_heatmap ='$#dashboard-db-host#$';
$username_heatmap = '$#dashboard-db-user#$';
$password_heatmap = '$#dashboard-db-pwd#$';
$dbname_heatmap = 'heatmap';

//userlimits
$host_limits = '$#dashboard-db-host#$';
$username_limits = '$#dashboard-db-user#$';
$password_limits = '$#dashboard-db-pwd#$';
$dbname_limits = 'profiledb';

$org_limits_api = '$#base-url#$/dashboardSmartCity/api/organizations.php';
$types_limits = ["IOTID","DashboardID","ModelID","AppID","DAAppID","DeviceGroupID","HeatmapID","PortiaID","SynopticID","SynopticTmplID","BrokerID"];

$host_od = '$#postgre-host#$';
$username_od = '$#postgre-user#$';
$password_od = '$#postgre-password#$';
$dbname_od = 'postgres';
?>
