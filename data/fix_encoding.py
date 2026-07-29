import sys

input_file = 'd:\\Proyectos\\Olan\\RedDragon\\data\\control_cambiosv2.csv'

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix common mojibake caused by reading UTF-8 as Windows-1252
try:
    # If the text was written as utf-8 but interpreted as latin1, 
    # we can reverse it.
    fixed_content = content.encode('windows-1252').decode('utf-8')
except Exception as e:
    # If it fails, fallback to simple string replacement
    replacements = {
        'Ã³': 'ó',
        'Ã¡': 'á',
        'Ã©': 'é',
        'Ã­': 'í',  # i acute
        'Ãº': 'ú',
        'Ã±': 'ñ',
        'Ã“': 'Ó',
        'Ã ': 'Á',
        'Ã‰': 'É',
        'Ã ': 'Í',
        'Ãš': 'Ú',
        'Ã‘': 'Ñ',
        'Ǹ': 'é'  # sometimes 'AlmacǸn' happens
    }
    fixed_content = content
    for bad, good in replacements.items():
        fixed_content = fixed_content.replace(bad, good)
        
with open(input_file, 'w', encoding='utf-8-sig') as f:
    f.write(fixed_content)

print('File encoding fixed and saved with UTF-8 BOM.')
