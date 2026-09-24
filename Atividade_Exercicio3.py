import pandas as pd
import matplotlib.pyplot as plt

df_stream = pd.read_csv("streamdata_usuarios.csv")

print("Primeiras 5 linhas:")
print(df_stream.head())

print("\nInformações do DataFrame:")
df_stream.info()


media_horas_plano = (
    df_stream.groupby("plano")["horas_assistidas"]
    .mean()
    .sort_values()
)

print("\nMédia de horas assistidas por plano:")
print(media_horas_plano)

plt.figure(figsize=(8, 5))

plt.barh(
    media_horas_plano.index,
    media_horas_plano.values,
    color=["#4C78A8", "#F58518", "#54A24B"]
)

plt.xlabel("Média de horas assistidas por mês")
plt.ylabel("Plano")
plt.title("Média de Horas Assistidas por Plano")

plt.grid(axis="x", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()


usuarios_cancelaram = df_stream[
    df_stream["cancelou_assinatura"] == "Sim"
]

usuarios_ativos = df_stream[
    df_stream["cancelou_assinatura"] == "Não"
]

plt.figure(figsize=(9, 5))

plt.hist(
    usuarios_cancelaram["score_satisfacao"],
    bins=range(1, 12),
    alpha=0.6,
    label="Cancelaram",
    color="red",
    edgecolor="black"
)

plt.hist(
    usuarios_ativos["score_satisfacao"],
    bins=range(1, 12),
    alpha=0.6,
    label="Ativos",
    color="steelblue",
    edgecolor="black"
)

plt.xlabel("Score de satisfação")
plt.ylabel("Quantidade de usuários")
plt.title("Distribuição da Satisfação por Status de Assinatura")

plt.xticks(range(1, 11))
plt.legend()

plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()


contagem_dispositivos = (
    df_stream["dispositivo_principal"]
    .value_counts()
)

print("\nQuantidade de usuários por dispositivo:")
print(contagem_dispositivos)

dispositivo_mais_utilizado = contagem_dispositivos.idxmax()

explode = [
    0.1 if dispositivo == dispositivo_mais_utilizado else 0
    for dispositivo in contagem_dispositivos.index
]

plt.figure(figsize=(8, 8))

plt.pie(
    contagem_dispositivos.values,
    labels=contagem_dispositivos.index,
    autopct="%.1f%%",
    explode=explode,
    startangle=90
)

plt.title("Distribuição dos Dispositivos Principais")
plt.axis("equal")

plt.tight_layout()
plt.show()
