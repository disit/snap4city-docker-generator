# -*- coding: utf-8 -*-
import subprocess

# edit according to your dashboarddb configuration
host = "localhost"
user = "root"
password = "changeme"

command = f"mysqldump −h{host} −u{user} −p{password} Dashboard Widgets WidgetsIconsMap multilanguage HeatmapRanges HeatmapColorLevels MainMenu MainMenuSubmenus > backup-1.sql"
print(subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf_8").stdout)
print('\n')
command_1 = f"mysqldump −h{host} −u{user} −p{password} iotdb functionalities mainmenu defaultpolicy formats protocols data_types defaultcontestbrokerpolicy > backup-1.sql"
print(subprocess.run(command_1, shell=True, capture_output=True, text=True, encoding="utf_8").stdout)
print('\n')