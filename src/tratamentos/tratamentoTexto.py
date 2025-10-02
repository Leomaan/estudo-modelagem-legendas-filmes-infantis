import glob
import re
import os

srt_folder = r"C:\Users\Leoman\Desktop\Legendas\Legendas\legendasextraidas"
output_folder = r"C:\Users\Leoman\Desktop\Legendas\Legendas\test"
os.makedirs(output_folder, exist_ok=True)

srt_files = glob.glob(os.path.join(srt_folder, '*.srt'))

for file_path in srt_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()

    text = ''
    for line in lines:
        # Ignorar números de sequência e timestamps
        if re.search(r'^\d+$', line) is None and re.search(r'^\d{2}:\d{2}:\d{2}', line) is None and line.strip() != '':
            # Remover tags HTML
            clean_line = re.sub(r'<.*?>', '', line).strip()
            if clean_line:
                text += clean_line + '\n'

    file_name = os.path.basename(file_path)
    name, ext = os.path.splitext(file_name)
    new_file_name = f"{name}.txt"
    new_file_path = os.path.join(output_folder, new_file_name)

    with open(new_file_path, 'w', encoding='utf-8') as f:
        f.write(text)

print(f"Processados {len(srt_files)} arquivos. Salvos em '{output_folder}'")
