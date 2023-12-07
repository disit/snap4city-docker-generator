const elements = document.querySelectorAll('.component');
const tooltips = document.querySelectorAll('.tooltip_cp');
const elements_2 = document.querySelectorAll('.component_2');
const tooltips_2 = document.querySelectorAll('.tooltip_cp_2');
const elements_3 = document.querySelectorAll('.component_3');
const tooltips_3 = document.querySelectorAll('.tooltip_cp_3');
const elements_4 = document.querySelectorAll('.component_4');
const tooltips_4 = document.querySelectorAll('.tooltip_cp_4');
const elements_5 = document.querySelectorAll('.component_5');
const tooltips_5 = document.querySelectorAll('.tooltip_cp_5');
const elements_6 = document.querySelectorAll('.component_6');
const tooltips_6 = document.querySelectorAll('.tooltip_cp_6');
const elements_7 = document.querySelectorAll('.component_7');
const tooltips_7 = document.querySelectorAll('.tooltip_cp_7');
const elements_8 = document.querySelectorAll('.component_8');
const tooltips_8 = document.querySelectorAll('.tooltip_cp_8');
var popperInstances = [], popperInstances_2 = [], popperInstances_3 = [];
var popperInstances_4 = [], popperInstances_5 = [], popperInstances_6 = [];
var popperInstances_7 = [], popperInstances_8 = [];
for (let i = 0; i<elements.length; i++) {
  if (i === 10)
    popperInstances[i]=Popper.createPopper(elements[i], tooltips[i], {placement: 'left',});
  else
    popperInstances[i]=Popper.createPopper(elements[i], tooltips[i]);
}
for (let i = 0; i<elements_2.length; i++) {
  popperInstances_2[i]=Popper.createPopper(elements_2[i], tooltips_2[i]);
}
for (let i = 0; i<elements_3.length; i++) {
  popperInstances_3[i]=Popper.createPopper(elements_3[i], tooltips_3[i]);
}
for (let i = 0; i<elements_4.length; i++) {
  popperInstances_4[i]=Popper.createPopper(elements_4[i], tooltips_4[i]);
}
for (let i = 0; i<elements_5.length; i++) {
  popperInstances_5[i]=Popper.createPopper(elements_5[i], tooltips_5[i]);
}
for (let i = 0; i<elements_6.length; i++) {
  popperInstances_6[i]=Popper.createPopper(elements_6[i], tooltips_6[i]);
}
for (let i = 0; i<elements_7.length; i++) {
  popperInstances_7[i]=Popper.createPopper(elements_7[i], tooltips_7[i]);
}
for (let i = 0; i<elements_8.length; i++) {
  popperInstances_8[i]=Popper.createPopper(elements_8[i], tooltips_8[i]);
}


function show() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips[i].setAttribute('data-show', '');
  // We need to tell Popper to update the tooltip position
  // after we show the tooltip, otherwise it will be incorrect
  popperInstances[i].update();
}

function hide() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips[i].removeAttribute('data-show');
}

function show_2() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_2[i].setAttribute('data-show', '');
  popperInstances_2[i].update();
}

function hide_2() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_2[i].removeAttribute('data-show');
}

function show_3() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_3[i].setAttribute('data-show', '');
  popperInstances_3[i].update();
}

function hide_3() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_3[i].removeAttribute('data-show');
}

function show_4() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_4[i].setAttribute('data-show', '');
  popperInstances_4[i].update();
}

function hide_4() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_4[i].removeAttribute('data-show');
}
function show_5() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_5[i].setAttribute('data-show', '');
  popperInstances_5[i].update();
}

function hide_5() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_5[i].removeAttribute('data-show');
}
function show_6() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_6[i].setAttribute('data-show', '');
  popperInstances_6[i].update();
}

function hide_6() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_6[i].removeAttribute('data-show');
}
function show_7() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_7[i].setAttribute('data-show', '');
  popperInstances_7[i].update();
}
function hide_7() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_7[i].removeAttribute('data-show');
}
function show_8() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_8[i].setAttribute('data-show', '');
  popperInstances_8[i].update();
}
function hide_8() {
  var i = Array.from(this.parentNode.children).indexOf(this);
  tooltips_8[i].removeAttribute('data-show');
}

const showEvents = ['mouseenter', 'focus'];
const hideEvents = ['mouseleave', 'blur'];

