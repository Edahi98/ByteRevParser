import polars as pl
import nlpaug.augmenter.char as nac
import random
import re

def inject_phonetic_errors(text):
    words = text.split()
    new_words = []
    
    for word in words:
        if random.random() < 0.4: 
            word_str = word.lower()
            
            if 'v' in word_str and random.random() < 0.5: word_str = word_str.replace('v', 'b', 1)
            elif 'b' in word_str and random.random() < 0.5: word_str = word_str.replace('b', 'v', 1)
            
            elif 'ce' in word_str and random.random() < 0.5: word_str = word_str.replace('ce', 'se', 1)
            elif 'ci' in word_str and random.random() < 0.5: word_str = word_str.replace('ci', 'si', 1)
            elif 'se' in word_str and random.random() < 0.5: word_str = word_str.replace('se', 'ce', 1)
            elif 'si' in word_str and random.random() < 0.5: word_str = word_str.replace('si', 'ci', 1)
            
            elif 'z' in word_str and random.random() < 0.5: word_str = word_str.replace('z', 's', 1)
            elif 's' in word_str and random.random() < 0.5: word_str = word_str.replace('s', 'z', 1)
            
            elif 'll' in word_str and random.random() < 0.5: word_str = word_str.replace('ll', 'y', 1)
            elif 'y' in word_str and random.random() < 0.5: word_str = word_str.replace('y', 'll', 1)
            
            elif 'ge' in word_str and random.random() < 0.5: word_str = word_str.replace('ge', 'je', 1)
            elif 'gi' in word_str and random.random() < 0.5: word_str = word_str.replace('gi', 'ji', 1)
            elif 'je' in word_str and random.random() < 0.5: word_str = word_str.replace('je', 'ge', 1)
            elif 'ji' in word_str and random.random() < 0.5: word_str = word_str.replace('ji', 'gi', 1)
            
            elif 'qu' in word_str and random.random() < 0.5: word_str = word_str.replace('qu', 'k', 1)
            elif 'k' in word_str and random.random() < 0.5: word_str = word_str.replace('k', 'qu', 1)
            
            elif word_str.startswith('h') and random.random() < 0.5: word_str = word_str[1:]
            elif not word_str.startswith('h') and word_str[0:1].isalpha() and random.random() < 0.2: word_str = 'h' + word_str
            
            if word.istitle():
                word_str = word_str.capitalize()
            elif word.isupper():
                word_str = word_str.upper()
                
            new_words.append(word_str)
        else:
            new_words.append(word)
            
    return " ".join(new_words)

def inject_special_chars(text):
    if len(text) < 5: return text
    chars = list(text)
    num_inject = random.randint(1, 4) # Reduced aggressiveness
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
    
    print(f"Generando {needed} filas con balance de ruido y limpieza...")
    
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
        
        # 1. Sinónimos primero (mantiene la frase comprensible)
        text = replace_synonyms(text)
        
        # REGLA CLAVE: 25% de las oraciones se salvan de TODO ruido y corte.
        # Esto asegura que haya frases completamente claras en el dataset.
        if random.random() < 0.25:
            augmented_rows.append({'frase': text})
            continue
            
        # Para el 75% restante, se baja drásticamente la probabilidad de cada ruido
        # para que se mezclen, pero no saturen la frase.
        
        if random.random() < 0.3:
            text = inject_phonetic_errors(text)
        
        if random.random() < 0.3:
            words = text.split()
            if len(words) > 2:
                target_len = random.randint(1, len(words))
                if target_len < len(words):
                    start = random.randint(0, len(words) - target_len)
                    text = " ".join(words[start:start+target_len])
            
        if random.random() < 0.3:
            try:
                choice = random.random()
                if choice < 0.33:
                    text = keyboard_aug.augment(text)[0]
                elif choice < 0.66:
                    text = swap_aug.augment(text)[0]
                else:
                    text = random_aug.augment(text)[0]
            except Exception: pass
            
        if random.random() < 0.2:
            try:
                text = inject_special_chars(text)
            except Exception: pass
                
        if random.random() < 0.15:
            text = text.upper() if random.random() < 0.5 else text.lower()
            
        augmented_rows.append({'frase': text})
        
    print("Sobreescribiendo el dataset final con datos balanceados...")
    df_final = pl.DataFrame(augmented_rows)
    df_final = df_final.sample(fraction=1.0, shuffle=True)
    
    df_final.write_csv(output_file)
    print("!Completado exitosamente!")

if __name__ == '__main__':
    main()
