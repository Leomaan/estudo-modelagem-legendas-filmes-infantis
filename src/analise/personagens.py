import os
import re
from collections import defaultdict

# Tenta importar as bibliotecas de dados e gráficos
try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError:
   
    print("Bibliotecas não encontradas.")
    exit()

def buscar_palavras_na_decada(caminho_arquivo, palavras_alvo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo_completo = f.read().lower()
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

    contagens = {}
    for palavra in palavras_alvo:
        ocorrencias = re.findall(r'\b' + re.escape(palavra.lower()) + r'\b', conteudo_completo)
        contagens[palavra] = len(ocorrencias)
        
    return contagens

def plotar_grafico(dataframe, palavras, titulo):
    palavras_validas = [p for p in palavras if p in dataframe.index]
    if not palavras_validas:
        # A mensagem de aviso para gráficos vazios foi removida
        return

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    for palavra in palavras_validas:
        ax.plot(dataframe.columns, dataframe.loc[palavra], marker='o', linestyle='-', label=palavra)

    ax.set_title(titulo, fontsize=16, pad=20)
    ax.set_ylabel("Frequência de Ocorrências", fontsize=12)
    ax.set_xlabel("Década", fontsize=12)
    ax.legend(title="Palavras", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.show()

def main(): 
    PALAVRAS_PARA_BUSCAR = [
        # Infantis e Fantasia
         "mágico", "príncipe", "princesa", "rei", "rainha", "herói", "monstro", "amigo", "brincar",
        
        # Animais e Natureza
        "animal", "urso", "cachorro", "gato", "macaco", "rato", 
    ]
    
    pasta_decadas = 'assets'
    
    if not os.path.isdir(pasta_decadas):
        return

    arquivos_txt = sorted([f for f in os.listdir(pasta_decadas) if f.endswith('.txt')])
    
    if not arquivos_txt:
        return

    resultados_gerais = defaultdict(dict)
    for nome_arquivo in arquivos_txt:
        caminho_completo = os.path.join(pasta_decadas, nome_arquivo)
        decada = os.path.splitext(nome_arquivo)[0]
        contagens_decada = buscar_palavras_na_decada(caminho_completo, PALAVRAS_PARA_BUSCAR)
        if contagens_decada:
            for palavra, contagem in contagens_decada.items():
                resultados_gerais[palavra][decada] = contagem
    if not resultados_gerais:
        return
        
    decadas_ordenadas = sorted(resultados_gerais[PALAVRAS_PARA_BUSCAR[0]].keys())
    
    df_resultados = pd.DataFrame.from_dict(resultados_gerais, orient='index')
    df_resultados = df_resultados[decadas_ordenadas]

    grupo_infantil = [
        "mágico", "príncipe", "princesa", "rei", "rainha", "herói", "monstro", "amigo", "brincar",
    ]
    grupo_animais = [
        "animal", "urso", "cachorro", "gato", "macaco", "rato", 
    ]
    
    plotar_grafico(df_resultados, grupo_infantil, "Evolução de Termos infantis e de Fantasia")
    plotar_grafico(df_resultados, grupo_animais, "Frequência de Animais em Narrativas")

if __name__ == "__main__":
    main()