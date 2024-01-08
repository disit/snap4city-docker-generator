config = {
	"verbose": true,
	"synOwnElmtType": "SynopticID",
	"keycloakAuth": "$#base-url#$/auth/",
	"srvSrcReq": "synopticserver",
	"synSvg": "$#base-url#$/dashboardSmartCity/img/synoptics/{0}.svg",
	"getOneKpiValue": "$#base-url#$/datamanager/api/v1/kpidata/{0}/values?last=1&accessToken={1}&sourceRequest={2}&sourceId={3}",
	"getOnePublicKpiValue": "$#base-url#$/datamanager/api/v1/public/kpidata/{0}/values?sourceRequest={1}&sourceId={2}",
	"getOneSensorValue": "$#base-url#$/ServiceMap/api/v1/?serviceUri={0}&valueName={1}&accessToken={2}",
	"getOnePublicSensorValue": "$#base-url#$/ServiceMap/api/v1/?serviceUri={0}&valueName={1}",
	"setValue": "$#base-url#$/datamanager/api/v1/kpidata/{0}/values?accessToken={1}&sourceRequest={2}&sourceId={3}",
	"getDashboardData": "$#base-url#$/dashboardSmartCity/management/getDashboardData.php?dashboardId={0}"
};
