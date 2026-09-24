import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
n_registros = 120

datas = pd.date_range(start='2024-01-01', periods=n_registros, freq='D')
categorias = ['Eletronicos', 'Livros', 'Roupas', 'Automotivo']
estados = ['SP', 'RJ', 'MG', 'RS', 'BA']

dados = {
    'data': datas,
    'categoria': np.random.choice(categorias, size=n_registros),
    'estado': np.random.choice(estados, size=n_registros),
    'valor': np.random.uniform(50, 4500, size=n_registros).round(2),
    'quantidade': np.random.randint(1, 15, size=n_registros),
}

df = pd.DataFrame(dados)

df['valor_venda'] = (
    df['valor'] * np.random.uniform(0.9, 1.1, size=n_registros)
).round(2)

df = df.set_index('data')


faturamento_mensal = df['valor_venda'].resample('ME').sum()

plt.figure(figsize=(10, 5))

plt.plot(
    faturamento_mensal.index,
    faturamento_mensal.values,
    marker='o',
    linestyle='--',
    color='royalblue'
)

plt.title('Faturamento Mensal')
plt.xlabel('Mês')
plt.ylabel('Faturamento (R$)')
plt.grid(True, linestyle=':', alpha=0.7)

plt.tight_layout()
plt.show()


vendas_categoria = (
    df.groupby('categoria')['valor_venda']
    .sum()
    .sort_values()
)

plt.figure(figsize=(9, 5))

plt.bar(
    vendas_categoria.index,
    vendas_categoria.values,
    color='seagreen'
)

plt.title('Total de Vendas por Categoria')
plt.xlabel('Categoria')
plt.ylabel('Total Vendido (R$)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


plt.figure(figsize=(9, 5))

plt.hist(
    df['valor'],
    bins=10,
    edgecolor='black',
    color='skyblue'
)

plt.title('Distribuição dos Valores das Vendas')
plt.xlabel('Valor da Venda (R$)')
plt.ylabel('Frequência')

plt.tight_layout()
plt.show()


quantidade_mensal = df['quantidade'].resample('ME').sum()

fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    figsize=(11, 8),
    sharex=True
)

ax1.plot(
    faturamento_mensal.index,
    faturamento_mensal.values,
    marker='o',
    color='darkblue',
    linewidth=2
)

ax1.set_title('Faturamento Mensal')
ax1.set_ylabel('Faturamento (R$)')
ax1.grid(True, linestyle=':', alpha=0.6)

ax2.bar(
    quantidade_mensal.index,
    quantidade_mensal.values,
    color='coral'
)

ax2.set_title('Quantidade Total de Itens Vendidos por Mês')
ax2.set_xlabel('Mês')
ax2.set_ylabel('Quantidade')
ax2.grid(axis='y', linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()


quantidade_media_mensal = df['quantidade'].resample('ME').mean()

fig, ax1 = plt.subplots(figsize=(11, 6))

barras = ax1.bar(
    faturamento_mensal.index,
    faturamento_mensal.values,
    width=20,
    color='steelblue',
    alpha=0.75,
    label='Faturamento'
)

ax1.set_xlabel('Mês')
ax1.set_ylabel('Faturamento (R$)', color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax1.grid(axis='y', linestyle=':', alpha=0.5)

ax2 = ax1.twinx()

linha = ax2.plot(
    quantidade_media_mensal.index,
    quantidade_media_mensal.values,
    color='darkorange',
    marker='o',
    linewidth=2,
    label='Quantidade média'
)

ax2.set_ylabel(
    'Quantidade Média de Itens por Venda',
    color='darkorange'
)
ax2.tick_params(axis='y', labelcolor='darkorange')

plt.title('Faturamento e Quantidade Média de Itens por Venda')

plt.tight_layout()
plt.show()


mes_maior_faturamento = faturamento_mensal.idxmax()
maior_faturamento = faturamento_mensal.max()

fig, ax = plt.subplots(figsize=(11, 6))

ax.plot(
    faturamento_mensal.index,
    faturamento_mensal.values,
    marker='o',
    linestyle='--',
    color='purple',
    linewidth=2
)

ax.set_title('Faturamento Mensal com Destaque para o Maior Valor')
ax.set_xlabel('Mês')
ax.set_ylabel('Faturamento (R$)')
ax.grid(True, linestyle=':', alpha=0.6)

ax.annotate(
    f'Maior faturamento\nR$ {maior_faturamento:,.2f}',
    xy=(mes_maior_faturamento, maior_faturamento),
    xytext=(20, 30),
    textcoords='offset points',
    arrowprops=dict(
        arrowstyle='->',
        color='red',
        linewidth=2
    ),
    fontsize=10,
    color='red',
    bbox=dict(
        boxstyle='round,pad=0.4',
        facecolor='white',
        edgecolor='red'
    )
)

plt.tight_layout()
plt.show()


pivot_vendas = pd.pivot_table(
    df,
    values='valor_venda',
    index='categoria',
    columns='estado',
    aggfunc='sum'
)

print('Tabela dinâmica:')
print(pivot_vendas)


fig, ax = plt.subplots(figsize=(9, 6))

heatmap = ax.imshow(
    pivot_vendas.values,
    cmap='YlGnBu',
    aspect='auto'
)

ax.set_xticks(
    np.arange(len(pivot_vendas.columns))
)
ax.set_xticklabels(
    pivot_vendas.columns
)

ax.set_yticks(
    np.arange(len(pivot_vendas.index))
)
ax.set_yticklabels(
    pivot_vendas.index
)

ax.set_xlabel('Estado')
ax.set_ylabel('Categoria')
ax.set_title('Heatmap de Vendas por Categoria e Estado')

cbar = plt.colorbar(heatmap, ax=ax)
cbar.set_label('Total de Vendas (R$)')

for i in range(len(pivot_vendas.index)):
    for j in range(len(pivot_vendas.columns)):
        valor = pivot_vendas.iloc[i, j]

        ax.text(
            j,
            i,
            f'R$ {valor:,.0f}',
            ha='center',
            va='center',
            color='black',
            fontsize=8
        )

plt.tight_layout()


plt.savefig(
    'heatmap_vendas.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()
