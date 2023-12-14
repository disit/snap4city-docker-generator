import subprocess

# edit according to your dashboarddb configuration
host = "localhost"
user = "root"
password = "changeme"

command = f"mysql −h{host} −u{user} −p{password} Dashboard < backup-1.sql"
print(subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf_8").stdout)
print('\n')
command_1 = f"mysql −h{host} −u{user} −p{password} iotdb < backup-2.sql"
print(subprocess.run(command_1, shell=True, capture_output=True, text=True, encoding="utf_8").stdout)
print('\n')