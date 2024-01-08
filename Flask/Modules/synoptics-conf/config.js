/* 	Synoptics.
	Copyright (C) 2019 DISIT Lab http://www.disit.org - University of Florence

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU Affero General Public License for more details.
	You should have received a copy of the GNU Affero General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>. */

config = {
	"httpPort": 3002,
	"httpsPort": 3001,
	"verbose": true,
	"ownershipApi": "$#base-url#$/ownership-api/v1/list/?type={0}&accessToken={1}&elementId={2}",
	"personalDataDelegatedApi": "$#base-url#$/datamanager/api/v1/username/{0}/delegated?accessToken={1}&sourceRequest={2}&sourceId={3}&elementType={4}",
	"personalDataPrivateApi": "$#base-url#$/datamanager/api/v1/kpidata?accessToken={0}&sourceRequest={1}&sourceId={2}&highLevelType=MyKPI",
	"synOwnElmtType": "SynopticID",
	"keycloakAuth": "$#base-url#$/auth/",
	"srvSrcReq": "synopticserver",
	"dbHost": "$#dashboard-db-host#$",
	"dbUser": "$#dashboard-db-user#$",
	"dbPass": "$#dashboard-db-pwd#$",
	"dbName": "Dashboard",
	"synSvg": "$#base-url#$/dashboardSmartCity/img/synoptics/{0}.svg",
	"getOneKpiValue": "$#base-url#$/datamanager/api/v1/kpidata/{0}/values?last=1&accessToken={1}&sourceRequest={2}&sourceId={3}",
	"getOnePublicKpiValue": "$#base-url#$/datamanager/api/v1/public/kpidata/{0}/values?sourceRequest={1}&sourceId={2}",
	"getOneSensorValue": "$#base-url#$/ServiceMap/api/v1/?serviceUri={0}&valueName={1}",
	"getOnePublicSensorValue": "$#base-url#$/ServiceMap/api/v1/?serviceUri={0}&valueName={1}",
	"setValue": "$#base-url#$/datamanager/api/v1/kpidata/{0}/values?accessToken={1}&sourceRequest={2}&sourceId={3}",
	"getPublicValue": "$#base-url#$/datamanager/api/v1/public/kpidata?sourceRequest={0}&sourceId={1}",
	"getDashboardData": "$#base-url#$/dashboardSmartCity/management/getDashboardData.php?dashboardId={0}",
	"kafka": {
		"enable": {
			"nonMapped": false,
			"myKPIs": true,
			"sensors": true,
			"shared": false
		},
		"endpoint": "kafka:9092"
	},
	"publicWriting": {
		"usr": "usermanager",
		"pwd": "",
		"cid": "js-synoptic-client"
	},
	"bkpCleanItvl": 600000
};