showEvents.forEach((event) => {
  for (let i = 0; i<elements.length; i++) {
    elements[i].addEventListener(event, show);
    tooltips[i].addEventListener(event, show);
  }
  for (let i = 0; i<elements_2.length; i++) {
    elements_2[i].addEventListener(event, show_2);
    tooltips_2[i].addEventListener(event, show_2);
  }
  for (let i = 0; i<elements_3.length; i++) {
    elements_3[i].addEventListener(event, show_3);
    tooltips_3[i].addEventListener(event, show_3);
  }
  for (let i = 0; i<elements_4.length; i++) {
    elements_4[i].addEventListener(event, show_4);
    tooltips_4[i].addEventListener(event, show_4);
  }
  for (let i = 0; i<elements_5.length; i++) {
    elements_5[i].addEventListener(event, show_5);
    tooltips_5[i].addEventListener(event, show_5);
  }
  for (let i = 0; i<elements_6.length; i++) {
    elements_6[i].addEventListener(event, show_6);
    tooltips_6[i].addEventListener(event, show_6);
  }
  for (let i = 0; i<elements_7.length; i++) {
    elements_7[i].addEventListener(event, show_7);
    tooltips_7[i].addEventListener(event, show_7);
  }

  for (let i = 0; i<elements_8.length; i++) {
    elements_8[i].addEventListener(event, show_8);
    tooltips_8[i].addEventListener(event, show_8);
  }
});

hideEvents.forEach((event) => {
  for (let i = 0; i<elements_8.length; i++) {
    elements_8[i].addEventListener(event, hide_8);
    tooltips_8[i].addEventListener(event, hide_8);
  }
  for (let i = 0; i<elements_7.length; i++) {
    elements_7[i].addEventListener(event, hide_7);
    tooltips_7[i].addEventListener(event, hide_7);
  }
  for (let i = 0; i<elements_6.length; i++) {
    elements_6[i].addEventListener(event, hide_6);
    tooltips_6[i].addEventListener(event, hide_6);
  }
  for (let i = 0; i<elements_5.length; i++) {
    elements_5[i].addEventListener(event, hide_5);
    tooltips_5[i].addEventListener(event, hide_5);
  }
  for (let i = 0; i<elements_4.length; i++) {
    elements_4[i].addEventListener(event, hide_4);
    tooltips_4[i].addEventListener(event, hide_4);
  }
  for (let i = 0; i<elements_2.length; i++) {
    elements_2[i].addEventListener(event, hide_2);
    tooltips_2[i].addEventListener(event, hide_2);
  }
  for (let i = 0; i<elements_3.length; i++) {
    elements_3[i].addEventListener(event, hide_3);
    tooltips_3[i].addEventListener(event, hide_3);
  }
  for (let i = 0; i<elements.length; i++) {
    elements[i].addEventListener(event, hide);
    tooltips[i].addEventListener(event, hide);
  }
});

