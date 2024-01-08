<?php
/*
[database]
servername= "$#dashboard-db-host#$"
username= "$#dashboard-db-user#$"
password = "$#dashboard-db-pwd#$"
dbname = "datatable"

[application]
target_dir="DataTableManager/files/"
time_zone="Europe/Rome"

float_datatype="hours,min,s,°C,°K,°F,mV,hPa,lux,bpm,kg/m³dB,m,km/h,ppb,ppm,A,mS/cm,KW/h,µg/m³W,mm,cbar,V,car/h,l/h,µm,deg,m/s,car/m,ugS/m3,ug/m3,SMC,MW/H,MW,KW,GW,W/m2,millivolt,mA,milliwatt,wh,Mean#,dBA,KA,t/h,t/d,mg/m3,M#,hits/cm2,umol/m2,#,Meuro,keuro,K#,euro,status,deg"
time_datatype="HH:MM"
string_datatype="status,latlon,ID,targa,text"
timestamp_datatype="timestamp"
integer_datatype="vote"
binary_datatype="bool"
url_datatype="SURI"

[phpMailer]
host="smtpserver"
port= "25"
email_from="info@me.org"
email_to="snap4city@me.org"

[api]
ownershipApiUrl = "$#base-url#$/ownership-api/v1/register/?"
valueTypeValueUnitApiUrl="$#base-url#$/iot-directory/api/device.php/?"
valueTypeValueUnitApiUrlTest="$#base-url#$/processloader/api/"
processLoaderURI= "$#base-url#$/processloader/api/"
ownershipLimitApiUrl="$#base-url#$/ownership-api/v1/limits?type=DataTableID&accessToken="
ownershipListApiUrl="$#base-url#$/ownership-api/v1/list/?type=DataTableID&accessToken="
ownershipDeleteApiUrl="$#base-url#$/ownership-api/v1/delete/?type=DataTableID&"
processLoaderNatureURI="$#base-url#$/processloader/api/dictionary/?type=subnature"
processLoaderValueUnitURI="$#base-url#$/processloader/api/dictionary/?type=value_unit"
processLoaderContextBrokerURI="$#base-url#$/iot-directory/api/contextbroker.php/?action=get_all_contextbroker&nodered"
valueTypeValueUnitAction="get_param_values"
valueTypeValueUnitNodered="1"
base_suri="http://www.disit.org/km4city/resource/poi/"
uploaderUserUrl="$#base-url#$/auth/realms/master/protocol/openid-connect/userinfo"
delegationUrl="$#base-url#$/datamanager/api/v1/username/"
locationUrl="$#base-url#$/ServiceMap/api/v1/location/?"
delegationOrgUrl="$#base-url#$/dashboardSmartCity/api/organizations.php?includeUsers=true&org="

elementType = "DataTableID"
elementUrl = ""
elementName = "DataTableID"
