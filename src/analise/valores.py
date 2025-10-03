import os
import matplotlib.pyplot as plt
import pandas as pd
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stopwords_pt = set(stopwords.words('portuguese'))

categorias_sociais = {
    "Família": ["família", "pai", "mãe", "irmão", "irmã", "avó", "avô", "lar", "casa", "amor", "nosso", "ohana", "vínculo", "pais", "protegido"],
    "Amizade": ["amigo", "amizade", "companheiro", "juntos", "ajudar", "solidariedade", "confiança", "lealdade", "parceiro", "time", "grupo"],
    "Ética": ["regras", "certo", "correto", "lei", "disciplina", "obedecer", "cumprir", "respeitar", "ordem", "norma", "dever", "responsabilidade", "seguir", "limite", "autoridade", "escolha", "consciência"],
    "Coragem": ["coragem", "medo", "assustado", "ousar", "aventura", "herói", "lutar", "desafio", "salvar", "defender", "enfrentar", "perigo", "valente", "destemido"],
    "Diversidade": ["diferente", "aceitar", "inclusão", "respeito", "igualdade", "tolerância", "amizade", "união", "cultura", "raça", "origem"],
}

assets_path = "assets"  
decadas_docs = {}

for filename in os.listdir(assets_path):
    if filename.endswith(".txt"):
        decada = filename.replace(".txt", "")
        with open(os.path.join(assets_path, filename), "r", encoding="utf-8") as f:
            texto = f.read()
        linhas = texto.split("\n")
        blocos = [" ".join(linhas[i:i+20]) for i in range(0, len(linhas), 20)]
        blocos = [b.strip() for b in blocos if len(b.strip()) > 20]
        decadas_docs[decada] = blocos

def classificar_texto(texto, categorias):
    texto_lower = texto.lower()
    palavras = [w for w in texto_lower.split() if w not in stopwords_pt]
    contagem = {cat: 0 for cat in categorias.keys()}
    for cat, keywords in categorias.items():
        contagem[cat] = sum(palavra in keywords for palavra in palavras)
    return contagem


frequencias = {cat: {} for cat in categorias_sociais.keys()}

for decada, blocos in decadas_docs.items():
    print(f"\n📌 Processando {decada} ({len(blocos)} blocos)...")
    contagem_total = {cat: 0 for cat in categorias_sociais.keys()}
    for bloco in blocos:
        contagem = classificar_texto(bloco, categorias_sociais)
        for cat, count in contagem.items():
            contagem_total[cat] += count
    for cat in categorias_sociais.keys():
        frequencias[cat][decada] = contagem_total[cat]


df = pd.DataFrame(frequencias).T.fillna(0)
print("\n🔎 Frequência de valores sociais por década:")
print(df)


df.plot(kind="bar", figsize=(10,6))
plt.title("Valores e normas sociais em filmes infantis por década", fontsize=14)
plt.ylabel("Frequência de palavras associadas", fontsize=12)
plt.xlabel("Categorias sociais", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.legend(title="Década")
plt.tight_layout()
plt.show()
