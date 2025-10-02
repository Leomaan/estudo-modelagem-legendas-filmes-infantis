import os
import re
import pandas as pd
import nltk  # Substituído o spacy por nltk
from tqdm import tqdm
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Ignorar avisos de uso de memória do TQDM e outros
warnings.filterwarnings('ignore')

# --- CONFIGURAÇÃO ---
PASTA_ASSETS = 'assets'
ARQUIVO_CLASSIFICACAO_PAPEIS = 'personagens_papeis.csv'
ARQUIVO_PARA_CLASSIFICAR = 'personagens_para_classificar.csv'
TAMANHO_AMOSTRA_IA = 5000  # Número de falas para analisar com IA (sentimento e verbos)

# --- FUNÇÕES DE ANÁLISE ---

def extrair_falas_das_decadas(pasta_assets):
    """
    Lê todos os arquivos .txt da pasta_assets, extrai falas e personagens
    e retorna um único DataFrame.
    """
    print("Iniciando extração de diálogos dos arquivos .txt...")
    todos_os_dados = []
    arquivos_txt = [f for f in os.listdir(pasta_assets) if f.endswith('.txt')]
    
    padrao = re.compile(r'^([A-Z][A-Z\s\(\).0-9\-]+):\s*(.*)')

    for nome_arquivo in tqdm(arquivos_txt, desc="Lendo arquivos de décadas"):
        decada = nome_arquivo.replace('.txt', '')
        caminho_arquivo = os.path.join(pasta_assets, nome_arquivo)
        
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
        except UnicodeDecodeError:
            with open(caminho_arquivo, 'r', encoding='latin-1') as f:
                linhas = f.readlines()

        for linha in linhas:
            match = padrao.match(linha)
            if match:
                personagem, dialogo = match.groups()
                personagem_limpo = personagem.strip().upper()
                if dialogo.strip():
                    todos_os_dados.append({
                        'decada': decada,
                        'personagem': personagem_limpo,
                        'dialogo': dialogo.strip()
                    })

    df = pd.DataFrame(todos_os_dados)
    print(f"Extração concluída. Total de {len(df)} falas encontradas.")
    return df

def analisar_atributos_linguisticos(df_amostra):
    """
    Aplica as análises de Sentimento e Verbos a um DataFrame de amostra.
    """
    print("\nIniciando análises de IA (isso pode demorar)...")
    
    # 1. Análise de Sentimento com Transformers (sem alteração)
    print(f"  - Analisando sentimento em {len(df_amostra)} falas de amostra...")
    sentiment_pipeline = pipeline("sentiment-analysis", model="luhf/bert-base-portuguese-cased-sentiment")
    
    def get_sentiment(text):
        try:
            result = sentiment_pipeline(text[:512])[0]
            score = 0
            if result['label'] == 'POSITIVE': score = 1
            elif result['label'] == 'NEGATIVE': score = -1
            return score
        except Exception:
            return None
            
    tqdm.pandas(desc="  - Calculando sentimento")
    df_amostra['sentimento'] = df_amostra['dialogo'].progress_apply(get_sentiment)

    # 2. Análise de Verbos com NLTK (MODIFICADO)
    print(f"  - Extraindo verbos com NLTK...")
    
    def extrair_verbos_nltk(texto):
        # NLTK para português usa o etiquetador do corpus Mac-Morpho
        # As etiquetas de verbo geralmente começam com 'V'
        try:
            tokens = nltk.word_tokenize(texto.lower())
            tags = nltk.pos_tag(tokens) # Usa o tagger padrão treinado no Mac-Morpho
            verbos = [palavra for palavra, tag in tags if tag.startswith('V')]
            return verbos
        except Exception:
            return []

    tqdm.pandas(desc="  - Extraindo verbos")
    df_amostra['verbos'] = df_amostra['dialogo'].progress_apply(extrair_verbos_nltk)
    
    print("Análises de IA concluídas.")
    return df_amostra

