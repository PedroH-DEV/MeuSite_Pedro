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

# Imagem principal (URL de uma imagem melhorada)
img_url = "https://via.placeholder.com/600x400.png?text=UniConstruction"  # Use um URL de imagem válido e melhorado
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
blocos = {
    "Bloco de Concreto": {"largura": 0.20, "altura": 0.10},
    "Bloco Cerâmico": {"largura": 0.19, "altura": 0.09}
}

# Cálculo do número de blocos necessários
if st.button("Calcular Blocos Necessários"):
    if largura_parede > 0 and altura_parede > 0:
        area_parede = largura_parede * altura_parede
        st.header("Resultados:")
        
        for tipo_bloco, dimensoes in blocos.items():
            area_bloco = dimensoes["largura"] * dimensoes["altura"]
            num_blocos = area_parede / area_bloco
            st.write(f"Você precisará de aproximadamente {num_blocos:.0f} {tipo_bloco.lower()}s para construir a parede.")
    else:
        st.error("Por favor, insira valores válidos para a largura e altura da parede.")
