import polars as pl
import nlpaug.augmenter.char as nac
import random
import re

def inject_special_chars(text):
    if len(text) < 5: return text
    chars = list(text)
    num_inject = random.randint(1, 6)
    special_chars = ['#', '@', '%', '&', '*', '$', '!', '?', '|', '~', '_', '-']
    for _ in range(num_inject):
        idx = random.randint(0, len(chars) - 1)
        if chars[idx] != ' ':
            action = random.choice(['prepend', 'replace', 'append'])
            s_char = random.choice(special_chars)
            if action == 'prepend':
                chars[idx] = s_char + chars[idx]
            elif action == 'append':
                chars[idx] = chars[idx] + s_char
            else:
                chars[idx] = s_char
    return "".join(chars)

def replace_synonyms(text):
    synonyms = {
        r'\bagrega\b': ['añade', 'adiciona', 'integra', 'suma', 'anexa', 'pega'],
        r'\bcambia\b': ['modifica', 'actualiza', 'corrige', 'ajusta', 'altera', 'remplaza'],
        r'\belimina\b': ['borra', 'quita', 'retira', 'suprime', 'deshace', 'cancela'],
        r'\bartes\b': ['diseños', 'imágenes', 'gráficos', 'esquemas', 'planos'],
        r'\bformato\b': ['documento', 'plantilla', 'archivo', 'registro'],
        r'\bprocedimiento\b': ['proceso', 'instructivo', 'método', 'paso a paso']
    }
    for pattern, replacements in synonyms.items():
        if random.random() < 0.7:
            def replace_match(match):
                word = match.group(0)
                rep = random.choice(replacements)
                if word.istitle(): return rep.capitalize()
                if word.isupper(): return rep.upper()
                return rep
            text = re.sub(pattern, replace_match, text, flags=re.IGNORECASE)
    return text

def main():
    input_file = r'd:\Proyectos\Olan\RedDragon\data\control_cambiosv2 copy.csv'
    output_file = r'd:\Proyectos\Olan\RedDragon\data\generador_nlp\dataset_10000.csv'
    
    print("Cargando dataset original con Polars...")
    df = pl.read_csv(input_file, infer_schema_length=0, truncate_ragged_lines=True, quote_char='"')
    
    target_count = 10000
    needed = target_count
    
    print(f"Generando {needed} filas sintéticas con longitudes ultra-variables...")
    
    keyboard_aug = nac.KeyboardAug(aug_char_p=0.3, aug_word_p=0.4, include_special_char=True)
    random_aug = nac.RandomCharAug(action="insert", aug_char_p=0.3, aug_word_p=0.4, spec_char='!@#$%^&*()_+')
    swap_aug = nac.RandomCharAug(action="swap", aug_char_p=0.2, aug_word_p=0.3)
    
    augmented_rows = []
    df = df.drop_nulls()
    valid_rows = [r for r in df.to_dicts() if 'frase' in r and 'etiqueta' in r and r['frase'] is not None and r['etiqueta'] is not None]
    
    for i in range(needed):
        if i % 1000 == 0 and i > 0:
            print(f"Progreso: {i} / {needed} generados...")
            
        row = random.choice(valid_rows)
        text = str(row['frase'])
        etiqueta = str(row['etiqueta'])
        
        # 1. Sinónimos primero
        text = replace_synonyms(text)
        
        # 2. LONGITUD ULTRA-VARIABLE (Afecta al 90% de los registros)
        if random.random() < 0.9:
            words = text.split()
            if len(words) > 2:
                # Escoger una longitud al azar entre 1 palabra y el total de palabras
                target_len = random.randint(1, len(words))
                if target_len < len(words):
                    # Tomar un pedazo al azar de esa longitud exacta
                    start = random.randint(0, len(words) - target_len)
                    text = " ".join(words[start:start+target_len])
            
        # 3. MEZCLA AGRESIVA DE RUIDO
        try:
            if random.random() < 0.5:
                text = keyboard_aug.augment(text)[0]
            if random.random() < 0.4:
                text = swap_aug.augment(text)[0]
            if random.random() < 0.4:
                text = random_aug.augment(text)[0]
            
            if random.random() < 0.8:
                text = inject_special_chars(text)
                
            if random.random() < 0.25:
                text = text.upper()
            elif random.random() < 0.25:
                text = text.lower()
                
            if random.random() < 0.3:
                words = text.split()
                if len(words) > 2:
                    idx = random.randint(0, len(words)-2)
                    words[idx] = words[idx] + words[idx+1]
                    del words[idx+1]
                    text = " ".join(words)
                    
        except Exception:
            text = inject_special_chars(text)
            
        augmented_rows.append({'frase': text, 'etiqueta': etiqueta})
        
    print("Sobreescribiendo el dataset final con longitudes variables...")
    df_final = pl.DataFrame(augmented_rows)
    df_final = df_final.sample(fraction=1.0, shuffle=True)
    
    df_final.write_csv(output_file)
    print("!Completado exitosamente!")

if __name__ == '__main__':
    main()
