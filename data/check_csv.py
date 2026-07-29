import csv
input_file = 'd:\\Proyectos\\Olan\\RedDragon\\data\\control_cambiosv2.csv'
with open(input_file, 'r', encoding='utf-8') as f:
    reader = list(csv.reader(f))
    print(f"Total CSV rows: {len(reader)}")
    for row in reader:
        if '150' in row[0]:
            print(f"Found 150 in row: {row}")