def gerar_visualizacoes(df_final, df_frequencia):
    """
    Gera e salva gráficos a partir dos dados analisados.
    """
    print("\nGerando visualizações...")
    
    # Gráfico 1: Sentimento Médio por Papel ao Longo das Décadas
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    sentimento_por_decada = df_final.groupby(['decada', 'papel'])['sentimento'].mean().unstack()
    sentimento_por_decada.plot(kind='line', marker='o', ax=ax)
    
    ax.set_title('Sentimento Médio por Papel ao Longo das Décadas', fontsize=16)
    ax.set_ylabel('Sentimento Médio (de -1 a 1)')
    ax.set_xlabel('Década')
    ax.legend(title='Papel')
    ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
    plt.tight_layout()
    plt.savefig('sentimento_por_decada.png')
    print("  - Gráfico 'sentimento_por_decada.png' salvo.")

    # Gráfico 2: Frequência de Falas (Contagem de Palavras)
    fig, ax = plt.subplots(figsize=(12, 7))
    df_frequencia.plot(kind='bar', stacked=True, ax=ax)
    
    ax.set_title('Volume de Palavras por Papel ao Longo das Décadas', fontsize=16)
    ax.set_ylabel('Total de Palavras')
    ax.set_xlabel('Década')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig('frequencia_palavras_por_decada.png')
    print("  - Gráfico 'frequencia_palavras_por_decada.png' salvo.")
    
    plt.close('all')

# --- BLOCO DE EXECUÇÃO PRINCIPAL ---

if __name__ == "__main__":
    if not os.path.exists(PASTA_ASSETS) or not os.listdir(PASTA_ASSETS):
        print(f"ERRO: A pasta '{PASTA_ASSETS}' não foi encontrada ou está vazia.")
        print("Por favor, crie a pasta e coloque seus arquivos .txt dentro dela.")
    else:
        df_dialogos = extrair_falas_das_decadas(PASTA_ASSETS)
        
        if not os.path.exists(ARQUIVO_CLASSIFICACAO_PAPEIS):
            print(f"\nAVISO: O arquivo de classificação '{ARQUIVO_CLASSIFICACAO_PAPEIS}' não foi encontrado.")
            
            contagem_personagens = df_dialogos['personagem'].value_counts().reset_index()
            contagem_personagens.columns = ['personagem', 'contagem_falas']
            contagem_personagens.to_csv(ARQUIVO_PARA_CLASSIFICAR, index=False)
            
            print(f"Foi criado um arquivo chamado '{ARQUIVO_PARA_CLASSIFICAR}'.")
            print("1. Abra este arquivo em um editor de planilhas.")
            print("2. Adicione uma nova coluna chamada 'papel'.")
            print("3. Preencha com 'heroi', 'vilao' ou 'coadjuvante'.")
            print(f"4. Salve o arquivo com o nome '{ARQUIVO_CLASSIFICACAO_PAPEIS}' e rode este script novamente.")
        else:
            print(f"\nArquivo de classificação '{ARQUIVO_CLASSIFICACAO_PAPEIS}' encontrado. Continuando a análise...")
            
            df_papeis = pd.read_csv(ARQUIVO_CLASSIFICACAO_PAPEIS)
            df_papeis = df_papeis[['personagem', 'papel']].dropna()
            df_completo = pd.merge(df_dialogos, df_papeis, on='personagem', how='inner')
            
            print("\nDistribuição de falas por papel encontrado:")
            print(df_completo['papel'].value_counts())
            
            df_completo['contagem_palavras'] = df_completo['dialogo'].apply(lambda x: len(x.split()))
            analise_frequencia = df_completo.groupby(['decada', 'papel'])['contagem_palavras'].sum().unstack().fillna(0)
            
            print("\n--- ANÁLISE DE FREQUÊNCIA (TOTAL DE PALAVRAS) ---")
            print(analise_frequencia)

            tamanho_real_amostra = min(TAMANHO_AMOSTRA_IA, len(df_completo))
            df_amostra = df_completo.sample(n=tamanho_real_amostra, random_state=42)
            
            df_analisado = analisar_atributos_linguisticos(df_amostra)

            analise_sentimento = df_analisado.groupby(['decada', 'papel'])['sentimento'].mean().unstack().fillna(0)
            print("\n--- ANÁLISE DE SENTIMENTO (SCORE MÉDIO) ---")
            print(analise_sentimento)
            
            print("\n--- ANÁLISE DE VERBOS (TOP 5 MAIS COMUNS POR PAPEL) ---")
            for papel in ['heroi', 'vilao', 'coadjuvante']:
                if papel in df_analisado['papel'].unique():
                    verbos = df_analisado[df_analisado['papel'] == papel]['verbos'].explode().value_counts()
                    print(f"\nPapel: {papel.upper()}")
                    print(verbos.head(5))

            gerar_visualizacoes(df_analisado, analise_frequencia)
            
            print("\nAnálise concluída com sucesso!")