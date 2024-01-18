'''Snap4city Docker & Kubernetes Generator
   Copyright (C) 2022 DISIT Lab http://www.disit.org - University of Florence

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

from flask import Flask, render_template, url_for, request, redirect, session, send_file, send_from_directory
import atexit
import os, json, errno, shutil
import datetime
from contextlib import closing
import re
import mysql.connector
import sys
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
sys.path.insert(1,'/functions')
from functions import snap4
if "allow_compress" not in os.environ:
    os.environ['allow_compress']="False"
if "allow_update" not in os.environ:
    os.environ['allow_update']="False"
if "add_utils" not in os.environ:
    os.environ['add_utils']="False"
if 'send-aws-k8s' not in os.environ:
    os.environ['send-aws-k8s'] ="False"

def print_date_time_sql():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the dump filename
    dump_filename = f"configurator_dump_{timestamp}.tsv"

    result=""
    # Construct the mysqldump command
    with closing(mysql.connector.connect(user= "access_user",
        password= "psw_something",
        host= "db",
        port= 3306,
        database= "configurations v-2",
        auth_plugin= 'caching_sha2_password')) as conn:
            q = "Select * from saved_configurations"
            cursor=conn.cursor()
            cursor.execute(q)
            result=cursor.fetchall()
    try:
        with open("./Output/"+dump_filename, "w") as f:
            for row in result:
                f.write("\t".join(row))
                f.write("\n")
        print("[LOG] Dumped",dump_filename)
    except subprocess.CalledProcessError as e:
        print(f"Error during database dump: {e}")


scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time_sql, trigger="interval", days=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def create_app():
    app = Flask(__name__)
    data = ""
    print("[LOG] Waiting",os.environ['time_wait_update_db'],"seconds for db startup...")
    os.system("sleep "+os.environ['time_wait_update_db'])
    print("[LOG] Attempting to update DB with latest data")
    try:
        with closing(mysql.connector.connect(host="db", user="root", passwd=os.environ['MYSQL_ROOT_PASSWORD'], port=3306, database="configurations v-2", auth_plugin='caching_sha2_password')) as conn:
            with open('./Mysql/latest.sql', 'r') as f:
                arr_f = f.read().split(';')
                for a in arr_f:
                    if any(substring in a for substring in ['DROP TABLE IF EXISTS `saved_configurations`','CREATE TABLE `saved_configurations`']):
                        pass
                    try:
                        cursor = conn.cursor()
                        cursor.execute(a, multi=True)
                        conn.commit()

                    except mysql.connector.Error as err:
                        print("[LOG] Database Setup Error at",datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),"reason:",err)
    except Exception as err:
        print("[LOG] Database Setup Fatal Error at",datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),"reason:",err)

    print("[LOG] Database Setup Ended at",datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    # This user is defined inside one of the sql for the db startup. It has proper permissions set.
    
    print_date_time_sql()
    db_conn_info = {
        "user": "access_user",
        "passwd": "psw_something",
        "host": "db",
        "port": 3306,
        "database": "configurations v-2",
        "auth_plugin": 'caching_sha2_password'
    }

    app.secret_key = b'\x8a\x17\x93kT\xc0\x0b6;\x93\xfdp\x8bLl\xe6u\xa9\xf5x'  # random bytes really
    

    @app.route('/', methods=['GET', 'POST'])
    def hello():
        return redirect(url_for('simple_choosing'))

    @app.route('/updating_information')
    def update_info():
        return render_template('updating_instructions.html')


    @app.route('/micro_components_x')
    def micro_x_2():
        return render_template('micro_x_2.html')

    @app.route('/normal_components_x_y')
    def normal_x_y():
        return render_template('normal_x_y.html')

    @app.route('/update_the_db_after_starting_it')
    def update_db(): #can't show this without permission
        if os.environ['allow_update']=="True":
            return render_template('db-updates.html')
        return

    @app.route('/updating_db', methods=['GET', 'POST'])
    def updating_db(): #can't do this without permission
        if os.environ['allow_update']=="True" or request.method == 'GET':
            result = ""
            try:
                with closing(mysql.connector.connect(host="db", user="root", passwd=request.form.to_dict()['password'], port=3306, database="configurations v-2", auth_plugin='caching_sha2_password')) as conn:
                    with open('/data/mysql/a.sql', 'r') as f:
                        arr_f = f.read().split(';')
                        for a in arr_f:
                            if any(substring in a for substring in ['DROP TABLE IF EXISTS `saved_configurations`','CREATE TABLE `saved_configurations`']):
                                pass
                            try:
                                cursor = conn.cursor()
                                cursor.execute(a, multi=True)
                                conn.commit()

                            except mysql.connector.Error as err:
                                result += err + '<br>'
            except:
                result = "Login failed"
            if result == "":
                result="No errors during update."
            print("[LOG] Database Updated",datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            return render_template('done.html', result=result)
        else:
            return


    @app.route('/done')
    def done():
        return render_template('done.html')

    @app.route('/small_components_x_y')
    def small_x_y():
        return render_template('small_x_y.html')

    @app.route('/dcs_components_x_y_z')
    def dcs_x_y_z():
        return render_template('dcs_x_y_z.html')

    @app.route('/make_more_opensearch', methods=['POST','GET'])
    def make_more_opensearch():
        if request.method == 'GET':  # if you didn't use a form you shouldn't be here
            return redirect(url_for('simple_choosing'))
        else:
            # getting ready for solving the placeholders
            print('[LOG] Extra OpenSearch:',datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            post = request.form.to_dict()
            references, fine_as_is = {},{}
            for key, value in post.items():
                if re.match(".*\$#[^\#]*#\$.*", value):
                    references[key]=value
                else:
                    fine_as_is[key]=value
            # solve the references, where possible
            while True:
                change = False
                remove_later = {}
                for key_r, value_r in references.items():
                    if re.match('.*\$#[^\#]*#\$.*', value_r):
                        for key_f, value_f in fine_as_is.items():
                            old = value_r
                            replaced = value_r.replace(key_f, value_f)
                            references[key_r] = replaced
                            if old != references[key_r]:
                                change = True
                                break
                    else:
                        remove_later[key_r]=value_r
                        change = True
                fine_as_is = dict(fine_as_is.items() | remove_later.items())  # add solved references to usable placeholders
                references = dict(references.items() ^ remove_later.items())  # remove solved references from currently unresolved references
                if not change: # either no more references exist or we hit a loop (eg $#id#$ -> $#psw#$ and $#psw#$ -> $#id#$)
                    break

            try: # make a folder to store the new files
                os.makedirs("./Output/opensearch-temp")
            except IsADirectoryError:  # Already exists
                shutil.rmtree("./Output/opensearch-temp")
                os.makedirs("./Output/opensearch-temp")
            snap4.copy('./Modules/merge-opensearch-instructions.txt', './Output/opensearch-temp/instructions.txt')
            open_ips_keys=[j for i,j in fine_as_is.items() if 'ip_field_opensearch-' in i]
            snap4.make_multiple_opensearch(int(fine_as_is["$#how-many-opensearch#$"]),fine_as_is['dashboard'],fine_as_is['LDAP'], 'token-not-used', open_ips_keys, alt_out='./Output/opensearch-temp')

            shutil.make_archive('compressed', 'zip', "./Output/opensearch-temp")
            try:
                shutil.rmtree("./Output/opensearch-temp")
            except FileNotFoundError:
                pass  # not a problem, we are deleting the file
            print('Sending Opensearch files')
            return send_file('./compressed.zip', download_name='opensearch-files.zip') #send the pack

    @app.route('/make_more_nifi', methods=['POST','GET'])
    def make_more_nifi():
        if request.method == 'GET':  # if you didn't use a form you shouldn't be here
            return redirect(url_for('simple_choosing'))
        else:
            # getting ready for solving the placeholders
            print('[LOG] Extra Nifi at',datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            post = request.form.to_dict()
            references, fine_as_is = {},{}
            ips = []
            detailed_ips = {}
            iotapps_ip = []
            for key, value in post.items():
                if re.match(".*\$#[^\#]*#\$.*", value):
                    references[key]=value
                else:
                    fine_as_is[key]=value
            # solve the references, where possible
            while True:
                change = False
                remove_later = {}
                for key_r, value_r in references.items():
                    if re.match('.*\$#[^\#]*#\$.*', value_r):
                        for key_f, value_f in fine_as_is.items():
                            old = value_r
                            replaced = value_r.replace(key_f, value_f)
                            references[key_r] = replaced
                            if old != references[key_r]:
                                change = True
                                break
                    else:
                        remove_later[key_r]=value_r
                        change = True
                fine_as_is = dict(fine_as_is.items() | remove_later.items())  # add solved references to usable placeholders
                references = dict(references.items() ^ remove_later.items())  # remove solved references from currently unresolved references
                if not change: # either no more references exist or we hit a loop (eg $#id#$ -> $#psw#$ and $#psw#$ -> $#id#$)
                    break
            nodes_ips = ''
            components_ips = """      - dashboard:"""+fine_as_is['dashboard']+"""
      - opensearch-n1:"""+fine_as_is['opensearch']+"""
      - kafka:"""+fine_as_is['kafka']
            # ports are hardcoded here and in flow, when active
            ports = [str(i) for i in range(1026, 1036)]
            i = 1
            for ip in ips:
                nodes_ips+='      - nifi-node-'+str(i)+':'+ip+'\n'
                i+=1
            j = 0
            files = ['./Output/nifi-temp/docker-compose-nifi-'+str(i)+'.yml' for i in range(int(fine_as_is['how-many-nifi']))]
            os.makedirs('./Output/nifi-temp')
            for i in range(len(files)):
                snap4.copy('./Modules/docker-compose-nifi-added.yml', files[i])

            snap4.copy('./Modules/merge-nifi-instructions.txt', './Output/nifi-temp/instructions.txt')

            for i in files:
                j = 0
                with open(i, 'r') as f:
                    s = f.read()
                    s=s.replace('$#node_name#$','nifi-node-'+str(j+1))
                    s=s.replace('$#extra_hosts#$',components_ips)
                    s=s.replace('$#id_zookeeper#$',fine_as_is['zookeeper'])

                j+=1
                with open(i, 'w') as f:
                    f.write(s)

            shutil.make_archive('compressed', 'zip', "./Output/nifi-temp")
            try:
                shutil.rmtree("./Output/nifi-temp")
            except FileNotFoundError:
                pass  # not a problem, we are deleting the file
            print('Sending nifi files')
            return send_file('./compressed.zip', download_name='nifi-files.zip') #send the pack


    @app.route('/more_nifi')
    def more_nifi():
        return render_template('more_nifi.html')

    @app.route('/more_opensearch')
    def more_opensearch():
        return render_template('more_opensearch.html')

    @app.route('/dcm_components_x_y_z_w')
    def dcm_x_y_z_w():
        return render_template('dcm_x_y_z_w.html')

    

    # the main page
    @app.route('/selecting_model')
    def simple_choosing():
        return render_template("simplified_choosing.html",helpmail=os.environ["help_mail"],kuber=os.environ["kuber"],version=os.environ["version"],multi_ip=os.environ['allow_compress'])

    # this is how the favicon is shown and set up
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                              'favicon.ico',mimetype='image/vnd.microsoft.icon')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html',helpmail=os.environ["help_mail"],version=os.environ["version"]), 404


    @app.errorhandler(500)
    def some_kinf_of_error(e):
        return render_template('500.html', e=e,helpmail=os.environ["help_mail"],version=os.environ["version"]), 500

    @app.route("/crash")
    def crash():
        return None  # can't return None, this is a test

    @app.route("/kubernetes_configuration")
    def kubernetes():
        return redirect(url_for('simple_choosing'))
        #return render_template("kubernetes.html",helpmail=os.environ["help_mail"])


    # this is where the user fills everything other than picking the model or the token
    @app.route("/fill_placeholders", methods=['POST','GET'])
    def fill_placeholders():
        if request.method == 'GET':  #if you didn't fill a form, you are redirected to the main page
            return redirect(url_for('simple_choosing'))
        else:
            initial_values = request.form
            select = None
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cur = conn.cursor()
                search_what = None
                try:
                    search_what=request.form['Model name']
                    method = 'no_token'
                except Exception:  #if a token was used, the model field doesn't exists and an error is thrown
                    method = 'with_token'
                    cur.execute('SELECT * from saved_configurations where token=%s and placeholder ="Model name"', (request.form['token_value'],))
                    try:
                        search_what = cur.fetchone()[2]  # was there actually a token?
                    except:
                        return redirect(url_for('simple_choosing'))  # no token was found, don't load anything
                finally:
                    # this will be used to generate the left side of the form
                    cur.execute('SELECT t1.Placeholder,t2.Type,t2.Desc,t2.Modello,t2.`Default`,t2.Desc_long, t2.Extra_parameters, t2.Hidden from placeholder_list as t1 left join additional_data as t2 on t1.Placeholder=t2.Placeholder WHERE t2.Modello=%s group by t1.placeholder order by t1.placeholder',(search_what,))
                    select=cur.fetchall()
            required, has_default, references = [],[],[]
            # telling apart references, empty placeholders and placeholders with default values
            for placeholder in select:
                if (placeholder[4] is None or placeholder[4] == '') and placeholder[7] != '1':  #TODO this is bandaged
                    required.append(placeholder)
                elif '$#' in placeholder[4] and '#$' in placeholder[4] and placeholder[7] != '1':  # can be better, even if works most of the times
                    references.append(placeholder)
                else:
                    has_default.append(placeholder)
            # the usage of tokens changes how the webpage will be loaded
            # in case of token, I'll have to put the values that were found after the page is done loading
            if method == 'no_token':
                # required = elements that are taken from the database
                # has_default = elements that are taken from the database but have a default value
                # references = elements that are taken from the database, have a default value that is a placeholder
                # initial_values = how many components, and which components
                # model = which model was selected, eg. Small
                # variable_values = not used here
                return render_template("solve_placeholder.html", required = required, has_default = has_default, references = references, initial_values = initial_values, model = search_what, helpmail=os.environ["help_mail"],version=os.environ["version"])
            elif method == 'with_token':
                with closing(mysql.connector.connect(**db_conn_info)) as conn:
                    # TODO small bug
                    cur = conn.cursor()
                    cur.execute('SELECT * from saved_configurations where token=%s',(request.form['token_value'],))
                    stored_values = cur.fetchall()
                    cur.execute("SELECT placeholder, saved_configurations.`values` from saved_configurations where Placeholder not like '$#%#$' and token =%s",(request.form['token_value'],))  # this might need to be reviewed
                    initial_values = dict((x, y) for x, y in cur.fetchall())
                    stored_values_dict = dict((y, z) for x, y, z in stored_values)
                    variable_values = snap4.retrieve_variable_components(stored_values_dict)

                    for key, value in initial_values.items():
                        if key != "Time" and key != "Model name" and key !='token_place':
                            variable_values[key]=value
                    # stored_values = what was saved the last time
                    return render_template("solve_placeholder_with_token.html", required = required, has_default = has_default, references = references, initial_values = variable_values, model = initial_values['Model name'], stored_values=stored_values, token=request.form['token_value'],helpmail=os.environ["help_mail"],version=os.environ["version"])


    #giving the configuration to the user
    @app.route("/deal_with_placeholders", methods=['POST','GET'])
    def dealing_with_placeholders():
        if request.method == 'GET':  # if you didn't use a form you shouldn't be here
            return redirect(url_for('simple_choosing'))
        else:
            # getting ready for solving the placeholders
            print('[LOG]:',datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            post = request.form.to_dict()
            modello = post.pop('Model name')
            token = post.pop('token_place')
            post["$#Time#$"]=(post.pop('Time'))
            references, fine_as_is = {},{}
            ips = []
            detailed_ips = {}
            iotapps_ip = []
            for key, value in post.items():
                # multiple placeholders, separated by |
                if re.match("(.*\$#[^\#]*#\$)(\|\$#[^\#]*#\$.*)+", key):
                    keys = key.split("|")
                    values = value.split("|")
                    for key1, value1 in zip (keys, values):
                        if re.match(".*\$#[^\#]*#\$.*", value1):
                            references[key1]=value1

                        elif key1.startswith('ip'):
                            fine_as_is['$#ip-'+str(len(ips))+'#$']=value1
                            ips.append(value1)
                            detailed_ips['$#'+key+'#$']=value1
                        else:
                            fine_as_is[key1]=value1
                if re.match(".*\$#[^\#]*#\$.*", value):
                    references[key]=value

                elif key.startswith('ip'):
                    fine_as_is['$#ip-'+str(len(ips))+'#$']=value
                    ips.append(value)
                    detailed_ips['$#'+key+'#$']=value
                else:
                    fine_as_is[key]=value
            # a list of a set of a list is a list without duplicates, lenght tells apart the former from the latter
            if len(ips) != len(set(ips)) and not os.environ['allow_compress']:
                print('IPs were not all different.')
                return None
            # solve the references, where possible
            while True:
                change = False
                remove_later = {}
                for key_r, value_r in references.items():
                    if re.match('.*\$#[^\#]*#\$.*', value_r):
                        for key_f, value_f in fine_as_is.items():
                            old = value_r
                            replaced = value_r.replace(key_f, value_f)
                            references[key_r] = replaced
                            if old != references[key_r]:
                                change = True
                                break
                    else:
                        remove_later[key_r]=value_r
                        change = True
                fine_as_is = dict(fine_as_is.items() | remove_later.items())  # add solved references to usable placeholders
                references = dict(references.items() ^ remove_later.items())  # remove solved references from currently unresolved references
                if not change: # either no more references exist or we hit a loop (eg $#id#$ -> $#psw#$ and $#psw#$ -> $#id#$)
                    break
            try:
                shutil.rmtree('./Output/'+token)
            except FileNotFoundError:
                pass  # folder is new
            # what files to use? ask the db
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cur = conn.cursor()
                cur.execute('SELECT files.*,CASE WHEN files_additional_data.file_id is NULL THEN 0 ELSE files_additional_data.file_position END as `filepos` FROM `configurations v-2`.files left outer join `configurations v-2`.files_additional_data on files.ID = files_additional_data.file_id where Modello=%s',(modello,))
                select = cur.fetchall()
            # TODO accounting for multiple machines, first attempt
            for file in select:
                #ask forgiveness, not permission
                try:
                    snap4.copy('./Modules'+file[3]+file[4], './Output/'+token+'/'+str(ips[file[-1]])+file[3]+file[4])

                except IOError as e:
                # ENOENT(2): file does not exist, raised also on missing dest parent dir
                    if e.errno != errno.ENOENT:
                        raise
                    # try creating parent directories
                    os.makedirs(os.path.dirname('./Output/'+token+'/'+str(ips[file[-1]])+file[3]+file[4]))
                    snap4.copy('./Modules'+file[3]+file[4], './Output/'+token+'/'+str(ips[file[-1]])+file[3]+file[4])
            descriptor=''
            fine_as_is['$#iot-amount#$']=post['# of IoT-Apps']
            if os.environ['send-aws-k8s'] == "True":
                snap4.add_utils('./Output/'+token+'/'+ips[0]+'/kubernetes_eks')
                #this or copy paste the first section of the post_setup.sh
                snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/kubernetes_eks/scripts/virtuoso/run.sh',fine_as_is)
                snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/kubernetes_eks/compatibility4nfs.py',fine_as_is)
            snap4.copy('./checker', './Output/'+token+'/checker')
            for dname, dirs, files in os.walk('./Output/'+token+'/checker'):
                for file in files:
                    try:
                        snap4.placeholders_in_file(os.path.join(dname,file), fine_as_is)
                    except UnicodeDecodeError as E:
                        pass #doesn't matter
            if modello in ("Micro","Kubernetes"):
                for i in range(int(post['# of IoT-Apps'])):
                    snap4.make_iotapp_folder('./Modules/iotapp-id','./Output/'+token+'/'+ips[0],i+1, fine_as_is)
                    if i == 0:
                        snap4.copy('./Modules/iotapp+/flows.json', './Output/'+token+'/'+ips[0]+'/iotapp-001/flows.json')
                        snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/iotapp-001/flows.json', fine_as_is)
                    snap4.make_iotapp_yaml('docker-compose-iotapp.yml','./Output/'+token+'/'+ips[0]+'/', i+1, fine_as_is, 1880+i)
                snap4.make_empty_apache('./Output/'+token+'/'+ips[0]+'/apache-proxy.conf',modello,int(post['# of IoT-Apps'],),1880,fine_as_is)
                #snap4.make_apache_proxy_conf_micro('./Output/'+token+'/'+ips[0]+'/apache-proxy.conf',modello,int(post['# of IoT-Apps'],),1880,fine_as_is)
                snap4.make_sql_micro('./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', 'orion-001', int(post['# of IoT-Apps']),snap4.make_iotb_data(fine_as_is))
                #snap4.remove_heatmap_mentions('./Output/'+token+'/'+ips[0]+'/database/preconfig.sql')
                snap4.fix_coordinates_micro(1, './Output/'+token+'/'+ips[0]+'/database/preconfig.sql', fine_as_is)
                snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', fine_as_is)
                snap4.fix_service_map_config('./Output/'+token+'/'+ips[0]+'/servicemap-conf/servicemap.properties','virtuoso-kb')
                snap4.make_multiple_brokers(1,'./Output/'+token+'/'+ips[0],'docker-compose-iotobsf.yml',fine_as_is)
                snap4.make_nifi_conf('./Output/'+token+'/'+ips[0]+'/nifi/conf/flow.xml.gz',1,fine_as_is)
                snap4.make_ldif('./Output/'+token+'/'+ips[0]+'/ldap', 'default.ldif', ['1000'], ['orion-1'])
                descriptor=post['$#Time#$']+'-'+post['# of IoT-Apps']+'-'

                snap4.merge_sh('./Output/'+token+'/'+ips[0]+'/setup.sh',['./Output/'+token+'/'+ips[0]+'/setup-opensearch.sh'])
                for file in select:
                    try:
                        if file[5] == 3:  # file needs placeholders adjustments
                            snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+file[3]+file[4], fine_as_is)
                        elif file[5] == 2:  # we usually already dealt with special files
                            snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+file[3]+file[4], fine_as_is)
                        elif file[5] == 1:  # file is fine as is
                            pass
                    except FileNotFoundError:
                        #happens if we merge a file into one another before coming here
                        pass
                if modello=='Kubernetes':
                    snap4.merge_sh('./Output/'+token+'/'+ips[0]+'/setup-virtuoso.sh',['./Output/'+token+'/'+ips[0]+'/post-setup-kubernetes.sh'])
                else:
                    snap4.merge_sh('./Output/'+token+'/'+ips[0]+'/setup-virtuoso.sh',['./Output/'+token+'/'+ips[0]+'/post-setup.sh'])
                os.rename('./Output/'+token+'/'+ips[0]+'/setup-virtuoso.sh','./Output/'+token+'/'+ips[0]+'/post-setup.sh')
                if fine_as_is["$#base-protocol#$"] == "https":
                    snap4.fixvarnish('./Output/'+token+'/'+ips[0]+'/varnish/varnish-conf/default.vcl', False)
                    snap4.make_ngnix_micro_ssl('./Output/'+token+'/'+ips[0]+'/nginx-proxy-conf',int(post['# of IoT-Apps'],),1880,fine_as_is)
                    snap4.copy('./Modules/enc.sh', './Output/'+token+'/'+ips[0]+'/letsencrypt.sh')
                    snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/letsencrypt.sh', fine_as_is)
                    with open('./Output/'+token+'/'+ips[0]+'/post-setup.sh', 'r') as f:
                        quick_fix=f.read()
                        quick_fix="""#!/bin/bash

read -p "Did you run the certificate generation yet? (yes/no) " yn

case $yn in
	yes ) echo Proceeding with post_setup...;;
	no ) echo It is expected to run the certificate generation before running this file. Go execute it before running this script again;
		exit;;
	* ) echo Invalid response;
		exit 1;;
esac
""" + quick_fix
                    with open('./Output/'+token+'/'+ips[0]+'/post-setup.sh', 'w') as f:
                        f.write(quick_fix)
                else:
                    snap4.fixvarnish('./Output/'+token+'/'+ips[0]+'/varnish/varnish-conf/default.vcl', True)
                    snap4.make_ngnix_micro('./Output/'+token+'/'+ips[0]+'/nginx-proxy-conf',int(post['# of IoT-Apps'],),1880,fine_as_is)

                snap4.merge_yaml('./Output/'+token+'/'+ips[0])
                if modello == 'Kubernetes':
                    snap4.copy('./Modules/kubernetes_README.md', './Output/'+token+'/'+ips[0]+'/kubernetes_README.md')
                    snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/kubernetes_README.md',fine_as_is)
                    snap4.docker_to_kubernetes('./Output/'+token+'/'+ips[0],fine_as_is['$#base-hostname#$'],fine_as_is['$#k8-namespace#$'])

            #refactor
            elif modello == "Normal":
                iotbrokers = fine_as_is['# of Iot-Brokers']
                for i in range(int(post['# of IoT-Apps'])):  #iotapps go in second vm, hence the second folder
                    snap4.make_iotapp_folder('./Modules/iotapp-id','./Output/'+token+'/'+ips[1],i+1, fine_as_is)
                    if i == 0:
                        snap4.copy('./Modules/iotapp+n/flows.json', './Output/'+token+'/'+ips[1]+'/iotapp-001/flows.json')
                        snap4.placeholders_in_file('./Output/'+token+'/'+ips[1]+'/iotapp-001/flows.json', fine_as_is)
                        snap4.make_iotapp_yaml('docker-compose-iotapp-checker-normal.yml','./Output/'+token+'/'+ips[1]+'/', i+1, fine_as_is, 1880+i)
                    else:
                        snap4.make_iotapp_yaml('docker-compose-iotapp.yml','./Output/'+token+'/'+ips[1]+'/', i+1, fine_as_is, 1880+i)
                #make_apache_proxy_conf_normal('./Output/'+token+'/'+ips[0]+'/apache-proxy.conf',modello,int(post['# of IoT-Apps']),1880,fine_as_is)
                snap4.make_empty_apache('./Output/'+token+'/'+ips[0]+'/apache-proxy.conf',modello,int(post['# of IoT-Apps']),1880,fine_as_is)
                snap4.fix_service_map_config('./Output/'+token+'/'+ips[0]+'/servicemap-conf/servicemap.properties','virtuoso-kb')
                snap4.make_multiple_brokers(iotbrokers,'./Output/'+token+'/'+ips[1],'docker-compose-iotobsf-normal.yml',fine_as_is)
                snap4.make_sql_normal('./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', 'orion-001', int(post['# of IoT-Apps']),snap4.make_iotb_data(fine_as_is))
                snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', fine_as_is)
                snap4.make_nifi_conf('./Output/'+token+'/'+ips[0]+'/nifi/conf/flow.xml.gz',int(iotbrokers),fine_as_is)
                descriptor=post['$#Time#$']+'-'+post['# of IoT-Apps']+'-'+iotbrokers+'-'
                if int(iotbrokers) == 1:
                    snap4.make_ldif('./Output/'+token+'/'+ips[0]+'/ldap', 'default.ldif', ['1000'], ['orion-1'])
                elif int(iotbrokers) == 2:
                    snap4.make_ldif('./Output/'+token+'/'+ips[0]+'/ldap', 'default.ldif', ['1000','1001'], ['orion-1','orion-2'],2)

                # after files are in order, fix the placeholders
                # don't put old folder
                for file in select:
                    if file[5] == 3:  # file needs placeholders adjustments
                        snap4.placeholders_in_file('./Output/'+token+'/'+str(ips[file[-1]])+file[3]+file[4], fine_as_is)
                    elif file[5] == 2:  # we usually already dealt with special files
                        snap4.placeholders_in_file('./Output/'+token+'/'+str(ips[file[-1]])+file[3]+file[4], fine_as_is)
                    elif file[5] == 1:  # file is fine as is
                        pass
                snap4.merge_sh('./Output/'+token+'/'+ips[0]+'/setup.sh',['./Output/'+token+'/'+ips[0]+'/setup-nifi.sh','./Output/'+token+'/'+ips[0]+'/setup-servicemap.sh','./Output/'+token+'/'+ips[0]+'/setup-iot-directory.sh','./Output/'+token+'/'+ips[0]+'/setup-opensearch.sh'])
                snap4.merge_sh('./Output/'+token+'/'+ips[0]+'/setup-virtuoso.sh',['./Output/'+token+'/'+ips[0]+'/post-setup.sh'])
                os.rename('./Output/'+token+'/'+ips[0]+'/setup-virtuoso.sh','./Output/'+token+'/'+ips[0]+'/post-setup.sh')
                if fine_as_is["$#base-protocol#$"] == "https":
                    snap4.fixvarnish('./Output/'+token+'/'+ips[0]+'/varnish/varnish-conf/default.vcl', False)
                    snap4.make_ngnix_normal_ssl('./Output/'+token+'/'+ips[0]+'/nginx-proxy-conf',int(post['# of IoT-Apps'],),1880,fine_as_is)
                    snap4.copy('./Modules/enc.sh', './Output/'+token+'/'+ips[0]+'/letsencrypt.sh')
                    snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/letsencrypt.sh', fine_as_is)
                    with open('./Output/'+token+'/'+ips[0]+'/post-setup.sh', 'r') as f:
                        quick_fix=f.read()
                        quick_fix="""#!/bin/bash

read -p "Did you run the certificate generation yet? (yes/no) " yn

case $yn in
	yes ) echo Proceeding with post_setup...;;
	no ) echo It is expected to run the certificate generation before running this file. Go execute it before running this script again;
		exit;;
	* ) echo Invalid response;
		exit 1;;
esac
""" + quick_fix
                    with open('./Output/'+token+'/'+ips[0]+'/post-setup.sh', 'w') as f:
                        f.write(quick_fix)
                else:
                    snap4.fixvarnish('./Output/'+token+'/'+ips[0]+'/varnish/varnish-conf/default.vcl', True)
                    snap4.make_ngnix_normal('./Output/'+token+'/'+ips[0]+'/nginx-proxy-conf',int(post['# of IoT-Apps'],),1880,fine_as_is)


                for i in range(len(ips)): # one single compose in each VM
                    snap4.merge_yaml('./Output/'+token+'/'+ips[i])
            elif modello == "Small":
                iotbrokers = fine_as_is['# of Iot-Brokers']
                for i in range(int(post['# of IoT-Apps'])):  #iotapps go in fourth vm
                    snap4.make_iotapp_folder('./Modules/iotapp-id','./Output/'+token+'/'+ips[3],i+1, fine_as_is)
                    snap4.make_iotapp_yaml('docker-compose-iotapp.yml','./Output/'+token+'/'+ips[3]+'/', i+1, fine_as_is, 1880+i)
                #make_apache_proxy_conf_small('./Output/'+token+'/'+ips[0]+'/apache-proxy.conf',modello,int(post['# of IoT-Apps']),1880,fine_as_is)
                descriptor=post['$#Time#$']+'-'+post['# of IoT-Apps']+'-'+iotbrokers+'-'
                snap4.make_empty_apache('./Output/'+token+'/'+ips[0]+'/apache-proxy.conf',modello,int(post['# of IoT-Apps']),1880,fine_as_is)
                snap4.fix_service_map_config('./Output/'+token+'/'+ips[2]+'/servicemap-conf/servicemap.properties','virtuoso-kb')
                snap4.make_multiple_brokers(iotbrokers,'./Output/'+token+'/'+ips[3],'docker-compose-iotobsf-small.yml',fine_as_is)
                snap4.make_sql_small('./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', './Output/'+token+'/'+ips[0]+'/database/preconfig.sql', ips[3], int(post['# of IoT-Apps']),snap4.make_iotb_data(fine_as_is))
                snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', fine_as_is)
                snap4.make_nifi_conf('./Output/'+token+'/'+ips[2]+'/nifi/conf/flow.xml.gz',int(iotbrokers),fine_as_is)
                if int(iotbrokers) == 1:
                    snap4.make_ldif('./Output/'+token+'/'+ips[1]+'/ldap', 'default.ldif', ['1000'], ['orion-1'])
                elif int(iotbrokers) == 2:
                    snap4.make_ldif('./Output/'+token+'/'+ips[1]+'/ldap', 'default.ldif', ['1000','1001'], ['orion-1','orion-2'],2)

                for file in select:
                    if file[5] == 3:  # file needs placeholders adjustments
                        snap4.placeholders_in_file('./Output/'+token+'/'+str(ips[file[-1]])+file[3]+file[4], fine_as_is)
                    elif file[5] == 2:  # we usually already dealt with special files
                        snap4.placeholders_in_file('./Output/'+token+'/'+str(ips[file[-1]])+file[3]+file[4], fine_as_is)
                    elif file[5] == 1:  # file is fine as is
                        pass
                for i in range(len(ips)): # one single compose in each VM
                    snap4.merge_yaml('./Output/'+token+'/'+ips[i])
                snap4.merge_sh('./Output/'+token+'/'+ips[2]+'/pre-post-setup.sh',['./Output/'+token+'/'+ips[2]+'/pre-post-setup.sh','./Output/'+token+'/'+ips[2]+'/small.sh'])
                os.rename('./Output/'+token+'/'+ips[2]+'/pre-post-setup.sh','./Output/'+token+'/'+ips[2]+'/post-setup.sh')
                if fine_as_is["$#base-protocol#$"] == "https":
                    snap4.make_ngnix_small_ssl('./Output/'+token+'/'+ips[0]+'/nginx-proxy-conf',int(post['# of IoT-Apps'],),1880,fine_as_is)
                    snap4.copy('./Modules/enc.sh', './Output/'+token+'/'+ips[0]+'/letsencrypt.sh')
                    snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/letsencrypt.sh', fine_as_is)
                    with open('./Output/'+token+'/'+ips[0]+'/post-setup.sh', 'r') as f:
                        quick_fix=f.read()
                        quick_fix="""#!/bin/bash

read -p "Did you run the certificate generation yet? (yes/no) " yn

case $yn in
	yes ) echo Proceeding with post_setup...;;
	no ) echo It is expected to run the certificate generation before running this file. Go execute it before running this script again;
		exit;;
	* ) echo Invalid response;
		exit 1;;
esac
""" + quick_fix
                    with open('./Output/'+token+'/'+ips[0]+'/post-setup.sh', 'w') as f:
                        f.write(quick_fix)
                else:
                    snap4.make_ngnix_small('./Output/'+token+'/'+ips[0]+'/nginx-proxy-conf',int(post['# of IoT-Apps'],),1880,fine_as_is)

            elif modello == "DataCitySmall":
                iotbrokers = fine_as_is['# of Iot-Brokers']
                for i in range(int(post['# of IoT-Apps'])):  #iotapps go in sixth vm
                    snap4.make_iotapp_folder('./Modules/iotapp-id','./Output/'+token+'/'+ips[5],i+1, fine_as_is)
                    snap4.make_iotapp_yaml('docker-compose-iotapp.yml','./Output/'+token+'/'+ips[5]+'/', i+1, fine_as_is, 1880+i)
                if int(iotbrokers) == 1:
                    snap4.make_ldif('./Output/'+token+'/'+ips[1]+'/ldap', 'default.ldif', ['1000'], ['orion-1'])
                elif int(iotbrokers) == 2:
                    snap4.make_ldif('./Output/'+token+'/'+ips[1]+'/ldap', 'default.ldif', ['1000','1001'], ['orion-1','orion-2'],2)
                descriptor=post['$#Time#$']+'-'+post['# of IoT-Apps']+'-'+iotbrokers+'-'+fine_as_is['# of ServiceMaps']+'-'
                snap4.make_nifi_conf('./Output/'+token+'/'+ips[2]+'/nifi/conf/flow.xml.gz',int(iotbrokers),fine_as_is)
                snap4.make_multiple_brokers(iotbrokers,'./Output/'+token+'/'+ips[3],'docker-compose-iotobsf-datacitysmall.yml',fine_as_is)
                snap4.make_empty_apache('./Output/'+token+'/'+ips[0]+'/apache-proxy.conf',modello,int(post['# of IoT-Apps']),1880,fine_as_is)
                #make_apache_proxy_conf_dcs('./Output/'+token+'/'+ips[0]+'/apache-proxy.conf',modello,int(post['# of IoT-Apps']),1880,fine_as_is)
                snap4.make_sql_dcs('./Output/'+token+'/'+ips[0]+'/database/preconfig.sql','./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', ips[5], int(post['# of IoT-Apps']),snap4.make_iotb_data(fine_as_is))
                snap4.make_n_servicemaps(fine_as_is['# of ServiceMaps'],'./Output/'+token+'/'+ips[4], fine_as_is)
                for n in range(int(fine_as_is['# of ServiceMaps'])):
                    snap4.copy('./Modules/setup-servicemap-dcs.sh','./Output/'+token+'/'+ips[4]+'/setup-servicemap-dcs-'+str(n+1).zfill(3)+'.sh')
                    snap4.copy('./Modules/post-setup-dcs.sh','./Output/'+token+'/'+ips[4]+'/dcs-'+str(n+1).zfill(3)+'.sh')
                    fine_as_is['$#id#$']=str(n+1).zfill(3)
                    snap4.placeholders_in_file('./Output/'+token+'/'+ips[4]+'/setup-servicemap-dcs-'+str(n+1).zfill(3)+'.sh', fine_as_is)
                    snap4.placeholders_in_file('./Output/'+token+'/'+ips[4]+'/dcs-'+str(n+1).zfill(3)+'.sh', fine_as_is)
                    fine_as_is.pop('$#id#$')
                    snap4.merge_sh('./Output/'+token+'/'+ips[4]+'/setup.sh',['./Output/'+token+'/'+ips[4]+'/setup-servicemap-dcs-'+str(n+1).zfill(3)+'.sh'])
                    snap4.merge_sh('./Output/'+token+'/'+ips[4]+'/post-setup.sh',['./Output/'+token+'/'+ips[4]+'/dcs-'+str(n+1).zfill(3)+'.sh'])
                    snap4.fix_service_map_config('./Output/'+token+'/'+ips[4]+'/servicemap-'+str(n+1).zfill(3)+'-conf/servicemap.properties','virtuoso-kb-'+str(n+1).zfill(3))
                snap4.adjust_dashboard_menu_dump_servicemaps(fine_as_is['# of ServiceMaps'],'./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', fine_as_is)
                snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', fine_as_is)
                for file in select:
                    if file[5] == 3:  # file needs placeholders adjustments
                        snap4.placeholders_in_file('./Output/'+token+'/'+str(ips[file[-1]])+file[3]+file[4], fine_as_is)
                    elif file[5] == 2:  # we usually already dealt with special files
                        snap4.placeholders_in_file('./Output/'+token+'/'+str(ips[file[-1]])+file[3]+file[4], fine_as_is)
                    elif file[5] == 1:  # file is fine as is
                        pass
                for i in range(len(ips)): # one single compose in each VM
                    snap4.merge_yaml('./Output/'+token+'/'+ips[i])
                snap4.merge_sh('./Output/'+token+'/'+ips[2]+'/pre-post-setup.sh',['./Output/'+token+'/'+ips[2]+'/pre-post-setup.sh','./Output/'+token+'/'+ips[2]+'/kibana.sh'])
                os.rename('./Output/'+token+'/'+ips[2]+'/pre-post-setup.sh','./Output/'+token+'/'+ips[2]+'/post-setup.sh')
                if fine_as_is["$#base-protocol#$"] == "https":
                    snap4.make_ngnix_dcs_ssl('./Output/'+token+'/'+ips[0]+'/nginx-proxy-conf',int(post['# of IoT-Apps'],),1880,fine_as_is,fine_as_is['# of ServiceMaps'])
                    snap4.copy('./Modules/enc.sh', './Output/'+token+'/'+ips[0]+'/letsencrypt.sh')
                    snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/letsencrypt.sh', fine_as_is)
                    with open('./Output/'+token+'/'+ips[0]+'/post-setup.sh', 'r') as f:
                        quick_fix=f.read()
                        quick_fix="""#!/bin/bash

read -p "Did you run the certificate generation yet? (yes/no) " yn

case $yn in
	yes ) echo Proceeding with post_setup...;;
	no ) echo It is expected to run the certificate generation before running this file. Go execute it before running this script again;
		exit;;
	* ) echo Invalid response;
		exit 1;;
esac
""" + quick_fix
                    with open('./Output/'+token+'/'+ips[0]+'/post-setup.sh', 'w') as f:
                        f.write(quick_fix)
                else:
                    snap4.make_ngnix_dcs('./Output/'+token+'/'+ips[0]+'/nginx-proxy-conf',int(post['# of IoT-Apps'],),1880,fine_as_is,fine_as_is['# of ServiceMaps'])

            elif modello == "DataCityMedium":
                descriptor=post['$#Time#$']+'-IoT'+post['# of IoT-Apps']+'-IoB'+post['# of Iot-Broker servers']+'-SVM'+post['# of ServiceMaps']+'-OSN'+post['# of Nifi nodes']+'-NIFI'+post['# of Nifi nodes']+'-VIRT'+post['# of ServiceMaps']+'-'
                list_iotapp=[value for (key,value) in sorted(detailed_ips.items()) if "iotapp" in key]
                list_nifi=[value for (key,value) in sorted(detailed_ips.items()) if "nifi" in key]
                list_opensearch=list_nifi
                list_broker=[value for (key,value) in sorted(detailed_ips.items()) if "broker" in key]
                list_virtuoso=[value for (key,value) in sorted(detailed_ips.items()) if "virtuoso" in key]
                #we need to fix a few values in fine_as_is
                fine_as_is['$#superservicemap-db-host#$']=list_virtuoso[0]
                fine_as_is['$#ip-nifi#$']=list_nifi[0]
                fine_as_is['$#elasticsearch-host#$']=list_opensearch[0]


                snap4.make_sql_dcm('./Output/'+token+'/'+ips[0]+'/database/preconfig.sql','./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', list_broker, int(post['# of IoT-Apps']),snap4.make_iotb_data(fine_as_is))
                snap4.make_multiple_nifi(ips[1], ips[4], list_opensearch[0], list_nifi, token, ips[1])
                for broker in enumerate(list_broker):
                    snap4.make_multiple_brokers(broker[0],'./Output/'+token+'/'+broker[1],'docker-compose-iotobsf.yml',fine_as_is)
                snap4.adjust_dashboard_menu_dump_servicemaps(fine_as_is['# of ServiceMaps'],'./Output/'+token+'/'+ips[0]+'/database/preconfig.sql', fine_as_is)

                snap4.make_empty_apache('./Output/'+token+'/'+ips[0]+'/apache-proxy.conf',modello,int(post['# of IoT-Apps']),1880,fine_as_is)
                for nifi in list_nifi:
                    snap4.make_nifi_conf('./Output/'+token+'/'+nifi+'/nifi/conf/flow.xml.gz',len(list_broker),fine_as_is)
                snap4.copy('./Modules/setup-nifi-multi.sh', './Output/'+token+'/'+list_nifi[0]+'/setup.sh')
                with open('./Output/'+token+'/'+list_nifi[0]+'/setup.sh','r') as fo:
                    read=fo.read()
                read=read.replace('$#nifi-ips#$',','.join(list_nifi))
                with open('./Output/'+token+'/'+list_nifi[0]+'/setup.sh','w') as fo:
                    fo.write(read)
                #snap4.make_n_servicemaps(2,'./Output/'+token+'/'+list_virtuoso[0], fine_as_is)
                for i in range(len(list_virtuoso)):
                    try:
                        snap4.make_n_servicemaps(1,'./Output/'+token+'/'+list_virtuoso[i], fine_as_is,i)
                    except Exception as E:
                        print(E)
                for i in range(len(list_virtuoso)):
                    snap4.copy('./Modules/setup-servicemap-dcs.sh','./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/setup-servicemap-dcs-'+str(i+1).zfill(3)+'.sh')
                    snap4.copy('./Modules/post-setup-dcs.sh','./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/dcs-'+str(i+1).zfill(3)+'.sh')
                    fine_as_is['$#id#$']=str(i+1).zfill(3)
                    snap4.placeholders_in_file('./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/setup-servicemap-dcs-'+str(i+1).zfill(3)+'.sh', fine_as_is)
                    snap4.placeholders_in_file('./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/dcs-'+str(i+1).zfill(3)+'.sh', fine_as_is)
                    fine_as_is.pop('$#id#$')
                    snap4.merge_sh('./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/setup.sh',['./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/setup-servicemap-dcs-'+str(i+1).zfill(3)+'.sh'])
                    snap4.merge_sh('./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/post-setup.sh',['./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/dcs-'+str(i+1).zfill(3)+'.sh'])
                for i in range(int(fine_as_is['# of ServiceMaps'])):
                    for j in range(len(list_virtuoso)):
                        snap4.fix_service_map_config('./Output/'+token+'/'+list_virtuoso[j]+'/servicemap-'+str(i+1).zfill(3)+'-conf/servicemap.properties','virtuoso-kb-'+str(i+1).zfill(3))

                snap4.make_ldif_multi('./Output/'+token+'/'+ips[1]+'/ldap', '\ldap\default_1.ldif',len(list_broker))
                # TODO review second parameter
                snap4.make_multiple_opensearch(len(list_opensearch), ips[0], ips[1], token, list_opensearch)
                for i in range(int(post['# of IoT-Apps'])):  # distribute iotapps
                    snap4.make_iotapp_folder('./Modules/iotapp-id','./Output/'+token+'/'+list_iotapp[i%len(list_iotapp)],i+1, fine_as_is)
                    if i == 0:
                        snap4.copy('./Modules/iotapp+/flows.json', './Output/'+token+'/'+list_iotapp[i%len(list_iotapp)]+'/iotapp-001/flows.json')
                        snap4.placeholders_in_file('./Output/'+token+'/'+list_iotapp[i%len(list_iotapp)]+'/iotapp-001/flows.json', fine_as_is)
                    snap4.make_iotapp_yaml('docker-compose-iotapp.yml','./Output/'+token+'/'+list_iotapp[i%len(list_iotapp)]+'/', i+1, fine_as_is, 1880+i)

                for dname, dirs, files in os.walk('./Output/'+token+'/'):
                    for file in files:
                        try:
                            snap4.placeholders_in_file(os.path.join(dname,file), fine_as_is)
                        except UnicodeDecodeError as E:
                            pass #doesn't matter
                for i in range(len(ips)): # one single compose in each VM
                    snap4.merge_yaml('./Output/'+token+'/'+ips[i])

                if fine_as_is["$#base-protocol#$"] == "https":
                    snap4.make_ngnix_dcm_ssl(fine_as_is, './Output/'+token+'/'+ips[0]+'/nginx-proxy-conf', int(post['# of IoT-Apps']), list_iotapp, list_virtuoso, ips[1], list_opensearch[0], ips[4], 1880, list_broker)
                    snap4.copy('./Modules/enc.sh', './Output/'+token+'/'+ips[0]+'/letsencrypt.sh')
                    snap4.placeholders_in_file('./Output/'+token+'/'+ips[0]+'/letsencrypt.sh', fine_as_is)
                    with open('./Output/'+token+'/'+ips[0]+'/post-setup.sh', 'r') as f:
                        quick_fix=f.read()
                        quick_fix="""#!/bin/bash

read -p "Did you run the certificate generation yet? (yes/no) " yn

case $yn in
	yes ) echo Proceeding with post_setup...;;
	no ) echo It is expected to run the certificate generation before running this file. Go execute it before running this script again;
		exit;;
	* ) echo Invalid response;
		exit 1;;
esac
""" + quick_fix
                    with open('./Output/'+token+'/'+ips[0]+'/post-setup.sh', 'w') as f:
                        f.write(quick_fix)
                else:
                    snap4.make_ngnix_dcm(fine_as_is, './Output/'+token+'/'+ips[0]+'/nginx-proxy-conf', int(post['# of IoT-Apps']), list_iotapp, list_virtuoso, ips[1], list_opensearch[0], ips[4], 1880, list_broker)

            elif modello == "DataCityLarge":
                #todo review ips, empty apache, ngnix config
                descriptor=post['$#Time#$']+'-IoT'+post['# of IoT-Apps']+'-IoB'+post['# of Iot-Broker servers']+'-SVM'+post['# of ServiceMaps']+'-OSN'+post['# of Opensearch nodes']+'-NIFI'+post['# of Nifi nodes']+'-VIRT'+post['# of ServiceMaps']+'-'
                list_iotapp=[value for (key,value) in sorted(detailed_ips.items()) if "iotapp" in key]
                list_opensearch=[value for (key,value) in sorted(detailed_ips.items()) if "opensearch" in key]
                list_nifi=[value for (key,value) in sorted(detailed_ips.items()) if "nifi" in key]
                list_broker=[value for (key,value) in sorted(detailed_ips.items()) if "broker" in key]
                list_virtuoso=[value for (key,value) in sorted(detailed_ips.items()) if "virtuoso" in key]

                #we need to fix a few values in fine_as_is
                fine_as_is['$#superservicemap-db-host#$']=list_virtuoso[0]
                fine_as_is['$#ip-nifi#$']=list_nifi[0]
                fine_as_is['$#elasticsearch-host#$']=list_opensearch[0]

                snap4.make_ngnix_dcl(fine_as_is, './Output/'+token+'/'+ips[0]+'/nginx-proxy-conf', int(post['# of IoT-Apps']), list_iotapp, list_virtuoso, ips[1], list_opensearch[0], ips[4], 1880)

                snap4.make_sql_dcl('./Output/'+token+'/'+ips[4]+'/database/preconfig.sql','./Output/'+token+'/'+ips[4]+'/database/preconfig.sql', list_broker, int(post['# of IoT-Apps']),snap4.make_iotb_data(fine_as_is))
                snap4.make_multiple_nifi(ips[1], ips[4], list_opensearch[0], list_nifi, token, ips[1])
                for broker in list_broker:
                    snap4.make_multiple_brokers(1,'./Output/'+token+'/'+broker,'docker-compose-iotobsf.yml',fine_as_is)
                snap4.adjust_dashboard_menu_dump_servicemaps(fine_as_is['# of ServiceMaps'],'./Output/'+token+'/'+ips[4]+'/database/preconfig.sql', fine_as_is)

                snap4.make_empty_apache('./Output/'+token+'/'+ips[0]+'/apache-proxy.conf',modello,int(post['# of IoT-Apps']),1880,fine_as_is)
                for nifi in list_nifi:
                    snap4.make_nifi_conf('./Output/'+token+'/'+nifi+'/nifi/conf/flow.xml.gz',len(list_broker),fine_as_is)
                for i in range(len(list_virtuoso)):
                    snap4.make_n_servicemaps(2,'./Output/'+token+'/'+list_virtuoso[i], fine_as_is)
                for i in range(len(list_virtuoso)*2):
                    snap4.copy('./Modules/setup-servicemap-dcs.sh','./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/setup-servicemap-dcs-'+str(i+1).zfill(3)+'.sh')
                    snap4.copy('./Modules/post-setup-dcs.sh','./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/post-setup-dcs-'+str(i+1).zfill(3)+'.sh')
                    fine_as_is['$#id#$']=str(i+1).zfill(3)
                    snap4.placeholders_in_file('./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/setup-servicemap-dcs-'+str(i+1).zfill(3)+'.sh', fine_as_is)
                    snap4.placeholders_in_file('./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/post-setup-dcs-'+str(i+1).zfill(3)+'.sh', fine_as_is)
                    fine_as_is.pop('$#id#$')
                    snap4.merge_sh('./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/setup.sh',['./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/setup-servicemap-dcs-'+str(i+1).zfill(3)+'.sh'])
                    snap4.merge_sh('./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/post-setup.sh',['./Output/'+token+'/'+list_virtuoso[i%int(fine_as_is['# of ServiceMaps'])]+'/post-setup-dcs-'+str(i+1).zfill(3)+'.sh'])
                for i in range(2):
                    for j in range(len(list_virtuoso)):
                        snap4.fix_service_map_config('./Output/'+token+'/'+list_virtuoso[j]+'/servicemap-'+str(i+1).zfill(3)+'-conf/servicemap.properties','virtuoso-kb-'+str(i+1).zfill(3))

                snap4.make_ldif_multi('./Output/'+token+'/'+ips[1]+'/ldap', '\ldap\default_1.ldif',len(list_broker))
                snap4.adjust_dashboard_menu_dump_servicemaps(fine_as_is['# of ServiceMaps'],'./Output/'+token+'/'+ips[4]+'/database/preconfig.sql', fine_as_is)
                # TODO review second parameter
                snap4.make_multiple_opensearch(len(list_opensearch), ips[0], ips[1], token, list_opensearch)
                for i in range(int(post['# of IoT-Apps'])):  # distribute iotapps
                    snap4.make_iotapp_folder('./Modules/iotapp-id','./Output/'+token+'/'+list_iotapp[i%len(list_iotapp)],i+1, fine_as_is)
                    if i == 0:
                        snap4.copy('./Modules/iotapp+/flows.json', './Output/'+token+'/'+list_iotapp[i%len(list_iotapp)]+'/iotapp-001/flows.json')
                        snap4.placeholders_in_file('./Output/'+token+'/'+list_iotapp[i%len(list_iotapp)]+'/iotapp-001/flows.json', fine_as_is)
                    snap4.make_iotapp_yaml('docker-compose-iotapp.yml','./Output/'+token+'/'+list_iotapp[i%len(list_iotapp)]+'/', i+1, fine_as_is, 1880+i)

                for dname, dirs, files in os.walk('./Output/'+token+'/'):
                    for file in files:
                        try:
                            snap4.placeholders_in_file(os.path.join(dname,file), fine_as_is)
                        except UnicodeDecodeError as E:
                            pass #doesn't matter
                for i in range(len(ips)): # one single compose in each VM
                    snap4.merge_yaml('./Output/'+token+'/'+ips[i])


            else:
                return None  # summons error 500
            try:
                os.remove("./Output/"+token+'./compressed.zip')
            except FileNotFoundError:
                pass  # not a problem, we are deleting the file
            
            fine_as_is["Token"]=token
            fine_as_is["version"]=os.environ["version"]
            #we'll be sorting a directory by key (so it's the placeholder) for the sake of reading it better by human eye
            if os.environ['send_placeholders'] == 'True':
                with open("./Output/"+token+'/placeholder_used.tsv','w') as f:
                    for key, value in {k: v for k, v in sorted(fine_as_is.items(), key=lambda item: item[0])}.items():
                        f.write(key+'\t'+value+'\n')
            shutil.make_archive('compressed', 'zip', "./Output/"+token)  #pack the folder
            #with tarfile.open('compressed.tar.gz', "w:gz", compresslevel=9) as tar:
                #tar.add("./Output/"+token, arcname=os.path.basename("./Output/"+token))
            print('Sending',modello+descriptor+token+'-config.zip')
            return send_file('./compressed.zip', download_name=os.environ["version"]+'-'+modello+'-'+descriptor+token+'-config.zip') #send the pack


    @app.route("/get_updating_tools", methods=['POST','GET'])
    def send_update_stuff():
        shutil.make_archive('updates', 'zip', "./updates")
        return send_file('./updates.zip', 'update-utilities.zip')
    
    # saving a configuration in the database
    @app.route("/saving_conf", methods=['POST','GET'])
    def saving_configuration():
        if request.method == 'GET':
            return
        else:
            form_to_add = request.form.to_dict()
            token=form_to_add.pop('token')
            toret=''
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cur = conn.cursor()
                cur.execute("SELECT token from saved_configurations where token=%s limit 1",(token,))
                result=cur.fetchall()
                if len(result)>0:
                    toret+='Your configuration already exists in the database.'
                else:
                    for key, value in form_to_add.items():
                        cur = conn.cursor()
                        cur.execute('insert into saved_configurations values (%s,%s,%s)', (token,key,value))
                        conn.commit()
                    toret+="Your configuration has been added to the database, don't forget to save your token!"
            return toret

    # configuration exists?
    @app.route("/conf_exists", methods=['POST','GET'])
    def checking_configuration():
        if request.method == 'GET':
            return
        else:
            form_to_add = request.form.to_dict()
            token=form_to_add.pop('token_value')
            if re.match('^[abcdef\d]{40}$', token):
                with closing(mysql.connector.connect(**db_conn_info)) as conn:
                    cur = conn.cursor()
                    cur.execute("SELECT token from saved_configurations where token=%s limit 1",(token,))
                    result=cur.fetchall()
                    if len(result)>0:
                        return 'true' #the framework gets mad if I return a boolean, so i need to cast it client side
                    return 'false'
            else: #don't bother checking, not a valid token
                return 'false'

    @app.route('/download/<download>')
    def download_file(download=''):
        if os.path.isdir('./Output/'+download):
            # send file
            shutil.make_archive('compressed', 'zip', "./Output/"+download)  #pack the folder
            #todo calculate the model
            return send_file('./compressed.zip', download_name=download+'-config.zip') #send the pack
        else: # config was never generated
            with closing(mysql.connector.connect(**db_conn_info)) as conn:
                cur = conn.cursor()
                cur.execute("SELECT token from saved_configurations where token=%s and Placeholder='Model name' limit 1",(download,))
                result=cur.fetchall()
                if len(result)>0:  # config is saved in database
                    return render_template('no_download.html', token=download)
                # config doesn't exists
                return render_template('no_download.html', token=None)

# HERE
    return app

if __name__ == "__main__":
    create_app().run(host='0.0.0.0', port=80)
