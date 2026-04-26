"""
Análise Exploratória — Desempenho no ENEM por Região e Tipo de Escola
Autor: Gabriela da Matta Matos
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os

# ── Configurações visuais ──────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["figure.dpi"] = 130

CORES_ESCOLA = {"Pública": "#2E75B6", "Privada": "#ED7D31"}
CORES_REGIAO = ["#2E75B6", "#ED7D31", "#70AD47", "#FFC000", "#9B59B6"]
OUTPUT_DIR = "graficos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Carregar dados ─────────────────────────────────────────────────
df = pd.read_csv("dados_enem_simulado.csv")
print(f"✔ Dataset carregado: {len(df):,} participantes\n")

# ── Análise 1: Média geral por região ─────────────────────────────
print("── Média geral por região ──")
media_regiao = (
    df.groupby("regiao")["media_geral"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
media_regiao.columns = ["Região", "Média Geral"]
print(media_regiao.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(media_regiao["Região"], media_regiao["Média Geral"],
               color=CORES_REGIAO, edgecolor="white", height=0.6)
ax.bar_label(bars, fmt="%.1f", padding=5, fontsize=10, fontweight="bold")
ax.set_xlabel("Média Geral", fontsize=11)
ax.set_title("Média Geral no ENEM por Região", fontsize=13, fontweight="bold", pad=15)
ax.set_xlim(450, 620)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/1_media_por_regiao.png")
plt.close()
print("  → Gráfico salvo\n")

# ── Análise 2: Escola pública vs privada ──────────────────────────
print("── Média por tipo de escola ──")
media_escola = (
    df.groupby("tipo_escola")["media_geral"]
    .mean()
    .reset_index()
)
media_escola.columns = ["Tipo de Escola", "Média Geral"]
print(media_escola.to_string(index=False))

fig, ax = plt.subplots(figsize=(6, 5))
bars = ax.bar(media_escola["Tipo de Escola"], media_escola["Média Geral"],
              color=[CORES_ESCOLA[t] for t in media_escola["Tipo de Escola"]],
              edgecolor="white", width=0.5)
ax.bar_label(bars, fmt="%.1f", padding=5, fontsize=11, fontweight="bold")
ax.set_ylabel("Média Geral", fontsize=11)
ax.set_title("Desempenho: Escola Pública vs Privada", fontsize=13, fontweight="bold", pad=15)
ax.set_ylim(450, 640)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/2_publica_vs_privada.png")
plt.close()
print("  → Gráfico salvo\n")

# ── Análise 3: Desempenho por área de conhecimento ────────────────
print("── Média por área de conhecimento ──")
areas = {
    "Ciências da Natureza": "nota_ciencias_natureza",
    "Ciências Humanas": "nota_ciencias_humanas",
    "Linguagens": "nota_linguagens",
    "Matemática": "nota_matematica",
    "Redação": "nota_redacao",
}
media_areas = {area: df[col].mean() for area, col in areas.items()}
media_areas_df = pd.DataFrame(list(media_areas.items()), columns=["Área", "Média"])
print(media_areas_df.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(media_areas_df["Área"], media_areas_df["Média"],
               color="#2E75B6", edgecolor="white", height=0.55)
ax.bar_label(bars, fmt="%.1f", padding=5, fontsize=10, fontweight="bold")
ax.set_xlabel("Média", fontsize=11)
ax.set_title("Média por Área de Conhecimento", fontsize=13, fontweight="bold", pad=15)
ax.set_xlim(450, 600)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/3_media_por_area.png")
plt.close()
print("  → Gráfico salvo\n")

# ── Análise 4: Escola pública vs privada por região ───────────────
print("── Média por região e tipo de escola ──")
media_reg_escola = (
    df.groupby(["regiao", "tipo_escola"])["media_geral"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 5))
regioes = media_reg_escola["regiao"].unique()
x = range(len(regioes))
width = 0.35

for i, tipo in enumerate(["Pública", "Privada"]):
    vals = [
        media_reg_escola[(media_reg_escola["regiao"] == r) &
                          (media_reg_escola["tipo_escola"] == tipo)]["media_geral"].values[0]
        for r in regioes
    ]
    bars = ax.bar([xi + i * width for xi in x], vals, width,
                  label=tipo, color=CORES_ESCOLA[tipo], edgecolor="white")
    ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=9)

ax.set_xticks([xi + width / 2 for xi in x])
ax.set_xticklabels(regioes, fontsize=10)
ax.set_ylabel("Média Geral", fontsize=11)
ax.set_title("Escola Pública vs Privada por Região", fontsize=13, fontweight="bold", pad=15)
ax.legend(title="Tipo de Escola")
ax.set_ylim(450, 660)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/4_regiao_x_escola.png")
plt.close()
print("  → Gráfico salvo\n")

print("✔ Análise concluída! Gráficos salvos em /graficos")
