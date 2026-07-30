import polars as pl
import random
import re

from spanish_nlp import augmentation

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
    input_file = r'd:\Proyectos\Olan\RedDragon\data\generador_nlp\datasets\fuente\control_cambios_original.csv'
    output_file = r'd:\Proyectos\Olan\RedDragon\data\generador_nlp\datasets\control_cambios_augmentado.csv'

    print("Cargando dataset original con Polars...")
    df = pl.read_csv(input_file, infer_schema_length=0, truncate_ragged_lines=True, quote_char='"')

    target_count = 10000
    needed = target_count

    print(f"Generando {needed} filas con balance de ruido y limpieza...")

    # Errores ortográficos reales del español (biblioteca spanish_nlp), no
    # simulación de tecleo/OCR: grapheme_spelling confunde grafemas que
    # suenan igual (b/v, s/z/c, ll/y, g/j), remove_accents omite tildes.
    grapheme_aug = augmentation.Spelling(method="grapheme_spelling", aug_percent=0.3, tokenizer="default")
    accent_aug = augmentation.Spelling(method="remove_accents", aug_percent=0.6, tokenizer="default")

    augmented_rows = []
    df = df.drop_nulls()
    valid_rows = [r for r in df.to_dicts() if 'frase' in r and 'etiqueta' in r and r['frase'] is not None and r['etiqueta'] is not None]

    for i in range(needed):
        if i % 1000 == 0 and i > 0:
            print(f"Progreso: {i} / {needed} generados...")

        origin_id = random.randrange(len(valid_rows))
        row = valid_rows[origin_id]
        text = str(row['frase'])
        etiqueta = str(row['etiqueta'])

        # 1. Sinónimos primero (mantiene la frase comprensible)
        text = replace_synonyms(text)

        # REGLA CLAVE: 25% de las oraciones se salvan de TODO ruido y corte.
        # Esto asegura que haya frases completamente claras en el dataset.
        if random.random() < 0.25:
            augmented_rows.append({'frase': text, 'origin_id': origin_id})
            continue

        # Omitir tildes es, con diferencia, la falta de ortografía más común en español.
        if random.random() < 0.5:
            try:
                text = accent_aug.augment(text, num_samples=1, num_workers=1)[0]
            except Exception: pass

        if random.random() < 0.3:
            try:
                text = grapheme_aug.augment(text, num_samples=1, num_workers=1)[0]
            except Exception: pass

        if random.random() < 0.15:
            words = text.split()
            if len(words) > 3:
                min_len = max(2, len(words) // 2)
                target_len = random.randint(min_len, len(words))
                if target_len < len(words):
                    start = random.randint(0, len(words) - target_len)
                    text = " ".join(words[start:start+target_len])

        if random.random() < 0.1:
            text = text.upper() if random.random() < 0.5 else text.lower()

        augmented_rows.append({'frase': text, 'origin_id': origin_id})

    print("Sobreescribiendo el dataset final con datos balanceados...")
    df_final = pl.DataFrame(augmented_rows)
    df_final = df_final.sample(fraction=1.0, shuffle=True)

    df_final.write_csv(output_file)
    print("!Completado exitosamente!")

if __name__ == '__main__':
    main()
