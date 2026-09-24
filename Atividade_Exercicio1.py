import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


np.random.seed(42)

datas = pd.date_range(
    start="2024-01-01",
    end="2024-06-30",
    freq="D"
)

produtos = [
    "Notebook",
    "Smartphone",
    "Fone de Ouvido",
    "Monitor"
]

dados = {
    "Data": np.random.choice(datas, size=300),
    "Produto": np.random.choice(
        produtos,
        size=300,
        p=[0.2, 0.4, 0.25, 0.15]
    ),
    "Quantidade": np.random.randint(1, 6, size=300),
    "Preco_Unitario": 0
}

df = pd.DataFrame(dados)


precos = {
    "Notebook": 3500,
    "Smartphone": 2000,
    "Fone de Ouvido": 150,
    "Monitor": 1200
}

df["Preco_Unitario"] = df["Produto"].map(precos)

print("Dataset criado com sucesso!")

print("\nPrimeiras 5 linhas:")
print(df.head())


df["Faturamento_Total"] = (
    df["Quantidade"] * df["Preco_Unitario"]
)

faturamento_produto = (
    df.groupby("Produto")["Faturamento_Total"]
    .sum()
    .sort_values(ascending=False)
)

print("\nFaturamento total por produto:")
print(faturamento_produto)


plt.figure(figsize=(9, 6))

plt.bar(
    faturamento_produto.index,
    faturamento_produto.values,
    color="steelblue"
)

plt.xlabel("Produto")
plt.ylabel("Faturamento Total (R$)")
plt.title("Faturamento Total por Produto")

plt.xticks(rotation=15)

plt.tight_layout()
plt.show()


df["Mes"] = df["Data"].dt.to_period("M")

faturamento_mes = (
    df.groupby("Mes")["Faturamento_Total"]
    .sum()
    .sort_index()
)

print("\nFaturamento total por mês:")
print(faturamento_mes)


plt.figure(figsize=(10, 6))

plt.plot(
    faturamento_mes.index.astype(str),
    faturamento_mes.values,
    marker="o",
    color="green",
    linewidth=2
)

plt.xlabel("Mês")
plt.ylabel("Faturamento Total (R$)")
plt.title("Evolução das Vendas ao Longo do Tempo")

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()


quantidade_produto = (
    df.groupby("Produto")["Quantidade"]
    .sum()
    .sort_values(ascending=False)
)

print("\nQuantidade total vendida por produto:")
print(quantidade_produto)


plt.figure(figsize=(8, 8))

plt.pie(
    quantidade_produto.values,
    labels=quantidade_produto.index,
    autopct="%.1f%%",
    startangle=90
)

plt.title("Proporção da Quantidade de Itens Vendidos por Produto")

plt.axis("equal")

plt.tight_layout()
plt.show()
