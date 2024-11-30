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

# Dimensões dos blocos (em metros)
bloco_concreto = {"largura": 0.20, "altura": 0.10}
canaleta_concreto = {"largura": 0.20, "altura": 0.10}

# Cálculo do número de blocos e canaletas necessários
if st.button("Calcular Blocos Necessários"):
    if largura_parede > 0 and altura_parede > 0:
        area_parede = largura_parede * altura_parede
        num_blocos = math.ceil(area_parede / (bloco_concreto["largura"] * bloco_concreto["altura"]))
        num_canaletas = math.ceil(area_parede / (canaleta_concreto["largura"] * canaleta_concreto["altura"]) * 0.1)  # Suposição: 10% são canaletas
        quantidade_argamassa = area_parede * 0.02  # Aproximadamente 0,02 m³ de argamassa por m² de parede
        
        st.header("Resultados:")
        st.write(f"Você precisará de aproximadamente {num_blocos} blocos de concreto (0.20m x 0.10m) para construir a parede.")
        st.write(f"Você precisará de aproximadamente {num_canaletas} canaletas de concreto.")
        st.write(f"Você precisará de aproximadamente {quantidade_argamassa:.2f} m³ de argamassa para reboco.")
        st.write(f"Resistência dos blocos: Blocos de concreto padrão possuem uma resistência de 6 a 10 MPa.")
    else:
        st.error("Por favor, insira valores válidos para a largura e altura da parede.")

