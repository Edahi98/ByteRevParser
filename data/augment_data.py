import csv
import random
import re

def replace_synonyms(text):
    synonyms = {
        r'\bagrega\b': ['añade', 'adiciona', 'integra', 'suma'],
        r'\bagregan\b': ['añaden', 'adicionan', 'integran', 'suman'],
        r'\badiciona\b': ['agrega', 'añade', 'integra'],
        r'\badicionan\b': ['agregan', 'añaden', 'integran'],
        r'\bañade\b': ['agrega', 'adiciona', 'incorpora'],
        r'\bañaden\b': ['agregan', 'adicionan', 'incorporan'],
        r'\bcambia\b': ['modifica', 'actualiza', 'corrige', 'ajusta'],
        r'\bcambian\b': ['modifican', 'actualizan', 'corrigen', 'ajustan'],
        r'\bmodifica\b': ['cambia', 'actualiza', 'corrige', 'ajusta'],
        r'\bmodifican\b': ['cambian', 'actualizan', 'corrigen', 'ajustan'],
        r'\belimina\b': ['borra', 'quita', 'retira', 'suprime'],
        r'\beliminan\b': ['borran', 'quitan', 'retiran', 'suprimen'],
        r'\bactualiza\b': ['modifica', 'renueva', 'pone al día'],
        r'\bactualizan\b': ['modifican', 'renuevan'],
        r'\bcorrige\b': ['enmienda', 'arregla', 'modifica'],
        r'\bartes\b': ['diseños', 'imágenes', 'gráficos'],
        r'\barte\b': ['diseño', 'imagen', 'gráfico'],
        r'\bformato\b': ['documento', 'plantilla', 'archivo'],
        r'\bprocedimiento\b': ['proceso', 'instructivo', 'método']
    }
    for pattern, replacements in synonyms.items():
        if random.random() < 0.5:
            # Function to match case
            def replace_match(match):
                word = match.group(0)
                rep = random.choice(replacements)
                if word.istitle(): return rep.capitalize()
                if word.isupper(): return rep.upper()
                return rep
            text = re.sub(pattern, replace_match, text, flags=re.IGNORECASE)
    return text

def add_typos(text):
    if len(text) < 10: return text
    chars = list(text)
    num_typos = random.randint(1, max(1, len(text)//25))
    for _ in range(num_typos):
        idx = random.randint(0, len(chars)-1)
        if chars[idx].isalpha():
            keyboard = 'qwertyuiopasdfghjklzxcvbnm'
            chars[idx] = random.choice(keyboard)
    return "".join(chars)

def add_fillers(text):
    fillers = ["eh, ", "o sea, ", "este... ", "bueno, ", "pues ", "a ver, "]
    if random.random() < 0.4:
        return random.choice(fillers) + text
    else:
        words = text.split()
        if len(words) > 4:
            insert_idx = random.randint(1, len(words)-1)
            words.insert(insert_idx, random.choice([f.strip(',. ') for f in fillers]))
            return " ".join(words)
    return text

def alter_casing_punct(text):
    if random.random() < 0.3:
        text = text.lower()
    if random.random() < 0.4:
        text = text.replace('.', '').replace(',', '')
    return text

def augment(text):
    strategies = [replace_synonyms, add_typos, add_fillers, alter_casing_punct]
    random.shuffle(strategies)
    
    num_strategies = random.randint(1, 3)
    for i in range(num_strategies):
        text = strategies[i](text)
    return text

def main():
    input_file = 'd:\\Proyectos\\Olan\\RedDragon\\data\\control_cambiosv2.csv'
    output_file = 'd:\\Proyectos\\Olan\\RedDragon\\data\\control_cambiosv2 copy.csv'
    
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = list(csv.reader(f))
        
    header = reader[0]
    data = reader[1:]
    
    output_data = data.copy()
    
    needed = 1000 - len(output_data) - 1 # -1 for header
    print(f"Generating {needed} augmented records...")
    
    for _ in range(needed):
        original_row = random.choice(data)
        if len(original_row) < 2: continue
        frase, etiqueta = original_row[0], original_row[1]
        
        aug_frase = augment(frase)
        output_data.append([aug_frase, etiqueta])
        
    random.shuffle(output_data)
    
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in output_data[:999]:
            writer.writerow(row)
            
    print(f"Done! Saved exactly 1000 rows to {output_file}")

if __name__ == '__main__':
    main()
