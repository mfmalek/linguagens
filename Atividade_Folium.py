import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster

np.random.seed(42)
n_imoveis = 45

dados_imoveis = {
    'id_imovel': range(1, n_imoveis + 1),
    'cidade': np.where(
        np.random.rand(n_imoveis) > 0.4,
        'Nova Iguaçu',
        'Queimados'
    ),
    'valor_venda': np.random.uniform(
        150000, 850000, n_imoveis
    ).round(2),
    'tipo': np.random.choice(
        ['Casa', 'Apartamento', 'Terreno'],
        n_imoveis
    )
}

df_mapa = pd.DataFrame(dados_imoveis)


def gerar_lat(cidade):
    if cidade == 'Nova Iguaçu':
        return -22.756 + np.random.uniform(-0.03, 0.03)
    return -22.716 + np.random.uniform(-0.02, 0.02)


def gerar_lon(cidade):
    if cidade == 'Nova Iguaçu':
        return -43.460 + np.random.uniform(-0.03, 0.03)
    return -43.555 + np.random.uniform(-0.02, 0.02)


df_mapa['latitude'] = df_mapa['cidade'].apply(gerar_lat)
df_mapa['longitude'] = df_mapa['cidade'].apply(gerar_lon)

display(df_mapa.head())


centro_lat = df_mapa['latitude'].mean()
centro_lon = df_mapa['longitude'].mean()


mapa_basico = folium.Map(
    location=[centro_lat, centro_lon],
    zoom_start=12,
    tiles='OpenStreetMap'
)

for _, imovel in df_mapa.head(5).iterrows():

    popup_texto = (
        f"<b>Tipo:</b> {imovel['tipo']}<br>"
        f"<b>Valor de venda:</b> "
        f"R$ {imovel['valor_venda']:,.2f}"
    )

    folium.Marker(
        location=[
            imovel['latitude'],
            imovel['longitude']
        ],
        popup=folium.Popup(
            popup_texto,
            max_width=300
        )
    ).add_to(mapa_basico)


mapa_basico

mapa_circulos = folium.Map(
    location=[centro_lat, centro_lon],
    zoom_start=12,
    tiles='OpenStreetMap'
)

cores_cidade = {
    'Nova Iguaçu': 'blue',
    'Queimados': 'orange'
}

for _, imovel in df_mapa.iterrows():

    cor = cores_cidade[imovel['cidade']]

    popup_texto = (
        f"<b>ID:</b> {imovel['id_imovel']}<br>"
        f"<b>Cidade:</b> {imovel['cidade']}<br>"
        f"<b>Tipo:</b> {imovel['tipo']}<br>"
        f"<b>Valor:</b> "
        f"R$ {imovel['valor_venda']:,.2f}"
    )

    folium.CircleMarker(
        location=[
            imovel['latitude'],
            imovel['longitude']
        ],
        radius=8,
        color=cor,
        fill=True,
        fill_color=cor,
        fill_opacity=0.7,
        tooltip='Clique para detalhes',
        popup=folium.Popup(
            popup_texto,
            max_width=300
        )
    ).add_to(mapa_circulos)

mapa_circulos

mapa_cluster = folium.Map(
    location=[centro_lat, centro_lon],
    zoom_start=12,
    tiles='OpenStreetMap'
)

cluster = MarkerCluster().add_to(mapa_cluster)

cores_tipo = {
    'Casa': 'green',
    'Apartamento': 'blue',
    'Terreno': 'gray'
}

for _, imovel in df_mapa.iterrows():

    cor = cores_tipo[imovel['tipo']]

    popup_texto = (
        f"<b>ID do imóvel:</b> {imovel['id_imovel']}<br>"
        f"<b>Cidade:</b> {imovel['cidade']}<br>"
        f"<b>Tipo:</b> {imovel['tipo']}<br>"
        f"<b>Valor de venda:</b> "
        f"R$ {imovel['valor_venda']:,.2f}"
    )

    folium.Marker(
        location=[
            imovel['latitude'],
            imovel['longitude']
        ],
        popup=folium.Popup(
            popup_texto,
            max_width=300
        ),
        tooltip=f"Imóvel {imovel['id_imovel']}",
        icon=folium.Icon(
            color=cor,
            icon='home',
            prefix='fa'
        )
    ).add_to(cluster)

nome_arquivo = 'mapa_imoveis_baixada.html'

mapa_cluster.save(nome_arquivo)

print(f"Mapa salvo com sucesso em: {nome_arquivo}")

mapa_cluster
