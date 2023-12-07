<?php
/*
[database]
servername= "dashboarddb"
username= "user"
password = "I8YfiHfBqq7BNFXM"
dbname = "datatable"

[application]
target_dir="POIManager/files/"
language_file="languages.csv"

[poi]
poi_template_column="name,abbreviation,descriptionShort,descriptionLong,phone,fax,url,email,refPerson,secondPhone,secondFax,secondEmail,secondCivicNumber,secondStreetAddress,notes,timetable,photo,other1,other2,other3,postalcode,province,city,streetAddress,civicNumber,latitude,longitude"
poi_datatypes="string,string,string,string,string,string,URL,email,string,string,string,email,string,string,string,string,URL,string,string,string,string,string,string,string,string,float,float"
cell_special_characters="?,|"

[api]
ownershipApiUrl = "http://zjyzfjjy/ownership-api/v1/register/?"
valueTypeValueUnitApiUrl="http://zjyzfjjy/iot-directory/api/device.php/?"
valueTypeValueUnitApiUrlTest="http://zjyzfjjy/processloader/api/"
processLoaderURI= "http://zjyzfjjy/processloader/api/"
ownershipLimitApiUrl="http://zjyzfjjy/ownership-api/v1/limits?type=PoiTableID&accessToken="
ownershipListApiUrl="http://zjyzfjjy/ownership-api/v1/list/?type=PoiTableID&accessToken="
ownershipDeleteApiUrl="http://zjyzfjjy/ownership-api/v1/delete/?type=PoiTableID&"
processLoaderNatureURI="http://zjyzfjjy/processloader/api/dictionary/?type=subnature"
processLoaderValueUnitURI="http://zjyzfjjy/processloader/api/dictionary/?type=value_unit"
processLoaderContextBrokerURI="http://zjyzfjjy/iot-directory/api/contextbroker.php/?action=get_all_contextbroker&nodered"
valueTypeValueUnitAction="get_param_values"
valueTypeValueUnitNodered="1"
elementType = "PoiTableID"
elementUrl = ""
elementName = "PoiTableID"
base_suri="http://www.disit.org/km4city/resource/poi/"
uploaderUserUrl="http://zjyzfjjy/auth/realms/master/protocol/openid-connect/userinfo"
delegationUrl="http://zjyzfjjy/datamanager/api/v1/username/"
locationUrl="http://zjyzfjjy/ServiceMap/api/v1/location/?"
