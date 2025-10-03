import os
import matplotlib.pyplot as plt
import pandas as pd
import nltk
from nltk.corpus import stopwords


try:
    stopwords_pt = set(stopwords.words('portuguese'))
except LookupError:
    print("Baixando pacote de stopwords do NLTK...")
    nltk.download('stopwords')
    stopwords_pt = set(stopwords.words('portuguese'))

categorias_emocionais = {
    "Alegria": ["feliz", "alegre", "contente", "radiante", "felicidade", "diversão", "riso", "sorriso", "celebração", "amor"],
    "Tristeza": ["triste", "tristeza", "choro", "lágrima", "sofrimento", "dor", "solitário", "melancolia", "pena", "coração partido"],
    "Medo": ["medo", "assustado", "pavor", "terror", "susto", "temer", "ansiedade", "perigo", "ameaça", "sombrio"],
    "Raiva": ["raiva", "ódio", "fúria", "bravo", "irritado", "zangado", "vingança", "luta", "briga", "injustiça"],
    "Surpresa": ["surpresa", "chocado", "espantado", "inesperado", "susto", "incrível", "inacreditável", "reviravolta"],
}

assets_path = "assets"
decadas_docs = {}


if not os.path.exists(assets_path):
    print("error na pasta")
else:
    for filename in sorted(os.listdir(assets_path)):
        if filename.endswith(".txt"):
            decada = filename.replace(".txt", "")
            with open(os.path.join(assets_path, filename), "r", encoding="utf-8") as f:
                texto = f.read()
            linhas = texto.split("\n")
            blocos = [" ".join(linhas[i:i+20]) for i in range(0, len(linhas), 20)]
            blocos = [b.strip() for b in blocos if len(b.strip()) > 10]
            decadas_docs[decada] = blocos

def classificar_emocao(texto, categorias):
    """Conta a ocorrência de palavras-chave de emoção em um texto."""
    texto_lower = texto.lower()
    palavras = [w.strip(".,!?-") for w in texto_lower.split()]
    contagem = {cat: 0 for cat in categorias.keys()}
    for cat, keywords in categorias.items():
        contagem[cat] = sum(palavra in keywords for palavra in palavras)
    return contagem

frequencias_emocionais = {cat: {} for cat in categorias_emocionais.keys()}

for decada, blocos in decadas_docs.items():
    contagem_total = {cat: 0 for cat in categorias_emocionais.keys()}
    for bloco in blocos:
        contagem = classificar_emocao(bloco, categorias_emocionais)
        for cat, count in contagem.items():
            contagem_total[cat] += count
    for cat in categorias_emocionais.keys():
        frequencias_emocionais[cat][decada] = contagem_total[cat]

df_emocoes = pd.DataFrame(frequencias_emocionais).T
df_emocoes.index.name = "Emoção"
print("\n🔎 Frequencia de emocoes por decada:")
print(df_emocoes)

df_emocoes.T.plot(kind="line", figsize=(12, 7), marker='o', colormap='viridis')
plt.title("Evolução das Emoções em Filmes Infantis por Década", fontsize=16)
plt.ylabel("Frequência de Palavras Associadas", fontsize=12)
plt.xlabel("Década", fontsize=12)
plt.xticks(rotation=0)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(title="Emoção")
plt.tight_layout()
plt.show()

df_proporcao = df_emocoes.div(df_emocoes.sum(axis=0), axis=1) * 100
df_proporcao.T.plot(kind="bar", stacked=True, figsize=(12, 7), colormap='plasma')
plt.title("Proporção de Emoções em Filmes Infantis por Década", fontsize=16)
plt.ylabel("Proporção (%)", fontsize=12)
plt.xlabel("Década", fontsize=12)
plt.xticks(rotation=0)
plt.legend(title="Emoção", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()