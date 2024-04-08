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
import mysql.connector
import json
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet



# edit this block according to your mysql server's configuration
db_conn_info = {
        "user": "root",
        "passwd": "root",
        "host": "localhost",
        "port": 3306,
        "database": "checker",
        "auth_plugin": 'mysql_native_password'
    }
def create_app():
    app = Flask(__name__)
    app.secret_key = b'\x8a\x17\x93kT\xc0\x0b6;\x93\xfdp\x8bLl\xe6u\xa9\xf5x'
    @app.route("/")
    def main_page():
        try:
            with mysql.connector.connect(**db_conn_info) as conn:
                cursor = conn.cursor(buffered=True)
                # to run malicious code, malicious code must be present in the db or the machine in the first place
                query = '''SELECT *,GetHighContrastColor(button_color) AS high_contrast_color FROM checker.complex_tests;'''
                cursor.execute(query)
                conn.commit()
                results = cursor.fetchall()
                
                return render_template("checker.html",extra=results)
        except Exception as e:
            print("Something went wrong because of",e)
            return render_template("error_showing.html", r = e)
        


    @app.route("/read_containers", methods=['POST','GET'])
    def check():
        if request.method == "POST":
            containers = get_container_data()
            #containers = subprocess.run('docker ps --format json -a', shell=True, capture_output=True, text=True, encoding="utf_8").stdout
            #log_to_db('asking_containers', 'docker ps --format json -a resulted in: '+containers)
            return containers
        else:
            log_to_db('asking_containers', "POST wasn't used in the request")
            return False
        
    @app.route("/run_test", methods=['POST','GET'])
    def run_test():
        if request.method == "POST":
            try:
                with mysql.connector.connect(**db_conn_info) as conn:
                    cursor = conn.cursor(buffered=True)
                    # to run malicious code, malicious code must be present in the db or the machine in the first place
                    query = '''select command from tests_table where container_name =%s'''
                    cursor.execute(query, (request.form.to_dict()['container'],))
                    conn.commit()
                    results = cursor.fetchall()
                    total_result = ""
                    for r in list(results):
                        command_ran = subprocess.run(r[0], shell=True, capture_output=True, text=True, encoding="cp437").stdout
                        
                        total_result += command_ran
                        query_1 = 'insert into tests_results (datetime, result, container, command) values (now(), %s, %s, %s);'
                        cursor.execute(query_1,(command_ran, request.form.to_dict()['container'],r[0],))
                        
                        conn.commit()
                        
                        log_to_db('test_ran', "result was "+command_ran)
                    return jsonify(results)
            except Exception as e:
                print("Something went wrong during tests running because of",e)
                return render_template("error_showing.html", r = e)
        else:
            log_to_db('asking_containers', "POST wasn't used in the request")
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
                        
                        log_to_db('test_ran', "result was "+string_used)
                    return jsonify(total_result)
            except Exception as e:
                print("Something went wrong during tests running because of",e)
                return render_template("error_showing.html", r = e)
        else:
            log_to_db('asking_containers', "POST wasn't used in the request")
            return "False"
        
    @app.route("/reboot_container", methods=['POST','GET'])
    def reboot_container():
        if request.method == "POST":
            result = subprocess.run('docker restart '+request.form.to_dict()['id'], shell=True, capture_output=True, text=True, encoding="utf_8").stdout
            # insert way to make result clearer here
            log_to_db('rebooting_containers', 'docker restart '+request.form.to_dict()['id']+' resulted in: '+result)
            return result
        else: 
            log_to_db('rebooting_containers', "POST wasn't used in the request")
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
                    log_to_db('getting_tests', 'Tests results were read')
                    results = cursor.fetchall()
                    
                    return jsonify(results)
            except Exception as e:
                print("Something went wrong because of",e)
                return render_template("error_showing.html", r = e)
        else: 
            log_to_db('getting_tests', "POST wasn't used in the request")
            return "False"
        
    # this is only called serverside
    def log_to_db(table, log):
        try:
            with mysql.connector.connect(**db_conn_info) as conn:
                cursor = conn.cursor(buffered=True)
                cursor.execute('''INSERT INTO `{}` (date, log) VALUES (NOW(),'{}')'''.format(table, log.replace("'","''")))
                conn.commit()
        except Exception as e:
            print("Something went wrong during db logging because of",e)
            
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
    
    @app.route("/container/<container_id>")
    def get_container_logs(container_id):
        r = '<br>'.join(subprocess.run('docker logs '+container_id, shell=True, capture_output=True, text=True, encoding="utf_8").stdout.split('\n'))
        container_name = subprocess.run('docker ps -a -f id='+container_id+' --format "{{.Names}}"', shell=True, capture_output=True, text=True, encoding="utf_8").stdout.split('\n')[0]
        return render_template('log_show.html', container_id = container_id, r = r, container_name=container_name)
    
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

        # index
        content.append(Paragraph("The following are hyperlinks to logs of each container.", styles["Heading1"]))
        for pair in data_stored:
            content.append(Paragraph(f'<a href="#{pair["header"]}" color="blue">{pair["header"]}</a>', styles["Normal"]))
            
        content.append(PageBreak())
        # Iterate over pairs
        for pair in data_stored:
            header = pair["header"]
            string = pair["string"]
            strings = string.split("<br>")

            # Add header to content
            content.append(Paragraph(f'<b><a name={header}></a>{header}</b>', styles["Heading1"]))

            # Add normal string if it exists
            for substring in strings:
                content.append(Paragraph(substring, styles["Normal"]))
            content.append(PageBreak())

        # Add content to the PDF document
        doc.build(content)

        # Send the PDF file as a response
        response = send_file(pdf_output_path)

        return response
    
    
    
    return app
    

if __name__ == "__main__":
    create_app().run(host='localhost', port=4080)