$(document).ready(function() {

var keycloak_myldap = new LeaderLine( //keycloak to myldap
  document.getElementById('item20'),
  document.getElementById('item17'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var myldap_ldap = new LeaderLine( //myldap to ldap
  document.getElementById('item21'),
  document.getElementById('item17'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var servicemap_virtuso = new LeaderLine( //servicemap to virtuoso
  document.getElementById('item3'),
  document.getElementById('item4'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var filter_broker = new LeaderLine( //filter to broker
  document.getElementById('item22'),
  document.getElementById('item6'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var filter_keyclock = new LeaderLine( //filter to keycloak
  document.getElementById('item22'),
  document.getElementById('item20'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var filter_frontend = new LeaderLine( //filter to frontend
  document.getElementById('item22'),
  document.getElementById('item14'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var filter_personaldata = new LeaderLine( //filter to personaldata
  document.getElementById('item22'),
  document.getElementById('item12'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var broker_mongo = new LeaderLine( //broker to mongo
  document.getElementById('item6'),
  document.getElementById('item10'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var broker_nifi = new LeaderLine( //broker to nifi
  document.getElementById('item6'),
  document.getElementById('item15'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var nifi_elastic = new LeaderLine( //nifi to elastic search
  document.getElementById('item15'),
  document.getElementById('item19'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var nifi_kafka = new LeaderLine( //nifi to kafka
  document.getElementById('item15'),
  document.getElementById('item5'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var nifi_servicemap = new LeaderLine( //nifi to servicemap
  document.getElementById('item15'),
  document.getElementById('item3'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var elastic_kibana = new LeaderLine( //kibana to elastic search
  document.getElementById('item16'),
  document.getElementById('item19'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var iot1_keycloak = new LeaderLine( //iotapp1 to keycloak
  document.getElementById('item1'),
  document.getElementById('item20'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var iot1_wsserver = new LeaderLine( //iotapp1 to wsserver
  document.getElementById('item1'),
  document.getElementById('item2'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var iot1_frontend = new LeaderLine( //iotapp1 to frontend
  document.getElementById('item1'),
  document.getElementById('item14'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var iot1_personaldata = new LeaderLine( //iotapp1 to personaldata
  document.getElementById('item1'),
  document.getElementById('item12'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var iot1_synoptics = new LeaderLine( //iotapp1 to synoptics
  document.getElementById('item1'),
  document.getElementById('item9'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var iot1_servicemap = new LeaderLine( //iotapp1 to servicemap
  document.getElementById('item1'),
  document.getElementById('item3'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var iot2_keycloak = new LeaderLine( //iotapp2 to keycloak
  document.getElementById('item24'),
  document.getElementById('item20'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var iot2_wsserver = new LeaderLine( //iotapp2 to wsserver
  document.getElementById('item24'),
  document.getElementById('item2'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var iot2_frontend = new LeaderLine( //iotapp2 to frontend
  document.getElementById('item24'),
  document.getElementById('item14'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var iot2_personaldata = new LeaderLine( //iotapp2 to personaldata
  document.getElementById('item24'),
  document.getElementById('item12'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var iot2_synoptics = new LeaderLine( //iotapp2 to synoptics
  document.getElementById('item24'),
  document.getElementById('item9'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var iot2_servicemap = new LeaderLine( //iotapp2 to servicemap
  document.getElementById('item24'),
  document.getElementById('item3'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var synoptics_database = new LeaderLine( //synoptics to database
  document.getElementById('item9'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var synoptics_kafka = new LeaderLine( //synoptics to kafka
  document.getElementById('item9'),
  document.getElementById('item5'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var synoptics_personaldata = new LeaderLine( //synoptics to personaldata
  document.getElementById('item9'),
  document.getElementById('item12'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var synoptics_keycloak = new LeaderLine( //synoptics to keycloak
  document.getElementById('item9'),
  document.getElementById('item20'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var kafka_zookerper = new LeaderLine( //kafka to zookeeper
  document.getElementById('item5'),
  document.getElementById('item7'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var wsserver_keycloak = new LeaderLine( //wsserver to keycloak
  document.getElementById('item2'),
  document.getElementById('item20'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var wsserver_database = new LeaderLine( //wsserver to database
  document.getElementById('item2'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var personaldata_database = new LeaderLine( //personaldata to database
  document.getElementById('item12'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var personaldata_keycloak = new LeaderLine( //personaldata to keycloak
  document.getElementById('item12'),
  document.getElementById('item20'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var personaldata_kafka = new LeaderLine( //personaldata to kafka
  document.getElementById('item12'),
  document.getElementById('item5'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var personaldata_ldapserver = new LeaderLine( //personaldata to ldapserver
  document.getElementById('item12'),
  document.getElementById('item17'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var servicemap_elastic = new LeaderLine( //servicemap to elasticsearch
  document.getElementById('item3'),
  document.getElementById('item19'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var servicemap_database = new LeaderLine( //servicemap to database
  document.getElementById('item3'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var servicemap_personaldata = new LeaderLine( //servicemap to personaldata
  document.getElementById('item3'),
  document.getElementById('item12'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var servicemap_ldapserver = new LeaderLine( //servicemap to ldapserver
  document.getElementById('item3'),
  document.getElementById('item17'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var front_keycloak = new LeaderLine( //frontend to keycloak
  document.getElementById('item14'),
  document.getElementById('item20'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var front_ldapserver = new LeaderLine( //frontend to ldapserver
  document.getElementById('item14'),
  document.getElementById('item17'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var front_database = new LeaderLine( //frontend to database
  document.getElementById('item14'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var front_personaldata = new LeaderLine( //frontend to personaldata
  document.getElementById('item14'),
  document.getElementById('item12'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var front_servicemap = new LeaderLine( //frontend to servicemap
  document.getElementById('item14'),
  document.getElementById('item3'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var front_broker = new LeaderLine( //frontend to broker
  document.getElementById('item14'),
  document.getElementById('item6'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var front_filter = new LeaderLine( //frontend to filter
  document.getElementById('item14'),
  document.getElementById('item22'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var cron_database = new LeaderLine( //dashboardcron to database
  document.getElementById('item18'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var cron_virtuoso = new LeaderLine( //dashboardcron to virtuoso
  document.getElementById('item18'),
  document.getElementById('item4'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var cron_personaldata = new LeaderLine( //dashboardcron to personaldata
  document.getElementById('item18'),
  document.getElementById('item12'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var cron_servicemap = new LeaderLine( //dashboardcron to servicemap
  document.getElementById('item18'),
  document.getElementById('item3'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var back_database = new LeaderLine( //backend to database
  document.getElementById('item8'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
//new

var cron_servicemap_2 = new LeaderLine( //dashboardcron to servicemap-2
  document.getElementById('item18'),
  document.getElementById('item28'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var front_servicemap_2 = new LeaderLine( //frontend to servicemap-2
  document.getElementById('item14'),
  document.getElementById('item28'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var servicemap_2_elastic = new LeaderLine( //servicemap-2 to elasticsearch
  document.getElementById('item28'),
  document.getElementById('item19'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var servicemap_2_database = new LeaderLine( //servicemap-2 to database
  document.getElementById('item28'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var servicemap_2_personaldata = new LeaderLine( //servicemap-2 to personaldata
  document.getElementById('item28'),
  document.getElementById('item12'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var servicemap_2_ldapserver = new LeaderLine( //servicemap-2 to ldapserver
  document.getElementById('item28'),
  document.getElementById('item17'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var servicemap_2_virtuso = new LeaderLine( //servicemap-2 to virtuoso-2
  document.getElementById('item28'),
  document.getElementById('item29'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var nifi_servicemap_2 = new LeaderLine( //nifi to servicemap-2
  document.getElementById('item15'),
  document.getElementById('item28'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var iot1_servicemap_2 = new LeaderLine( //iotapp1 to servicemap-2
  document.getElementById('item1'),
  document.getElementById('item28'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
var iot2_servicemap_2 = new LeaderLine( //iotapp2 to servicemap-2
  document.getElementById('item24'),
  document.getElementById('item28'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var cron_virtuoso = new LeaderLine( //dashboardcron to virtuoso-2
  document.getElementById('item18'),
  document.getElementById('item29'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );

  var od_insert_database = new LeaderLine( //od_insert to database
  document.getElementById('item100'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var od_insert_od_database = new LeaderLine( //od_insert to od-database
  document.getElementById('item100'),
  document.getElementById('item103'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var od_get_database = new LeaderLine( //od-get to database
  document.getElementById('item101'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var od_get_od_database = new LeaderLine( //od-get to od-database
  document.getElementById('item101'),
  document.getElementById('item103'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var od_build_database = new LeaderLine( //od-build to database
  document.getElementById('item102'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var od_build_od_database = new LeaderLine( //od-build to od-database
  document.getElementById('item102'),
  document.getElementById('item103'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var heatmap_api_database = new LeaderLine( //heatmap-api to database
  document.getElementById('item35'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var heatmap2geosrv_database = new LeaderLine( //heatmap2geosrv to database
  document.getElementById('item34'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var heatmap2geosrv_geoserver = new LeaderLine( //heatmap2geosrv to geoserver
  document.getElementById('item34'),
  document.getElementById('item30'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var geoserver_geoserver_db = new LeaderLine( //geoserver to geoserver-db
  document.getElementById('item30'),
  document.getElementById('item33'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var harvester_database = new LeaderLine( //harverster to database
  document.getElementById('item105'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
  var harvester_api_database = new LeaderLine( //harverster-api to database
  document.getElementById('item104'),
  document.getElementById('item11'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );

  var nifi_varnish = new LeaderLine( //nifi to varnish
  document.getElementById('item3'),
  document.getElementById('item15'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square', path:'arc'}
  );
//hoverable

var keycloak_myldap_h = new LeaderLine( //keycloak to myldap
  LeaderLine.mouseHoverAnchor(document.getElementById('item20')),
  document.getElementById('item17'), {color:'red', startPlug: 'square'}
  );
var myldap_ldap_h = new LeaderLine( //myldap to ldap
  LeaderLine.mouseHoverAnchor(document.getElementById('item21')),
  document.getElementById('item17'), { color:'red', startPlug: 'square'}
  );
var servicemap_virtuso_h = new LeaderLine( //servicemap to virtuoso
  LeaderLine.mouseHoverAnchor(document.getElementById('item3')),
  document.getElementById('item4'), { color:'red', startPlug: 'square'}
  );
var filter_broker_h = new LeaderLine( //filter to broker
  LeaderLine.mouseHoverAnchor(document.getElementById('item22')),
  document.getElementById('item6'), { color:'red', startPlug: 'square'}
  );
var filter_keyclock_h = new LeaderLine( //filter to keycloak
  LeaderLine.mouseHoverAnchor(document.getElementById('item22')),
  document.getElementById('item20'), { color:'red', startPlug: 'square'}
  );
var filter_personaldata_h = new LeaderLine( //filter to personaldata
  LeaderLine.mouseHoverAnchor(document.getElementById('item22')),
  document.getElementById('item12'), { color:'red', startPlug: 'square'}
  );
var filter_frontend_h = new LeaderLine( //filter to frontend
  LeaderLine.mouseHoverAnchor(document.getElementById('item22')),
  document.getElementById('item14'), { color:'red', startPlug: 'square'}
  );
var broker_mongo_h = new LeaderLine( //broker to mongo
  LeaderLine.mouseHoverAnchor(document.getElementById('item6')),
  document.getElementById('item10'), { color:'red', startPlug: 'square'}
  );
var broker_nifi_h = new LeaderLine( //broker to nifi
  LeaderLine.mouseHoverAnchor(document.getElementById('item6')),
  document.getElementById('item15'), { color:'red', startPlug: 'square'}
  );
var nifi_elastic_h = new LeaderLine( //nifi to elastic search
  LeaderLine.mouseHoverAnchor(document.getElementById('item15')),
  document.getElementById('item19'), { color:'red', startPlug: 'square'}
  );
var nifi_kafka_h = new LeaderLine( //nifi to kafka
  LeaderLine.mouseHoverAnchor(document.getElementById('item15')),
  document.getElementById('item5'), { color:'red', startPlug: 'square'}
  );
var nifi_servicemap_h = new LeaderLine( //nifi to servicemap
  LeaderLine.mouseHoverAnchor(document.getElementById('item15')),
  document.getElementById('item3'), { color:'red', startPlug: 'square'}
  );
var elastic_kibana_h = new LeaderLine( //kibana to elastic search
  LeaderLine.mouseHoverAnchor(document.getElementById('item16')),
  document.getElementById('item19'), { color:'red', startPlug: 'square'}
  );
var iot1_keycloak_h = new LeaderLine( //iotapp1 to keycloak
  LeaderLine.mouseHoverAnchor(document.getElementById('item1')),
  document.getElementById('item20'), {color:'red', startPlug: 'square', path:'arc'}
  );
var iot1_wsserver_h = new LeaderLine( //iotapp1 to wsserver
  LeaderLine.mouseHoverAnchor(document.getElementById('item1')),
  document.getElementById('item2'), {color:'red', startPlug: 'square', path:'arc'}
  );
var iot1_frontend_h = new LeaderLine( //iotapp1 to frontend
  LeaderLine.mouseHoverAnchor(document.getElementById('item1')),
  document.getElementById('item14'), {color:'red', startPlug: 'square', path:'arc'}
  );
var iot1_personaldata_h = new LeaderLine( //iotapp1 to personaldata
  LeaderLine.mouseHoverAnchor(document.getElementById('item1')),
  document.getElementById('item12'), {color:'red', startPlug: 'square', path:'arc'}
  );
var iot1_synoptics_h = new LeaderLine( //iotapp1 to synoptics
  LeaderLine.mouseHoverAnchor(document.getElementById('item1')),
  document.getElementById('item9'), {color:'red', startPlug: 'square', path:'arc'}
  );
var iot1_servicemap_h = new LeaderLine( //iotapp1 to servicemap
  LeaderLine.mouseHoverAnchor(document.getElementById('item1')),
  document.getElementById('item3'), {color:'red', startPlug: 'square', path:'arc'}
  );
var iot2_keycloak_h = new LeaderLine( //iotapp2 to keycloak
  LeaderLine.mouseHoverAnchor(document.getElementById('item24')),
  document.getElementById('item20'), {color:'red', startPlug: 'square'}
  );
var iot2_wsserver_h = new LeaderLine( //iotapp2 to wsserver
  LeaderLine.mouseHoverAnchor(document.getElementById('item24')),
  document.getElementById('item2'), {color:'red', startPlug: 'square'}
  );
var iot2_frontend_h = new LeaderLine( //iotapp2 to frontend
  LeaderLine.mouseHoverAnchor(document.getElementById('item24')),
  document.getElementById('item14'), {color:'red', startPlug: 'square'}
  );
var iot2_personaldata_h = new LeaderLine( //iotapp2 to personaldata
  LeaderLine.mouseHoverAnchor(document.getElementById('item24')),
  document.getElementById('item12'), {color:'red', startPlug: 'square'}
  );
var iot2_synoptics_h = new LeaderLine( //iotapp2 to synoptics
  LeaderLine.mouseHoverAnchor(document.getElementById('item24')),
  document.getElementById('item9'), {color:'red', startPlug: 'square'}
  );
var iot2_servicemap_h = new LeaderLine( //iotapp2 to servicemap
  LeaderLine.mouseHoverAnchor(document.getElementById('item24')),
  document.getElementById('item3'), {color:'red', startPlug: 'square'}
  );
var synoptics_database_h = new LeaderLine( //synoptics to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item9')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
var synoptics_kafka_h = new LeaderLine( //synoptics to kafka
  LeaderLine.mouseHoverAnchor(document.getElementById('item9')),
  document.getElementById('item5'), {color:'red', startPlug: 'square'}
  );
var synoptics_personaldata_h = new LeaderLine( //synoptics to personaldata
  LeaderLine.mouseHoverAnchor(document.getElementById('item9')),
  document.getElementById('item12'), {color:'red', startPlug: 'square', path:'arc'}
  );
var synoptics_keycloak_h = new LeaderLine( //synoptics to keycloak
  LeaderLine.mouseHoverAnchor(document.getElementById('item9')),
  document.getElementById('item20'), {color:'red', startPlug: 'square', path:'arc'}
  );
var kafka_zookerper_h = new LeaderLine( //kafka to zookeeper
  LeaderLine.mouseHoverAnchor(document.getElementById('item5')),
  document.getElementById('item7'), {color:'red', startPlug: 'square'}
  );
var wsserver_keycloak_h = new LeaderLine( //wsserver to keycloak
  LeaderLine.mouseHoverAnchor(document.getElementById('item2')),
  document.getElementById('item20'), {color:'red', startPlug: 'square', path:'arc'}
  );
var wsserver_database_h = new LeaderLine( //wsserver to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item2')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
var personaldata_database_h = new LeaderLine( //personaldata to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item12')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
var personaldata_keycloak_h = new LeaderLine( //personaldata to keycloak
  LeaderLine.mouseHoverAnchor(document.getElementById('item12')),
  document.getElementById('item20'), {color:'red', startPlug: 'square', path:'arc'}
  );
var personaldata_kafka_h = new LeaderLine( //personaldata to kafka
  LeaderLine.mouseHoverAnchor(document.getElementById('item12')),
  document.getElementById('item5'), {color:'red', startPlug: 'square'}
  );
var personaldata_ldapserver_h = new LeaderLine( //personaldata to ldapserver
  LeaderLine.mouseHoverAnchor(document.getElementById('item12')),
  document.getElementById('item17'), {color:'red', startPlug: 'square'}
  );
var servicemap_elastic_h = new LeaderLine( //servicemap to elasticsearch
  LeaderLine.mouseHoverAnchor(document.getElementById('item3')),
  document.getElementById('item19'), {color:'red', startPlug: 'square'}
  );
var servicemap_database_h = new LeaderLine( //servicemap to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item3')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
var servicemap_personaldata_h = new LeaderLine( //servicemap to personaldata
  LeaderLine.mouseHoverAnchor(document.getElementById('item3')),
  document.getElementById('item12'), {color:'red', startPlug: 'square', path:'arc'}
  );
var servicemap_ldapserver_h = new LeaderLine( //servicemap to ldapserver
  LeaderLine.mouseHoverAnchor(document.getElementById('item3')),
  document.getElementById('item17'), {color:'red', startPlug: 'square'}
  );
var front_keycloak_h = new LeaderLine( //frontend to keycloak
  LeaderLine.mouseHoverAnchor(document.getElementById('item14')),
  document.getElementById('item20'), {color:'red', startPlug: 'square', path:'arc'}
  );
var front_ldapserver_h = new LeaderLine( //frontend to ldapserver
  LeaderLine.mouseHoverAnchor(document.getElementById('item14')),
  document.getElementById('item17'), {color:'red', startPlug: 'square'}
  );
var front_database_h = new LeaderLine( //frontend to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item14')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
var front_personaldata_h = new LeaderLine( //frontend to personaldata
  LeaderLine.mouseHoverAnchor(document.getElementById('item14')),
  document.getElementById('item12'), {color:'red', startPlug: 'square', path:'arc'}
  );
var front_servicemap_h = new LeaderLine( //frontend to servicemap
  LeaderLine.mouseHoverAnchor(document.getElementById('item14')),
  document.getElementById('item3'), {color:'red', startPlug: 'square', path:'arc'}
  );
var front_broker_h = new LeaderLine( //frontend to broker
  LeaderLine.mouseHoverAnchor(document.getElementById('item14')),
  document.getElementById('item6'), {color:'red', startPlug: 'square'}
  );
var front_filter_h = new LeaderLine( //frontend to filter
  LeaderLine.mouseHoverAnchor(document.getElementById('item14')),
  document.getElementById('item22'), {color:'red', startPlug: 'square'}
  );
var cron_database_h = new LeaderLine( //dashboardcron to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item18')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
var cron_virtuoso_h = new LeaderLine( //dashboardcron to virtuoso
  LeaderLine.mouseHoverAnchor(document.getElementById('item18')),
  document.getElementById('item4'), {color:'red', startPlug: 'square'}
  );
var cron_personaldata_h = new LeaderLine( //dashboardcron to personaldata
  LeaderLine.mouseHoverAnchor(document.getElementById('item18')),
  document.getElementById('item12'), {color:'red', startPlug: 'square'}
  );
var cron_servicemap_h = new LeaderLine( //dashboardcron to servicemap
  LeaderLine.mouseHoverAnchor(document.getElementById('item18')),
  document.getElementById('item3'), {color:'red', startPlug: 'square'}
  );
var back_database_h = new LeaderLine( //backend to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item8')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
//from normal
var filter2_broker = new LeaderLine( //filter2 to broker2
  document.getElementById('item27'),
  document.getElementById('item25'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var filter2_keyclock = new LeaderLine( //filter2 to keycloak
  document.getElementById('item27'),
  document.getElementById('item20'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var filter2_frontend = new LeaderLine( //filter2 to frontend
  document.getElementById('item27'),
  document.getElementById('item14'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var filter2_personaldata = new LeaderLine( //filter2 to personaldata
  document.getElementById('item27'),
  document.getElementById('item25'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'});
var front_filter2 = new LeaderLine( //frontend to filter2
  document.getElementById('item14'),
  document.getElementById('item27'), {color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
);
var broker2_mongo2 = new LeaderLine( //broker2 to mongo2
  document.getElementById('item25'),
  document.getElementById('item26'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
var broker2_nifi = new LeaderLine( //broker to nifi
  document.getElementById('item25'),
  document.getElementById('item15'), { color:'rgb(255, 0, 0, 0.18)', startPlug: 'square'}
  );
// other lines
var filter2_broker_h = new LeaderLine( //filter2 to broker2
  LeaderLine.mouseHoverAnchor(document.getElementById('item27')),
  document.getElementById('item25'), { color:'red', startPlug: 'square'}
  );
var filter2_keyclock_h = new LeaderLine( //filter2 to keycloak
  LeaderLine.mouseHoverAnchor(document.getElementById('item27')),
  document.getElementById('item20'), { color:'red', startPlug: 'square'}
  );
var filter2_personaldata_h = new LeaderLine( //filter2 to personaldata
  LeaderLine.mouseHoverAnchor(document.getElementById('item27')),
  document.getElementById('item12'), { color:'red', startPlug: 'square'}
  );
var filter2_frontend_h = new LeaderLine( //filter2 to frontend
  LeaderLine.mouseHoverAnchor(document.getElementById('item27')),
  document.getElementById('item14'), { color:'red', startPlug: 'square'}
  );
var front_filter2_h = new LeaderLine( //frontend to filter
  LeaderLine.mouseHoverAnchor(document.getElementById('item14')),
  document.getElementById('item27'), {color:'red', startPlug: 'square'}
  );
var broker2_mongo2_h = new LeaderLine( //broker2 to mongo2
  LeaderLine.mouseHoverAnchor(document.getElementById('item25')),
  document.getElementById('item26'), { color:'red', startPlug: 'square'}
  );
var broker2_nifi_h = new LeaderLine( //broker2 to nifi
  LeaderLine.mouseHoverAnchor(document.getElementById('item25')),
  document.getElementById('item15'), { color:'red', startPlug: 'square'}
  );

var cron_servicemap_2_h = new LeaderLine( //dashboardcron to servicemap-2
  LeaderLine.mouseHoverAnchor(document.getElementById('item18')),
  document.getElementById('item28'), {color:'red', startPlug: 'square'}
  );
var front_servicemap_2_h = new LeaderLine( //frontend to servicemap-2
  LeaderLine.mouseHoverAnchor(document.getElementById('item14')),
  document.getElementById('item28'), {color:'red', startPlug: 'square', path:'arc'}
  );
var servicemap_2_elastic_h = new LeaderLine( //servicemap-2 to elasticsearch
  LeaderLine.mouseHoverAnchor(document.getElementById('item28')),
  document.getElementById('item19'), {color:'red', startPlug: 'square'}
  );
var servicemap_2_database_h = new LeaderLine( //servicemap-2 to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item28')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
var servicemap_2_personaldata_h = new LeaderLine( //servicemap-2 to personaldata
  LeaderLine.mouseHoverAnchor(document.getElementById('item28')),
  document.getElementById('item12'), {color:'red', startPlug: 'square', path:'arc'}
  );
var servicemap_2_ldapserver_h = new LeaderLine( //servicemap-2 to ldapserver
  LeaderLine.mouseHoverAnchor(document.getElementById('item28')),
  document.getElementById('item17'), {color:'red', startPlug: 'square'}
  );
var servicemap_2_virtuso_h = new LeaderLine( //servicemap-2 to virtuoso-2
  LeaderLine.mouseHoverAnchor(document.getElementById('item28')),
  document.getElementById('item29'), { color:'red', startPlug: 'square'}
  );
var nifi_servicemap_2_h = new LeaderLine( //nifi to servicemap-2
  LeaderLine.mouseHoverAnchor(document.getElementById('item15')),
  document.getElementById('item28'), { color:'red', startPlug: 'square'}
  );
var iot1_servicemap_2_h = new LeaderLine( //iotapp1 to servicemap-2
  LeaderLine.mouseHoverAnchor(document.getElementById('item1')),
  document.getElementById('item28'), {color:'red', startPlug: 'square', path:'arc'}
  );
var iot2_servicemap_2_h = new LeaderLine( //iotapp2 to servicemap-2
  LeaderLine.mouseHoverAnchor(document.getElementById('item24')),
  document.getElementById('item28'), {color:'red', startPlug: 'square'}
  );
var cron_virtuoso_h = new LeaderLine( //dashboardcron to virtuoso-2
  LeaderLine.mouseHoverAnchor(document.getElementById('item18')),
  document.getElementById('item29'), {color:'red', startPlug: 'square'}
  );

  var od_insert_database_h = new LeaderLine( //od_insert to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item100')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
  var od_insert_od_database_h = new LeaderLine( //od_insert to od-database
  LeaderLine.mouseHoverAnchor(document.getElementById('item100')),
  document.getElementById('item103'), {color:'red', startPlug: 'square'}
  );
  var od_get_database_h = new LeaderLine( //od-get to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item101')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
  var od_get_od_database_h = new LeaderLine( //od-get to od-database
  LeaderLine.mouseHoverAnchor(document.getElementById('item101')),
  document.getElementById('item103'), {color:'red', startPlug: 'square'}
  );
  var od_build_database_h = new LeaderLine( //od-build to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item102')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
  var od_build_od_database_h = new LeaderLine( //od-build to od-database
  LeaderLine.mouseHoverAnchor(document.getElementById('item102')),
  document.getElementById('item103'), {color:'red', startPlug: 'square'}
  );

  var heatmap_api_database_h = new LeaderLine( //heatmap-api to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item35')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
  var heatmap2geosrv_database_h = new LeaderLine( //heatmap2geosrv to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item34')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
  var heatmap2geosrv_geoserver_h = new LeaderLine( //heatmap2geosrv to geoserver
  LeaderLine.mouseHoverAnchor(document.getElementById('item34')),
  document.getElementById('item30'), {color:'red', startPlug: 'square'}
  );
  var geoserver_geoserver_db_h = new LeaderLine( //geoserver to geoserver-db
  LeaderLine.mouseHoverAnchor(document.getElementById('item30')),
  document.getElementById('item33'), {color:'red', startPlug: 'square'}
  );
  var harvester_database_h = new LeaderLine( //harvester to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item105')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );
var harvester_api_database_h = new LeaderLine( //harvester_api to database
  LeaderLine.mouseHoverAnchor(document.getElementById('item104')),
  document.getElementById('item11'), {color:'red', startPlug: 'square'}
  );

var nifi_varnish_h = new LeaderLine( //nifi to varnish
  LeaderLine.mouseHoverAnchor(document.getElementById('item15')),
  document.getElementById('item106'), {color:'red', startPlug: 'square', path:'arc'}
  );
});
