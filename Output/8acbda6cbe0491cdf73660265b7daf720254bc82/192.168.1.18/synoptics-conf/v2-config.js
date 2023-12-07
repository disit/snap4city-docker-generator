config = {
	"verbose": true,
	"synOwnElmtType": "SynopticID",
	"keycloakAuth": "http://zjyzfjjy/auth/",
	"srvSrcReq": "synopticserver",
	"synSvg": "http://zjyzfjjy/dashboardSmartCity/img/synoptics/{0}.svg",
	"getOneKpiValue": "http://zjyzfjjy/datamanager/api/v1/kpidata/{0}/values?last=1&accessToken={1}&sourceRequest={2}&sourceId={3}",
	"getOnePublicKpiValue": "http://zjyzfjjy/datamanager/api/v1/public/kpidata/{0}/values?sourceRequest={1}&sourceId={2}",
	"getOneSensorValue": "http://zjyzfjjy/ServiceMap/api/v1/?serviceUri={0}&valueName={1}&accessToken={2}",
	"getOnePublicSensorValue": "http://zjyzfjjy/ServiceMap/api/v1/?serviceUri={0}&valueName={1}",
	"setValue": "http://zjyzfjjy/datamanager/api/v1/kpidata/{0}/values?accessToken={1}&sourceRequest={2}&sourceId={3}",
	"getDashboardData": "http://zjyzfjjy/dashboardSmartCity/management/getDashboardData.php?dashboardId={0}"
};
