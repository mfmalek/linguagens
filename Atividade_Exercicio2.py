import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_theme(style="whitegrid")

np.random.seed(101)


n = 200

categorias = [
    "Eletrônicos",
    "Vestuário",
    "Casa e Decoração",
    "Livros"
]

dados = {
    "ID_Cliente": np.random.randint(1000, 1050, size=n),
    "Categoria": np.random.choice(categorias, size=n),
    "Valor_Gasto": np.random.normal(
        loc=250,
        scale=80,
        size=n
    ).round(2),
    "Avaliacao_Compra": np.random.choice(
        [1, 2, 3, 4, 5, np.nan],
        size=n,
        p=[0.1, 0.1, 0.2, 0.3, 0.2, 0.1]
    ),
    "Idade_Cliente": np.random.randint(18, 65, size=n)
}

df_ecommerce = pd.DataFrame(dados)

df_ecommerce = pd.concat(
    [df_ecommerce, df_ecommerce.iloc[:10]],
    ignore_index=True
)

print("Dataset gerado com sucesso!")
print(f"Total de linhas no dataset: {len(df_ecommerce)}")

print("\nPrimeiras 5 linhas:")
print(df_ecommerce.head())


quantidade_duplicadas = df_ecommerce.duplicated().sum()

print("\nQuantidade de linhas duplicadas:")
print(quantidade_duplicadas)

df_ecommerce = df_ecommerce.drop_duplicates()

print("\nTotal de linhas após remover duplicatas:")
print(len(df_ecommerce))


print("\nQuantidade de valores nulos por coluna:")
print(df_ecommerce.isnull().sum())


mediana_avaliacao = df_ecommerce["Avaliacao_Compra"].median()

print("\nMediana da Avaliacao_Compra:")
print(mediana_avaliacao)

df_ecommerce["Avaliacao_Compra"] = (
    df_ecommerce["Avaliacao_Compra"]
    .fillna(mediana_avaliacao)
)

print("\nValores nulos após o tratamento:")
print(df_ecommerce.isnull().sum())



plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df_ecommerce,
    x="Categoria",
    y="Valor_Gasto"
)

plt.xlabel("Categoria")
plt.ylabel("Valor Gasto")
plt.title("Distribuição do Valor Gasto por Categoria")

plt.xticks(rotation=15)

plt.tight_layout()
plt.show()


print("\nEstatísticas de Valor_Gasto por categoria:")

estatisticas_categoria = (
    df_ecommerce
    .groupby("Categoria")["Valor_Gasto"]
    .agg(["count", "mean", "std", "min", "max"])
    .sort_values("std", ascending=False)
)

print(estatisticas_categoria)



plt.figure(figsize=(10, 6))

sns.histplot(
    data=df_ecommerce,
    x="Idade_Cliente",
    kde=True,
    bins=15,
    color="steelblue"
)

plt.xlabel("Idade do Cliente")
plt.ylabel("Quantidade de Clientes")
plt.title("Distribuição da Idade dos Clientes")

plt.tight_layout()
plt.show()
