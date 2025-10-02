import zipfile
import os
import re

pasta_zip = r"C:\Users\Leoman\Desktop\Legendas\Legendas"
pasta_srt = r"C:\Users\Leoman\Desktop\Legendas\Legendas\test"

padrao = re.compile(r"(.*?)[\.\s\(\[]*(\d{4})[\)\]]*")

for arquivo in os.listdir(pasta_zip):
    if arquivo.lower().endswith(".zip"):
        caminho_zip = os.path.join(pasta_zip, arquivo)
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            for nome_arquivo in zip_ref.namelist():
                if nome_arquivo.lower().endswith(".srt"):
                    match = padrao.search(arquivo)
                    if match:
                        nome, ano = match.groups()
                        nome_srt = f"{nome}.{ano}.srt"
                    else:

                        nome_srt = nome_arquivo
                    caminho_destino = os.path.join(pasta_srt, nome_srt)

                    with zip_ref.open(nome_arquivo) as srt_file, open(caminho_destino, 'wb') as out_file:
                        out_file.write(srt_file.read())

print("Extração feita")
