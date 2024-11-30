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
espessura_reboco_cm = st.number_input("Espessura do reboco (em centímetros):", min_value=1, max_value=10, step=1, value=1.5)

# Custo médio dos materiais
custo_bloco = st.number_input("Custo médio por bloco (em R$):", min_value=0.0, step=0.1)
custo_canaleta = st.number_input("Custo médio por canaleta (em R$):", min_value=0.0, step=0.1)
custo_argamassa = st.number_input("Custo médio por m³ de argamassa (em R$):", min_value=0.0, step=0.1)

# Dimensões dos blocos e canaletas (em metros)
blocos = {
    "Bloco estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "quantidade": 0},
    "Bloco estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "quantidade": 0},
    "Bloco estrutural 14 x 19 x 34cm": {"largura": 0.34, "altura": 0.19, "quantidade": 0},
    "Bloco estrutural 14 x 19 x 44cm": {"largura": 0.44, "altura": 0.19, "quantidade": 0},
    "Bloco estrutural 14 x 19 x 14cm": {"largura": 0.14, "altura": 0.19, "quantidade": 0},
    "Bloco estrutural 14 x 19 x 19cm": {"largura": 0.19, "altura": 0.19, "quantidade": 0}
}

canaletas = {
    "Canaleta estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "quantidade": 0},
    "Canaleta estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "quantidade": 0}
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
        
        st.header("Resultados:")
        custo_total_blocos = 0
        custo_total_canaletas = 0
        
        for tipo_bloco, dimensoes in blocos.items():
            st.write(f"{tipo_bloco}: {dimensoes['quantidade']} blocos")
            custo_total_blocos += dimensoes["quantidade"] * custo_bloco
        
        for tipo_canaleta, dimensoes in canaletas.items():
            st.write(f"{tipo_canaleta}: {dimensoes['quantidade']} canaletas")
            custo_total_canaletas += dimensoes["quantidade"] * custo_canaleta
        
        custo_total_argamassa = volume_reboco * custo_argamassa
        
        st.write(f"Você precisará de aproximadamente {volume_reboco:.2f} m³ de argamassa para reboco.")
        st.write(f"Custo total dos blocos: R$ {custo_total_blocos:.2f}")
        st.write(f"Custo total das canaletas: R$ {custo_total_canaletas:.2f}")
        st.write(f"Custo total da argamassa: R$ {custo_total_argamassa:.2f}")
        st.write(f"Custo total: R$ {custo_total_blocos + custo_total_canaletas + custo_total_argamassa:.2f}")
    else:
        st.error("Por favor, insira valores válidos para a largura, altura da parede e espessura do reboco.")
