import csv
input_file = 'd:\\Proyectos\\Olan\\RedDragon\\data\\control_cambiosv2.csv'
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if '10012497' in row[0]:
            print(f"Row {i}: {row}")
