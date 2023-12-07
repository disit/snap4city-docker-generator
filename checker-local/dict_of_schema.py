import json

def parse_mysql_dump(dump_file_path):
    schema = {}
    current_table = None

    with open(dump_file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            #line = line.strip()

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

dump_file_path = 'out.sql'

result = parse_mysql_dump(dump_file_path)
print(json.dumps(result, indent=2))
