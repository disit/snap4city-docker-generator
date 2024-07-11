'''Copyright (C) 2023 DISIT Lab http://www.disit.org - University of Florence

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.'''
import subprocess
from flask import Flask, jsonify, render_template, request, send_file
import requests
import mysql.connector
import json
import os
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import telegram
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
import base64
import random
import string
import traceback
from urllib.parse import urlparse
from datetime import datetime

f = open("conf.json")
config = json.load(f)


API_TOKEN = config['telegram-api-token']

greendot = """<svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="green"/></svg>"""
reddot = """<svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="red"/></svg>"""

# edit this block according to your mysql server's configuration
db_conn_info = {
        "user": config['db-user'],
        "passwd": config['db-passwd'],
        "host": config['db-host'],
        "port": config['db-port'],
        "database": "checker",
        "auth_plugin": 'mysql_native_password'
    }

def send_telegram(chat_id, message):
    bot = telegram.Bot(token=API_TOKEN)
    asyncio.run(bot.send_message(chat_id=chat_id, text=message))
    return

def send_email(sender_email, sender_password, receiver_emails, subject, message):
    smtp_server = config['smtp-server']
    smtp_port = config['smtp-port']
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ','.join(receiver_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server.send_message(msg)
    server.quit()
    return

def isalive():
    try:
        send_email(config["sender-email"], config["sender-email-password"], config["email-recipients"], config["platform-url"]+" is alive", config["platform-url"]+" is alive")
        send_telegram(config['telegram-channel'], config["platform-url"]+" is alive")
    except Exception:
        print("Something went wrong:", traceback.print_exc())
    return

def auto_run_tests():
    try:
        with mysql.connector.connect(**db_conn_info) as conn:
            cursor = conn.cursor(buffered=True)
            # to run malicious code, malicious code must be present in the db or the machine in the first place
            query = '''select command from tests_table;'''
            cursor.execute(query)
            conn.commit()
            results = cursor.fetchall()
            total_result = ""
            badstuff = ""
            for r in list(results):
                command_ran = subprocess.run(r[0], shell=True, capture_output=True, text=True, encoding="cp437").stdout
                total_result += command_ran
                if "Failure" in command_ran:
                    badstuff += r[0] + " resulted in " + command_ran + "\n"
            return badstuff
    except Exception:
        print("Something went wrong during tests running because of:",traceback.print_exc())

def auto_alert_status():
    containers_ps = [a for a in (subprocess.run('docker ps --format json -a', shell=True, capture_output=True, text=True, encoding="utf_8").stdout).split('\n')][:-1]
    containers_stats = [b for b in (subprocess.run('docker stats --format json -a --no-stream', shell=True, capture_output=True, text=True, encoding="utf_8").stdout).split('\n')][:-1]
    containers_merged = []
    for container_stats in containers_stats:
        for container_ps in containers_ps:
            for key1, value1 in json.loads(container_stats).items():
                for key2, value2 in json.loads(container_ps).items():
                    if key1 == "Name" and key2 == "Names":
                        if value1 == value2:
                            containers_merged.append({**json.loads(container_ps), **json.loads(container_stats)})
    try:
        with mysql.connector.connect(**db_conn_info) as conn:
            cursor = conn.cursor(buffered=True)
            query = '''SELECT * FROM checker.component_to_category;'''
            cursor.execute(query)
            conn.commit()
            results = cursor.fetchall()
    except Exception:
        send_alerts("Can't reach db, auto alert 1, reason:",traceback.print_exc())
        return
    is_alive_with_ports = auto_run_tests()
    categories = [a[0].replace("*","") for a in results]
    containers_which_should_be_running_and_are_not = [c for c in containers_merged if any(c["Names"].startswith(value) for value in categories) and (c["State"] != "running")]
    containers_which_should_be_exited_and_are_not = [c for c in containers_merged if any(c["Names"].startswith(value) for value in ["62149183138_certbot_1"]) and c["State"] != "exited"]
    containers_which_are_running_but_are_not_healthy = [c for c in containers_merged if any(c["Names"].startswith(value) for value in categories) and "unhealthy" in c["Status"]]
    problematic_containers = containers_which_should_be_exited_and_are_not + containers_which_should_be_running_and_are_not + containers_which_are_running_but_are_not_healthy
    #containers_which_are_fine = list(set([n["Names"] for n in containers_merged]) - set([n["Names"] for n in problematic_containers]))
    names_of_problematic_containers = [n["Names"] for n in problematic_containers]
    if len(names_of_problematic_containers) > 0 or len(is_alive_with_ports) > 0:
        try:
            issues = ""
            if len(names_of_problematic_containers) > 0:
                issues = "There are problems with the containers: "+str(problematic_containers) + "\n"
            if len(is_alive_with_ports) > 0:
                issues += is_alive_with_ports
            send_alerts(issues)
        except Exception:
            print("Issues when trying to reach the database due to:",traceback.print_exc())
            send_alerts("Couldn't reach database while sending error messages due to:",traceback.print_exc())
            return
    else:
        try:
            with mysql.connector.connect(**db_conn_info) as conn:
                cursor = conn.cursor(buffered=True)
                update_healthy_categories_query=f"UPDATE `checker`.`summary_status` SET `status` = %s;"
                cursor.execute(update_healthy_categories_query, [greendot])
                conn.commit()
                return
        except Exception:
            send_alerts("Couldn't reach database while not needing to send error messages")
            return

    
def send_alerts(message):
    try:
        send_email(config["sender-email"], config["sender-email-password"], config["email-recipients"], config["platform-url"]+" is in trouble!", message)
        send_telegram(config["platform-url"]+" is alive", message)
    except Exception:
        print("Error while sending alerts: ",traceback.print_exc())
    
    
scheduler = BackgroundScheduler()
scheduler.add_job(auto_alert_status, trigger='interval', minutes=15)
scheduler.add_job(isalive, 'cron', hour=8, minute=0)
scheduler.add_job(isalive, 'cron', hour=20, minute=0)
scheduler.start()
auto_alert_status()
def create_app():
    app = Flask(__name__)
    app.secret_key = b'\x8a\x17\x93kT\xc0\x0b6;\x93\xfdp\x8bLl\xe6u\xa9\xf5x'

    @app.route("/")
    def main_page():
        try:
            with mysql.connector.connect(**db_conn_info) as conn:
                user = ""
                try:
                    user = base64.b64decode(request.headers["Authorization"][len('Basic '):]).decode('utf-8')
                    user = user[:user.find(":")]
                except Exception:
                    pass
                cursor = conn.cursor(buffered=True)
                # to run malicious code, malicious code must be present in the db or the machine in the first place
                query = '''SELECT complex_tests.*, GetHighContrastColor(button_color), COALESCE(categories.category, "System") as category FROM checker.complex_tests left join category_test on id = category_test.test left join categories on categories.idcategories = category_test.category;'''
                cursor.execute(query)
                conn.commit()
                results = cursor.fetchall()
                if user != "admin":
                    return render_template("checker.html",extra=results,categories=get_container_categories(),extra_data=get_extra_data())
                else:
                    query_2 = "SELECT * FROM checker.test_ran order by datetime desc limit 200;"
                    cursor.execute(query_2)
                    conn.commit()
                    results_log = cursor.fetchall()
                    return render_template("checker-admin.html",extra=results,categories=get_container_categories(),extra_data=get_extra_data(),admin_log=results_log)
        except Exception:
            print("Something went wrong because of:",traceback.print_exc())
            return render_template("error_showing.html", r = traceback.print_exc()), 500


    @app.route("/get_data_from_source")
    def get_additional_data():
        if request.method == "GET":
            try:
                response = requests.get(request.args.to_dict()['url_of_resource'])
                response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
                print("\n\n" + response.text + "\n\n")
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None
        else:
            return "<html>You didn't use a GET.</html>"
    
    @app.route("/get_complex_test_buttons")
    def get_complex_test_buttons():
        try:
            with mysql.connector.connect(**db_conn_info) as conn:
                cursor = conn.cursor(buffered=True)
                # to run malicious code, malicious code must be present in the db or the machine in the first place
                query = '''SELECT complex_tests.*, GetHighContrastColor(button_color), COALESCE(categories.category, "System") as category FROM checker.complex_tests left join category_test on id = category_test.test left join categories on categories.idcategories = category_test.category;'''
                cursor.execute(query)
                conn.commit()
                results = cursor.fetchall()
                return results
        except Exception:
            print("Something went wrong because of:",traceback.print_exc())
            return render_template("error_showing.html", r = traceback.print_exc()), 500
        
    @app.route("/container_is_okay", methods=['POST'])
    def make_category_green():
        if request.method == "POST":
            try:
                with mysql.connector.connect(**db_conn_info) as conn:
                    cursor = conn.cursor(buffered=True)
                    update_categories_query=f"""UPDATE `checker`.`summary_status` SET `status` = %s WHERE (`category` = '{request.form.to_dict()['container']}');"""
                    cursor.execute(update_categories_query, [greendot])
                    conn.commit()
                    return "👌"
            except Exception:
                print(traceback.print_exc())
                send_alerts("Can't reach db")
                return "There was a problem: "+traceback.print_exc(), 500
        
    @app.route("/read_containers", methods=['POST','GET'])
    def check():
        if request.method == "POST":
            containers = get_container_data()
            #containers = subprocess.run('docker ps --format json -a', shell=True, capture_output=True, text=True, encoding="utf_8").stdout
            #log_to_db('asking_containers', 'docker ps --format json -a resulted in: '+containers)
            return containers
        else:
            log_to_db('asking_containers', "POST wasn't used in the request", request)
            return False
            
    @app.route("/advanced_read_containers", methods=['POST','GET'])
    def check_adv():
        if request.method == "POST":
            try:
                results = None
                with mysql.connector.connect(**db_conn_info) as conn:
                    cursor = conn.cursor(buffered=True)
                    query = '''SELECT distinct position FROM checker.component_to_category;'''
                    cursor.execute(query)
                    conn.commit()
                    results = cursor.fetchall()
                    total_answer=[]
                    for r in results:
                        obtained = requests.post(r[0]+"/sentinel/read_containers", headers=request.headers).text
                        total_answer = total_answer + json.loads(obtained)
                    return total_answer
            except Exception:
                print("Something went wrong because of:",traceback.print_exc())
                return render_template("error_showing.html", r = traceback.print_exc()), 500
        else:
            log_to_db('asking_containers', "POST wasn't used in the request", request)
            return False

    @app.route("/get_container_categories", methods=['POST','GET'])
    def get_container_categories():
        try:
            with mysql.connector.connect(**db_conn_info) as conn:
                cursor = conn.cursor(buffered=True)
                query = '''SELECT * FROM checker.component_to_category;'''
                cursor.execute(query)
                conn.commit()
                results = cursor.fetchall()
                return results
        except Exception:
            print("Something went wrong because of:",traceback.print_exc())
            return render_template("error_showing.html", r = traceback.print_exc()), 500
    
    def get_extra_data():
        try:
            with mysql.connector.connect(**db_conn_info) as conn:
                cursor = conn.cursor(buffered=True)
                query = '''SELECT category, resource_address, resource_description, resource_information FROM checker.extra_resources join categories on categories.idcategories = extra_resources.id_category;'''
                cursor.execute(query)
                conn.commit()
                results = cursor.fetchall()
                return results
        except Exception:
            print("Something went wrong because of",traceback.print_exc())
            return "Error in get extra data!"
        
    @app.route("/run_test", methods=['POST','GET'])
    def run_test():
        if request.method == "POST":
            try:
                with mysql.connector.connect(**db_conn_info) as conn:
                    cursor = conn.cursor(buffered=True)
                    # to run malicious code, malicious code must be present in the db or the machine in the first place
                    query = '''select command, command_explained from tests_table where container_name =%s'''
                    cursor.execute(query, (request.form.to_dict()['container'],))
                    conn.commit()
                    results = cursor.fetchall()
                    total_result = ""
                    command_ran_explained = ""
                    for r in list(results):
                        command_ran = subprocess.run(r[0], shell=True, capture_output=True, text=True, encoding="cp437").stdout
                        command_ran_explained = subprocess.run(r[1], shell=True, capture_output=True, text=True, encoding="cp437").stdout + '\n'
                        total_result += "Running " + r[0] + " with result " + command_ran
                        query_1 = 'insert into tests_results (datetime, result, container, command) values (now(), %s, %s, %s);'
                        cursor.execute(query_1,(command_ran, request.form.to_dict()['container'],r[0],))
                        conn.commit()
                        log_to_db('test_ran', "Executing the is alive test on "+request.form.to_dict()['container']+" resulted in: "+command_ran, request)
                    return jsonify(total_result, command_ran_explained)
            except Exception:
                print("Something went wrong during tests running because of",traceback.print_exc())
                return render_template("error_showing.html", r = traceback.print_exc()), 500
        else:
            log_to_db('asking_containers', "POST wasn't used in the request", request)
            return "False"
        
    @app.route("/run_test_complex", methods=['POST','GET'])
    def run_test_complex():
        if request.method == "POST":
            try:
                with mysql.connector.connect(**db_conn_info) as conn:
                    cursor = conn.cursor(buffered=True)
                    # to run malicious code, malicious code must be present in the db or the machine in the first place
                    query = '''select command from complex_tests where name_of_test =%s'''
                    form_dict = request.form.to_dict()
                    test_name = form_dict.pop('test_name')
                    cursor.execute(query, (test_name,))
                    conn.commit()
                    results = cursor.fetchall()
                    total_result = ""
                    for r in list(results):
                        arguments_test = " "
                        for key, value in form_dict.items():
                            arguments_test+='-'+key+' "'+value+'" '
                        command_ran = subprocess.run(r[0]+arguments_test, shell=True, capture_output=True, text=True, encoding="cp437")
                        if len(command_ran.stderr) > 0:
                            string_used = '<p style="color:#FF0000";>'+command_ran.stderr+'</p> '+command_ran.stdout
                        else:
                            string_used = command_ran.stdout
                        total_result += string_used
                        query_1 = 'insert into tests_results (datetime, result, container, command) values (now(), %s, %s, %s);'
                        cursor.execute(query_1,(string_used, test_name,r[0],))
                        conn.commit()
                        log_to_db('test_ran', "Executing the complex test " + test_name + " resulted in: " +string_used, request)
                    return jsonify(total_result)
            except Exception:
                print("Something went wrong during tests running because of",traceback.print_exc())
                return render_template("error_showing.html", r = traceback.print_exc()), 500
        else:
            log_to_db('asking_containers', "POST wasn't used in the request", request)
            return "False"
        
    @app.route("/reboot/<container_id>", methods=['POST', 'GET'])
    def reboot(container_id):
        try:
            return render_template("reboot.html", container=container_id)
        except Exception:
            print("Something went wrong during rebooting because of:",traceback.print_exc())
            return render_template("error_showing.html", r = traceback.print_exc()), 500
        
        
    @app.route("/test_all_ports", methods=['GET'])
    def test_all_ports():
        result = {}
        with mysql.connector.connect(**db_conn_info) as conn:
            cursor = conn.cursor(buffered=True)
            # to run malicious code, malicious code must be present in the db or the machine in the first place
            query = '''select container_name, command from tests_table;'''
            cursor.execute(query)
            conn.commit()
            results = cursor.fetchall()
            for r in list(results):
                command_ran = subprocess.run(r[1], shell=True, capture_output=True, text=True, encoding="cp437").stdout
                result[r[0]]=command_ran
        return result
            
    @app.route("/deauthenticate", methods=['POST','GET'])
    def deauthenticate():
        return "You have been deauthenticated", 401
        
    @app.route("/reboot_container", methods=['POST','GET'])
    def reboot_container():
        if request.method == "POST":
            something = str(base64.b64decode(request.headers["Authorization"][len("Basic "):]))[:-1]
            psw = something[something.find(":")+1:]
            if psw == request.form.to_dict()['psw']:
                result = subprocess.run('docker restart '+request.form.to_dict()['id'], shell=True, capture_output=True, text=True, encoding="utf_8").stdout
                log_to_db('rebooting_containers', 'docker restart '+request.form.to_dict()['id']+' resulted in: '+result, request)
                return result
            else:
                return "Container not rebooted", 401
        else: 
            log_to_db('rebooting_containers', "POST wasn't used in the request", request)
            return "False"
            
    @app.route("/reboot_container_advanced/<container_id>", methods=['POST','GET'])
    def reboot_container_advanced(container_id):
        if request.method == "POST":
            try:
                with mysql.connector.connect(**db_conn_info) as conn:
                    something = str(base64.b64decode(request.headers["Authorization"][len("Basic "):]))[:-1]
                    psw = something[something.find(":")+1:]
                    cursor = conn.cursor(buffered=True)
                    # to run malicious code, malicious code must be present in the db or the machine in the first place
                    query = '''SELECT position FROM checker.component_to_category where component=%s;'''
                    cursor.execute(query, (container_id,))
                    conn.commit()
                    results = cursor.fetchall()
                    r = requests.post(results[0][0]+"/sentinel/reboot_container", headers=request.headers, data={"id": container_id, "psw": psw})
                    return r.text
            except Exception:
                print("Something went wrong during advanced container rebooting because of:",traceback.print_exc())
                return render_template("error_showing.html", r = traceback.print_exc()), 500
        else: 
            log_to_db('rebooting_containers', "POST wasn't used in the request", request)
            return "False"
        
    @app.route("/tests_results", methods=['POST','GET'])
    def get_tests():
        if request.method == "POST":
            try:
                with mysql.connector.connect(**db_conn_info) as conn:
                    cursor = conn.cursor(buffered=True)
                    query = '''WITH RankedEntries AS ( 
                        SELECT *, ROW_NUMBER() OVER (PARTITION BY container ORDER BY datetime DESC) AS row_num FROM tests_results
                        ) 
                        SELECT * FROM RankedEntries WHERE row_num = 1;'''
                    cursor.execute(query)
                    conn.commit()
                    log_to_db('getting_tests', 'Tests results were read', request)
                    results = cursor.fetchall()
                    return jsonify(results)
            except Exception:
                print("Something went wrong because of:",traceback.print_exc())
                return render_template("error_showing.html", r = traceback.print_exc()), 500
        else: 
            log_to_db('getting_tests', "POST wasn't used in the request", request)
            return "False"
        
    # this is only called serverside
    def log_to_db(table, log, request=None):
        if (request):
            user = base64.b64decode(request.headers["Authorization"][len('Basic '):]).decode('utf-8')
            user = user[:user.find(":")] 
        else:
            user = "Unidentified user"
        try:
            with mysql.connector.connect(**db_conn_info) as conn:
                cursor = conn.cursor(buffered=True)
                cursor.execute('''INSERT INTO `{}` (datetime, log, perpetrator) VALUES (NOW(),'{}','{}')'''.format(table, log.replace("'","''"), user))
                conn.commit()
        except Exception:
            print("Something went wrong during db logging because of:",traceback.print_exc(), "in",table)
            
    @app.route("/load_db",methods=['POST'])
    def load_db():
        trying_to_load_db_resulted_in = subprocess.run('mysql -u root --password=root -D checker < just_complex.sql', shell=True, capture_output=True, text=True, encoding="utf_8")
        out = trying_to_load_db_resulted_in.stdout
        err = trying_to_load_db_resulted_in.stderr
        if "mysql: [Warning] Using a password on the command line interface can be insecure" in err:
            err = ""
        else:
            err = '<p style="color:#FF0000";>'+err+'</p>'
        if len(err)==0 and len(out)==0:
            out = '<input type="button" name="db-success" id="db-success" value="Success! Click to reload" class="form-control" onclick="location.reload()"/>'
        return err+out
    
    
    @app.route("/get_complex_tests", methods=["GET"])
    def get_complex_tests():
        if request.method == "GET":
            try:
                with mysql.connector.connect(**db_conn_info) as conn:
                    cursor = conn.cursor(buffered=True)
                    query = '''WITH RankedEntries AS ( 
                        SELECT *, ROW_NUMBER() OVER (PARTITION BY container ORDER BY datetime DESC) AS row_num FROM tests_results
                        ) 
                        SELECT * FROM RankedEntries WHERE row_num = 1;'''
                    cursor.execute(query)
                    conn.commit()
                    log_to_db('getting_tests', 'Tests results were read', request)
                    results = cursor.fetchall()
                    return jsonify(results)
            except Exception:
                print("Something went wrong because of:",traceback.print_exc())
                return render_template("error_showing.html", r = traceback.print_exc()), 500
        else: 
            log_to_db('getting_tests', "POST wasn't used in the request", request)
            return "False"
    
    @app.route("/container/<container_id>")
    def get_container_logs(container_id):
        r = '<br>'.join(subprocess.run('docker logs '+container_id+" --tail 1000", shell=True, capture_output=True, text=True, encoding="utf_8").stdout.split('\n'))
        container_name = subprocess.run('docker ps -a -f id='+container_id+' --format "{{.Names}}"', shell=True, capture_output=True, text=True, encoding="utf_8").stdout.split('\n')[0]
        return render_template('log_show.html', container_id = container_id, r = r, container_name=container_name)
    
    @app.route("/get_summary_status")
    def get_summary_status():
        try:
            with mysql.connector.connect(**db_conn_info) as conn:
                cursor = conn.cursor(buffered=True)
                cursor.execute('''SELECT * FROM summary_status;''')
                results = cursor.fetchall()
                return jsonify(results)
        except Exception:
            print("Something went wrong during db logging because of:",traceback.print_exc())
            return "Problems when obtaining summary statuses due to: "+ traceback.print_exc(), 500
    
    def get_container_data(do_not_jsonify=False):
        containers_ps = [a for a in (subprocess.run('docker ps --format json -a', shell=True, capture_output=True, text=True, encoding="utf_8").stdout).split('\n')][:-1]
        containers_stats = [b for b in (subprocess.run('docker stats --format json -a --no-stream', shell=True, capture_output=True, text=True, encoding="utf_8").stdout).split('\n')][:-1]
        containers_merged = []
        for container_stats in containers_stats:
            for container_ps in containers_ps:
                for key1, value1 in json.loads(container_stats).items():
                    for key2, value2 in json.loads(container_ps).items():
                        if key1 == "Name" and key2 == "Names":
                            if value1 == value2:
                                containers_merged.append({**json.loads(container_ps), **json.loads(container_stats)})
        if do_not_jsonify:
            return containers_merged
        return jsonify(containers_merged)
    
    @app.route('/generate_pdf', methods=['POST'])
    def generate_pdf():
        data_stored = []
        for container_data in get_container_data(True):
            r = '<br>'.join(subprocess.run('docker logs '+container_data['ID'] + ' --tail 500', shell=True, capture_output=True, text=True, encoding="utf_8").stdout.split('\n'))
            data_stored.append({"header": container_data['Name'], "string": r})
        
        # Create a PDF document
        pdf_output_path = "logs.pdf"
        doc = SimpleDocTemplate(pdf_output_path, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        # Initialize list to store content
        content = []
        extra_logs = []
        tests_out = None
        extra_tests = []
        
        try:
            with mysql.connector.connect(**db_conn_info) as conn:
                cursor = conn.cursor(buffered=True)
                query = '''WITH RankedEntries AS ( 
                    SELECT *, ROW_NUMBER() OVER (PARTITION BY container ORDER BY datetime DESC) AS row_num FROM tests_results
                    ) 
                    SELECT * FROM RankedEntries WHERE row_num = 1;'''
                cursor.execute(query)
                conn.commit()
                log_to_db('getting_tests', 'Tests results were read', request)
                results = cursor.fetchall()
                tests_out = results
        except Exception:
            print("Something went wrong because of:",traceback.print_exc())
            return render_template("error_showing.html",r="Couldn't generate report due to: "+traceback.print_exc()), 500
        # index
        content.append(Paragraph("The following are hyperlinks to logs of each container.", styles["Heading1"]))
        for pair in data_stored:
            if pair["header"] in ['dashboard-backend','myldap']:
                continue
            content.append(Paragraph(f'<a href="#{pair["header"]}" color="blue">{pair["header"]}</a>', styles["Normal"]))
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for root, dirs, files in os.walk(os.path.join(current_dir, os.pardir)):
            if 'log.txt' in files:
                logs_file_path = os.path.join(root, 'log.txt')
                with open(logs_file_path, 'r') as file:
                    content.append(Paragraph('<a href="#iot-directory-log" color="blue">iot-directory-log</a>', styles["Normal"]))
                    extra_logs.append(Paragraph(f'<b><a name=iot-directory-log></a>iot-directory-log</b>', styles["Heading1"]))
                    extra_logs.append(Paragraph(file.read(), styles["Normal"]))
                break  # Stop searching after finding the first occurrence
        for test in tests_out:
            if not test:
                break
            content.append(Paragraph(f'<a href="#{test[3]}" color="blue">{test[3]}</a>', styles["Normal"]))
            extra_tests.append(test)
        content.append(PageBreak())
        
        
        # Iterate over pairs
        for pair in data_stored:
            if pair["header"] in ['dashboard-backend','myldap']:
                continue
            header = pair["header"]
            string = pair["string"]
            strings = string.split("<br>")
            # Add header to content
            content.append(Paragraph(f'<b><a name={header}></a>{header}</b>', styles["Heading1"]))
            # Add normal string if it exists
            for substring in strings:
                content.append(Paragraph(substring, styles["Normal"]))
            content.append(PageBreak())
        for extra in extra_logs:
            content.append(extra)
        content.append(PageBreak())
        for test in extra_tests:
            content.append(Paragraph(f'<b><a name="{test[3]}"></a>{test[3]}</b>', styles["Heading1"]))
            content.append(Paragraph(test[2], styles["Normal"]))
        # Add content to the PDF document
        doc.build(content)
        # Send the PDF file as a response
        response = send_file(pdf_output_path)
        return response
    
    def find_target_folder(parent_folder):
        for root, dirs, files in os.walk(parent_folder):
            if "docker-compose.yml" in files and "setup.sh" in files:
                return root
        return None
    
    @app.route('/clear_certifications', methods=['GET'])
    def clear_certifications():
        user = ""
        try:
            user = base64.b64decode(request.headers["Authorization"][len('Basic '):]).decode('utf-8')
            user = user[:user.find(":")]
        except Exception:
            return render_template("error_showing.html", r = "Issues during the establishing of the user: "+ traceback.print_exc()), 500
        if user != "admin":
            return render_template("error_showing.html", r = "User is not authorized to perform the operation."), 401
        script_folder = os.path.dirname(os.path.abspath(__file__))
        parent_folder = os.path.dirname(script_folder)
        
        # Find the target folder
        target_folder = find_target_folder(parent_folder)
        if target_folder:
            # Define the output zip file path and password
            subprocess.run(f'cd {target_folder}; rm -f *snap4city-certification-*.zip', shell=True, capture_output=True, text=True, encoding="utf_8")
            return "Done"
        
    
    @app.route('/certification', methods=['GET'])
    def certification():
        user = ""
        try:
            user = base64.b64decode(request.headers["Authorization"][len('Basic '):]).decode('utf-8')
            user = user[:user.find(":")]
        except Exception:
            return render_template("error_showing.html", r = "Issues during the establishing of the user: "+ traceback.print_exc()), 500
        if user != "admin":
            return render_template("error_showing.html", r = "User is not authorized to perform the operation."), 401
        script_folder = os.path.dirname(os.path.abspath(__file__))
        parent_folder = os.path.dirname(script_folder)
        
        # Find the target folder
        target_folder = find_target_folder(parent_folder)
        
        if target_folder:
            # Define the output zip file path and password
            password = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(16))
            make_certification = subprocess.run(f'cd {target_folder}; bash make_dumps_of_database.sh; zip -r -P {password} snap4city-certification-{password}.zip iotapp-00*/flows.json d*conf iot-directory-conf m*conf n*conf ownership-conf/config.php nifi/conf servicemap-conf/servicemap.properties ../placeholder_used.txt *dump.* servicemap-iot-conf/iotdeviceapi.dtd servicemap-superservicemap-conf/settings.xml synoptics-conf/ mongo_dump virtuoso_dump ../checker/*', shell=True, capture_output=True, text=True, encoding="utf_8")
            if len(make_certification.stderr) > 0:
                return send_file(target_folder + f'/snap4city-certification-{password}.zip')
                # bypass this shit, for now
                return render_template("error_showing.html", r = "There were issues: "+ make_certification.stderr), 500
            else:
                return send_file(target_folder + f'/snap4city-certification-{password}.zip')
        else:
            return render_template("error_showing.html", r = "Couldn't find the snap4city installation."), 500
            
    @app.route('/clustered_certification', methods=['GET'])
    def clustered_certification():
        user = ""
        try:
            user = base64.b64decode(request.headers["Authorization"][len('Basic '):]).decode('utf-8')
            user = user[:user.find(":")]
        except Exception:
            return render_template("error_showing.html", r = "Issues during the establishing of the user: "+ traceback.print_exc()), 500
        if user != "admin":
            return render_template("error_showing.html", r = "User is not authorized to perform the operation."), 401
        try:
            results = None
            with mysql.connector.connect(**db_conn_info) as conn:
                cursor = conn.cursor(buffered=True)
                query = '''SELECT distinct position FROM checker.component_to_category;'''
                cursor.execute(query)
                conn.commit()
                results = cursor.fetchall()
                error = False
                errorText = ""
                #pick folder
                now = datetime.now()
                folder_name = now.strftime("%Y-%m-%d_%H-%M-%S")
                os.makedirs(folder_name)
                for r in results:
                    file_name, content_disposition = "", ""
                    obtained = requests.get(r[0]+"/sentinel/certification", headers=request.headers)
                    if 'Content-Disposition' in obtained.headers:
                        content_disposition = obtained.headers['Content-Disposition']
                    if 'filename=' in content_disposition:
                        file_name = content_disposition.split('filename=')[1].strip('"')
                    if len(file_name) < 1:
                        errorText += "Unable to recover password from sentinel located at " + r[0] + "\n"
                        error = True
                    if obtained.status_code == 200 and len(file_name) > 1:
                        with open(folder_name+'/'+urlparse(r[0]).hostaname + ' - ' +file_name, "wb+") as file:
                            if not error:
                                file.write(obtained.content)
                    else:
                        error = True
                        errorText += "Couldn't read file from sentinel located at " + r[0] + " because of error in request: "+ str(obtained.status_code) + '\n'
                if error:
                    return render_template("error_showing.html", r = errorText.replace("\n","<br>")), 500
                else:
                    password = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(16))
                    subprocess.run(f'cd {folder_name}; rar a snap4city-certification-composite-{password}.rar -p"{password}" snap4city-certification-*.rar -k', shell=True, capture_output=True, text=True, encoding="utf_8")
                    return send_file(f'snap4city-certification-composite-{password}.rar')
        except Exception:
            print("Something went wrong during clustered certification due to:",traceback.print_exc())
            return render_template("error_showing.html", r = traceback.format_exc()), 500
    return app
    
if __name__ == "__main__":
    create_app().run(host='localhost', port=4080)
