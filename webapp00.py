import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import math

# Configurações gerais do layout e título da página
st.set_page_config(
    page_title="Calculadora de Blocos - UniConstruction",
    page_icon="🏠",
    layout="wide"
)

# Função para carregar imagens a partir de URLs
def carregar_imagem(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se o pedido foi bem-sucedido
        return Image.open(BytesIO(response.content))
    except (requests.exceptions.RequestException, UnidentifiedImageError) as e:
        st.error(f"Erro ao carregar a imagem: {e}")
        return None

# Função para obter preços médios (simulação)
def obter_precos():
    # Simulação de preços médios dos materiais
    return {
        "custo_bloco": 5.0,  # R$ por bloco
        "custo_canaleta": 6.0,  # R$ por canaleta
        "custo_argamassa": 300.0  # R$ por m³
    }

# Imagem principal (URL fornecido)
img_url = "https://fei.edu.br/engenhariadofuturo/images/civilin.jpg"
img = carregar_imagem(img_url)

# Adicionando título e imagem principal
st.title("🧱 Calculadora de Blocos | UniConstruction")
if img:
    st.image(img, use_column_width=True)

# Criando campos de entrada para o cálculo
st.header("Informe o tamanho da parede:")

largura_parede = st.number_input("Largura da parede (em metros):", min_value=0.0, step=0.1)
altura_parede = st.number_input("Altura da parede (em metros):", min_value=0.0, step=0.1)
espessura_reboco_cm = st.number_input("Espessura do reboco (em centímetros):", min_value=1.0, max_value=10.0, step=0.1, value=1.5)

# Dimensões dos blocos e canaletas (em metros)
blocos = {
    "Bloco estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "quantidade": 0, "imagem": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhsTOAT5hTiZ8dSyQCYxJqhCT0lnBHHcJu1Q&s"},
    "Bloco estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/Veda%C3%A7%C3%A3o-F39-L14-Canaleta-Desenho-t%C3%A9cnico.jpg"},
    "Bloco estrutural 14 x 19 x 44cm": {"largura": 0.44, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/F29-L14-Bloco-44-Desenho-t%C3%A9cnico.jpg"},
    "Bloco estrutural 14 x 19 x 14cm": {"largura": 0.14, "altura": 0.19, "quantidade": 0, "imagem": "https://orcamentor.com/media/insumos/44904.png"}
}

canaletas = {
    "Canaleta estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/F29-L14-Canaleta-Desenho-t%C3%A9cnico-1.jpg"},
    "Canaleta estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/Veda%C3%A7%C3%A3o-F39-L14-Canaleta-Desenho-t%C3%A9cnico.jpg"}
}

# Cálculo do número de blocos e canaletas necessários
if st.button("Calcular Blocos Necessários"):
    if largura_parede > 0 and altura_parede > 0 and espessura_reboco_cm > 0:
        area_parede = largura_parede * altura_parede
        espessura_reboco_m = espessura_reboco_cm / 100  # Converter cm para metros

        for tipo_bloco, dimensoes in blocos.items():
            area_bloco = dimensoes["largura"] * dimensoes["altura"]
            quantidade = math.ceil(area_parede / area_bloco)
            blocos[tipo_bloco]["quantidade"] = quantidade

        for tipo_canaleta, dimensoes in canaletas.items():
            area_canaleta = dimensoes["largura"] * dimensoes["altura"]
            quantidade = math.ceil(area_parede / area_canaleta * 0.1)  # Suposição: 10% são canaletas
            canaletas[tipo_canaleta]["quantidade"] = quantidade

        volume_reboco = area_parede * espessura_reboco_m  # Volume de argamassa para reboco

        # Obter preços médios dos materiais
        precos = obter_precos()
        custo_bloco = precos["custo_bloco"]
        custo_canaleta = precos["custo_canaleta"]
        custo_argamassa = precos["custo_argamassa"]

        st.header("Resultados:")
        custo_total_blocos = 0
        custo_total_canaletas = 0

        for tipo_bloco, dimensoes in blocos.items():
            st.write(f"{tipo_bloco}: {dimensoes['quantidade']} blocos")
            st.image(dimensoes["imagem"], caption=tipo_bloco, use_column_width=True)
            custo_total_blocos += dimensoes["quantidade"] * custo_bloco

        for tipo_canaleta, dimensoes in canaletas.items():
            st.write(f"{tipo_canaleta}: {dimensoes['quantidade']} canaletas")
            st.image(dimensoes["imagem"], caption=tipo_canaleta, use_column_width=True)
            custo_total_canaletas += dimensoes["quantidade"] * custo_canaleta

        custo_total_argamassa = volume_reboco * custo_argamassa

        st.write(f"Você precisará de aproximadamente {volume_reboco:.2f} m³ de argamassa para reboco.")
        st.write(f"Custo total dos blocos: R$ {custo_total_blocos:.2f}")
        st.write(f"Custo total das canaletas: R$ {custo_total_canaletas:.2f}")
        st.write(f"Custo total da argamassa: R$ {custo_total_argamassa:.2f}")
        st.write(f"Custo total: R$ {custo_total_blocos + custo_total_canaletas + custo_total_argamassa:.2f}")
    else:
        st.error("Por favor, insira valores válidos para a largura, altura da parede e espessura do reboco.")
