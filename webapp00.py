import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

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

# Imagem principal
img_url = "https://via.placeholder.com/150"  # Use um URL de imagem válido
img = carregar_imagem(img_url)

# Adicionando título e imagem principal
st.title("🧱 Calculadora de Blocos | UniConstruction")
if img:
    st.image(img, use_column_width=True)

# Criando campos de entrada para o cálculo
st.header("Informe o tamanho da parede:")

largura_parede = st.number_input("Largura da parede (em metros):", min_value=0.0, step=0.1)
altura_parede = st.number_input("Altura da parede (em metros):", min_value=0.0, step=0.1)

# Dimensões padrão de um bloco (em metros)
largura_bloco = 0.19  # 19 cm
altura_bloco = 0.09  # 9 cm

# Cálculo do número de blocos necessários
if st.button("Calcular Blocos Necessários"):
    if largura_parede > 0 and altura_parede > 0:
        area_parede = largura_parede * altura_parede
        area_bloco = largura_bloco * altura_bloco
        num_blocos = area_parede / area_bloco
        st.success(f"Você precisará de aproximadamente {num_blocos:.0f} blocos para construir a parede.")
    else:
        st.error("Por favor, insira valores válidos para a largura e altura da parede.")

