import glob
import os
import re

txt_folder = r"C:\Users\Leoman\Desktop\Legendas\Legendas\txt"
output_folder = r"C:\Users\Leoman\Desktop\Legendas\Legendas\TextoPorDecada"
os.makedirs(output_folder, exist_ok=True)

txt_files = glob.glob(os.path.join(txt_folder, '*.txt'))

decadas = {}

for file_path in txt_files:
    file_name = os.path.basename(file_path)
    
    # Extrair os últimos 4 dígitos antes da extensão como ano
    match = re.search(r'(\d{4})\.txt$', file_name)
    if match:
        ano = int(match.group(1))
        decada = f"{ano//10*10}s"  # exemplo: 2010 → 2010s
    else:
        decada = "SemAno"

    # Ler o texto
    with open(file_path, 'r', encoding='utf-8') as f:
        texto = f.read()
    
    # Acumular no dicionário
    if decada not in decadas:
        decadas[decada] = []
    decadas[decada].append(texto)

# Salvar um arquivo por década
for decada, textos in decadas.items():
    combined_text = "\n".join(textos)
    output_path = os.path.join(output_folder, f"{decada}.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(combined_text)

print(f"Arquivos combinados por década salvos em '{output_folder}'")
