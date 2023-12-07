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

import json

def parse_mysql_dump(dump_file_path):
    schema = {}
    current_table = None

    with open(dump_file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            
            if line.startswith('CREATE TABLE'):
                table_name = line.split('`')[1]
                current_table = table_name
                schema[current_table] = []
            
            elif line.startswith('  `'):
                if current_table:
                    parts = line.split('`')
                    column_name = parts[1]
                    column_type = parts[2].split()[0]
                    schema[current_table].append({'Field': column_name, 'Type': column_type})

    return schema
# replace 'dump_file.sql' with your MySQL dump file path
dump_file_path = 'out.sql'

result = parse_mysql_dump(dump_file_path)
print(json.dumps(result, indent=2))
