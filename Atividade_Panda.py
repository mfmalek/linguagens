import numpy as np
import pandas as pd

df_vendas = pd.DataFrame(dados_vendas)
df_clientes = pd.DataFrame(dados_clientes)

print("Dimensões:", df_vendas.shape)
df_vendas.info()

df_vendas['valor'] = df_vendas['valor'].fillna(
    df_vendas.groupby('categoria')['valor'].transform('median')
)

vendas_altas = df_vendas.query("status == 'Concluído' and valor > 500")
print("\nVendas Concluídas > R$ 500:\n", vendas_altas)

df_completo = pd.merge(df_vendas, df_clientes, on='cliente_id', how='left')

df_completo['media_categoria'] = df_completo.groupby('categoria')['valor'].transform('mean')

qtd_gmail = df_completo['email'].str.contains('@gmail.com').sum()
print(f"\nTotal de vendas de clientes com Gmail: {qtd_gmail}")

df_completo['data_hora'] = pd.to_datetime(df_completo['data_hora'])
df_completo['mes'] = df_completo['data_hora'].dt.month_name()
df_completo['dia_semana'] = df_completo['data_hora'].dt.day_name()

tabela_dinamica = pd.pivot_table(
    df_completo,
    values='valor',
    index='categoria',
    columns='cidade',
    aggfunc='sum',
    fill_value=0
)

print("\nTabela Dinâmica:\n", tabela_dinamica)
