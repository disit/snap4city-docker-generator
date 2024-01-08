<?php
/*
[database]
servername= "$#dashboard-db-host#$"
username= "$#dashboard-db-user#$"
password = "$#dashboard-db-pwd#$"
dbname = "datatable"

[application]
target_dir="POIManager/files/"
language_file="languages.csv"

[poi]
poi_template_column="name,abbreviation,descriptionShort,descriptionLong,phone,fax,url,email,refPerson,secondPhone,secondFax,secondEmail,secondCivicNumber,secondStreetAddress,notes,timetable,photo,other1,other2,other3,postalcode,province,city,streetAddress,civicNumber,latitude,longitude"
poi_datatypes="string,string,string,string,string,string,URL,email,string,string,string,email,string,string,string,string,URL,string,string,string,string,string,string,string,string,float,float"
cell_special_characters="?,|"

[api]
ownershipApiUrl = "$#base-url#$/ownership-api/v1/register/?"
valueTypeValueUnitApiUrl="$#base-url#$/iot-directory/api/device.php/?"
valueTypeValueUnitApiUrlTest="$#base-url#$/processloader/api/"
processLoaderURI= "$#base-url#$/processloader/api/"
ownershipLimitApiUrl="$#base-url#$/ownership-api/v1/limits?type=PoiTableID&accessToken="
ownershipListApiUrl="$#base-url#$/ownership-api/v1/list/?type=PoiTableID&accessToken="
ownershipDeleteApiUrl="$#base-url#$/ownership-api/v1/delete/?type=PoiTableID&"
processLoaderNatureURI="$#base-url#$/processloader/api/dictionary/?type=subnature"
processLoaderValueUnitURI="$#base-url#$/processloader/api/dictionary/?type=value_unit"
processLoaderContextBrokerURI="$#base-url#$/iot-directory/api/contextbroker.php/?action=get_all_contextbroker&nodered"
valueTypeValueUnitAction="get_param_values"
valueTypeValueUnitNodered="1"
elementType = "PoiTableID"
elementUrl = ""
elementName = "PoiTableID"
base_suri="http://www.disit.org/km4city/resource/poi/"
uploaderUserUrl="$#base-url#$/auth/realms/master/protocol/openid-connect/userinfo"
delegationUrl="$#base-url#$/datamanager/api/v1/username/"
locationUrl="$#base-url#$/ServiceMap/api/v1/location/?"
