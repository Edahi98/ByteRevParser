input_file = 'd:\\Proyectos\\Olan\\RedDragon\\data\\control_cambiosv2.csv'
with open(input_file, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace('Ã ndice', 'Índice')
content = content.replace('Ã', 'Í') # just in case

with open(input_file, 'w', encoding='utf-8-sig') as f:
    f.write(content)
