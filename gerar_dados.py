"""
Gerador de dados simulados inspirados no ENEM.
Usado para fins de portfólio — estrutura baseada nos microdados reais do INEP.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

n = 5000

regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
estados = {
    "Norte": ["AM", "PA", "RO", "RR", "AC", "AP", "TO"],
    "Nordeste": ["BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE", "AL"],
    "Centro-Oeste": ["GO", "MT", "MS", "DF"],
    "Sudeste": ["SP", "RJ", "MG", "ES"],
    "Sul": ["PR", "SC", "RS"],
}
tipo_escola = ["Pública", "Privada"]
sexo = ["F", "M"]

regiao_aluno = np.random.choice(regioes, n, p=[0.08, 0.27, 0.08, 0.43, 0.14])
estado_aluno = [np.random.choice(estados[r]) for r in regiao_aluno]
escola_aluno = np.random.choice(tipo_escola, n, p=[0.75, 0.25])
sexo_aluno = np.random.choice(sexo, n)

# Médias base por região e tipo de escola
media_base = {
    ("Norte", "Pública"): 490, ("Norte", "Privada"): 580,
    ("Nordeste", "Pública"): 485, ("Nordeste", "Privada"): 575,
    ("Centro-Oeste", "Pública"): 510, ("Centro-Oeste", "Privada"): 600,
    ("Sudeste", "Pública"): 525, ("Sudeste", "Privada"): 620,
    ("Sul", "Pública"): 530, ("Sul", "Privada"): 615,
}

notas_cn, notas_ch, notas_lc, notas_mt, notas_red = [], [], [], [], []

for r, e in zip(regiao_aluno, escola_aluno):
    base = media_base[(r, e)]
    notas_cn.append(round(np.clip(np.random.normal(base, 70), 300, 1000), 1))
    notas_ch.append(round(np.clip(np.random.normal(base + 10, 65), 300, 1000), 1))
    notas_lc.append(round(np.clip(np.random.normal(base + 5, 60), 300, 1000), 1))
    notas_mt.append(round(np.clip(np.random.normal(base - 20, 90), 300, 1000), 1))
    notas_red.append(round(np.clip(np.random.normal(base + 15, 150), 0, 1000), 1))

df = pd.DataFrame({
    "regiao": regiao_aluno,
    "estado": estado_aluno,
    "tipo_escola": escola_aluno,
    "sexo": sexo_aluno,
    "nota_ciencias_natureza": notas_cn,
    "nota_ciencias_humanas": notas_ch,
    "nota_linguagens": notas_lc,
    "nota_matematica": notas_mt,
    "nota_redacao": notas_red,
})

df["media_geral"] = df[["nota_ciencias_natureza", "nota_ciencias_humanas",
                          "nota_linguagens", "nota_matematica", "nota_redacao"]].mean(axis=1).round(1)

df.to_csv("dados_enem_simulado.csv", index=False)
print(f"Dataset gerado: {len(df)} registros")
print(df.head())
