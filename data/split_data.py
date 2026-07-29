import csv
import re

input_file = 'd:\\Proyectos\\Olan\\RedDragon\\data\\control_cambiosv2.csv'

new_rows = []

with open(input_file, mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if len(row) < 2:
            continue
        frase, etiqueta = row[0], row[1]
        
        if '\n' in frase:
            lines = frase.split('\n')
            for line in lines:
                line = line.strip()
                # Remove leading numbers, dashes, asterisks
                line = re.sub(r'^[\d\.\-\*\s]+', '', line)
                if len(line.split()) > 2:
                    new_rows.append([line, etiqueta])

with open(input_file, mode='a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for new_row in new_rows:
        writer.writerow(new_row)

print(f'Added {len(new_rows)} separated lines.')
