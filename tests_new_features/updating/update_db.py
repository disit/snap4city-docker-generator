import mysql.connector
import os


def apply_updates(starts_as_old, connection):
    print('starts as',str(starts_as_old))
    while starts_as_old < 4:
        print('applying',str(starts_as_old))
        for dname, dirs, files in os.walk('update-'+str(starts_as_old)):
            print(files)
            for file in files:
                if ".sql" == file[-4:]:
                    try:
                        with open(os.path.join(dname,file), 'r', encoding='utf-8') as fopen:
                            print('appling',os.path.join(dname,file),'\n')
                            commands = fopen.read().split(';')
                            commands = [command for command in commands if command[0:2]!='--']
                            for command in commands:
                                try:
                                    cursor = connection.cursor(dictionary=True, buffered=True)
                                    cursor.execute(command)
                                    #print(command)
                                except Exception as E:
                                    if "1064" in str(E):
                                        continue # syntax error due to lazy filtering, not a real error
                                    print("command:",command,"failed due to",E)
                    except UnicodeDecodeError as E:
                        print(E)
        starts_as_old = starts_as_old +1

def check_column_existence(host, username, password, database, table_name1, column_name1, table_name2, column_name2, table_name3, column_name3):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )

        cursor = connection.cursor(dictionary=True, buffered=True)

        # Check if the column exists in the table
        cursor.execute(f"SHOW COLUMNS FROM {table_name1} LIKE '{column_name1}'")
        result = cursor.fetchone()

        if result:
            print("Not the first one")
        else:
            apply_updates(1, connection)
            return
            
        cursor.execute(f"SHOW COLUMNS FROM {table_name2} LIKE '{column_name2}'")
        result = cursor.fetchone()

        if result:
            print("Not the second one")
        else:
            apply_updates(2, connection)
            return
            
        cursor.execute(f"SHOW COLUMNS FROM {table_name3} LIKE '{column_name3}'")
        result = cursor.fetchone()

        if result:
            print("Up to date")
        else:
            apply_updates(3, connection)
            return

        connection.close()
    except mysql.connector.Error as error:
        print("Error:", error)


# edit according to your dashboarddb configuration
host = 'localhost'
username = 'user-root'
password = 'changeme'
database = 'Dashboard'

result = check_column_existence(host, username, password, database, "SynopticTemplates", "singleReadVariable", "DashboardWizard", "value_name", "Config_dashboard", "theme")

