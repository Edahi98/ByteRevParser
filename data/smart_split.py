import csv
import re

input_file = 'd:\\Proyectos\\Olan\\RedDragon\\data\\control_cambiosv2.csv'

new_rows = []

def classify(line, parent_label):
    line_lower = line.lower()
    
    # Priority classification based on keywords
    if any(k in line_lower for k in ['elimina', 'eliminacion', 'eliminación', 'borra', 'retira', 'suprime', 'elimna']):
        return 'Eliminación'
    elif any(k in line_lower for k in ['agrega', 'adiciona', 'adición', 'adicion', 'añade', 'integra', 'entradas']):
        return 'Adición'
    elif any(k in line_lower for k in ['emite', 'emisión', 'emision', 'crea', 'creación', 'creacion', 'inicial']):
        return 'Emisión'
    elif any(k in line_lower for k in ['cambia', 'modifica', 'actualiza', 'corrige', 'cambio', 're-paginación', 're-paginacion', 'generaliza']):
        return 'Cambio'
        
    # If no explicit keyword is found but it says something like "Se colocan flechas", "Materiales se especifica", default to Cambio
    if any(k in line_lower for k in ['se especifica', 'se amplia', 'se colocan']):
        return 'Cambio'
        
    return parent_label

with open(input_file, mode='r', encoding='utf-8') as f:
    reader = list(csv.reader(f))
    
for row in reader[1:]:
    if len(row) < 2:
        continue
    frase, etiqueta = row[0], row[1]
    
    if '\n' in frase:
        lines = frase.split('\n')
        for line in lines:
            line = line.strip()
            # Remove leading numbers, dashes, asterisks
            line = re.sub(r'^[\d\.\-\*\s]+', '', line)
            
            # Skip lines that are just context like "6 (HOJA: 1,12)" or "# DE ARTES (HOJA)"
            if re.match(r'^[\d\s]+\(hoja.*', line.lower()) or line.lower().startswith('# de artes') or line.lower().startswith('total de artes'):
                continue
                
            if len(line.split()) > 2:
                new_label = classify(line, etiqueta)
                new_rows.append([line, new_label])

with open(input_file, mode='a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for new_row in new_rows:
        writer.writerow(new_row)

print(f'Added {len(new_rows)} SMART separated lines.')
