import os

# Caminho da pasta onde estão as legendas
pasta = r'C:\Users\Leoman\Desktop\Legendas\Legendas\legendasextraidas'

# Lista todos os arquivos com extensão .srt
legendas = [arquivo for arquivo in os.listdir(pasta) if arquivo.endswith('.srt')]

# Exibe a lista
for legenda in legendas:
    print(legenda)
    
print(f"\nTotal de legendas: {len(legendas)}")