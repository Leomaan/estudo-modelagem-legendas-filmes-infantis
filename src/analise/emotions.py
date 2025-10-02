import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from transformers import pipeline


try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')

print("Carregando o modelo de classificação de emoções...")
classificador_emocao = pipeline(
    "text-classification",
    model="michellejieli/emotion_text_classifier", 
    top_k=1
)
print("Modelo carregado com sucesso!")


def analisar_emocoes_arquivo(caminho_arquivo):
    print(f"Analisando o arquivo: {caminho_arquivo}...")
    
    mapa_emocoes = { 
        "joy": "Alegria", 
        "sadness": "Tristeza", 
        "fear": "Medo", 
        "anger": "Raiva", 
        "surprise": "Surpresa", 
        "love": "Amor" 
    }
    
    contagem_emocoes = {emocao: 0 for emocao in mapa_emocoes.values()}

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            texto = f.read()
    except FileNotFoundError:
        print(f"AVISO: Arquivo não encontrado: {caminho_arquivo}")
        return None

    sentencas = nltk.sent_tokenize(texto, language='portuguese')
    
    if not sentencas:
        print("Arquivo vazio ou sem sentenças para analisar.")
        return contagem_emocoes

    tokenizer = classificador_emocao.tokenizer
    # limite 512.
    limite_modelo = 512
    
    # segurança, um pouco menor
    chunk_size = 500
    stride = 100  

    textos_para_analise = []
    for sentenca in sentencas:
        #permite quebrar sentenças longas
        tokens = tokenizer(sentenca, truncation=False, padding=False)['input_ids']
        
        if len(tokens) < limite_modelo:
            textos_para_analise.append(sentenca)
        else:
            print(f"-> AVISO: Quebrando uma sentença longa com {len(tokens)} tokens...")
            # Removemos os tokens especiais de início/fim ([CLS], [SEP]) para a quebra
            input_ids_sem_especiais = tokens[1:-1]
            
            for i in range(0, len(input_ids_sem_especiais), chunk_size - stride):
                chunk_tokens = input_ids_sem_especiais[i : i + chunk_size]
                chunk_texto = tokenizer.decode(chunk_tokens)
                if chunk_texto and not chunk_texto.isspace():
                    textos_para_analise.append(chunk_texto)
        
    print(f"Processando um total de {len(textos_para_analise)} textos (sentenças + chunks)...")
    if not textos_para_analise:
        print("Nenhum texto válido para análise após o filtro.")
        return contagem_emocoes

    resultados = classificador_emocao(textos_para_analise, batch_size=16) 

    for resultado in resultados:
        label = resultado[0]['label']
        if label in mapa_emocoes:
            emocao_mapeada = mapa_emocoes[label]
            contagem_emocoes[emocao_mapeada] += 1
            
    print(f"Análise concluída.")
    return contagem_emocoes


pasta_assets = "assets"
decadas = ["1980s", "1990s", "2000s", "2010s"] 

resultados_por_decada = {}

for decada in decadas:
    caminho = os.path.join(pasta_assets, f"{decada}.txt")
    resultado = analisar_emocoes_arquivo(caminho)
    if resultado:
        resultados_por_decada[decada] = resultado


if resultados_por_decada:
    df_emocoes = pd.DataFrame.from_dict(resultados_por_decada, orient='index').fillna(0)
    
    df_percentual = df_emocoes.div(df_emocoes.sum(axis=1), axis=0) * 100

    print("\n--- Resultados (Contagem Absoluta das Emoções) ---")
    print(df_emocoes)
    
    print("\n--- Resultados (Percentual por Década entre as Emoções) ---")
    print(df_percentual.round(2))

    sns.set_style("whitegrid")
    ax = df_percentual.plot(
        kind='bar',
        figsize=(14, 8),
        colormap='viridis',
        rot=0
    )

    plt.title('Evolução Temporal das Emoções em Legendas de Filmes Infantis', fontsize=16)
    plt.ylabel('Distribuição Percentual (%)', fontsize=12)
    plt.xlabel('Década', fontsize=12)
    plt.legend(title='Emoções')
    plt.tight_layout()

    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', label_type='edge', fontsize=8)

    plt.show()
else:
    print("\nNenhuma análise foi realizada. Verifique se os arquivos estão na pasta 'assets'.")