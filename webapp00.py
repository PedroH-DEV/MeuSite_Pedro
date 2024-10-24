import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Carregando a imagem principal a partir da URL
url = "https://santaangelaconstrutora.com.br/wp-content/uploads/2021/07/Implantacao-JB.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# Carregando um GIF animado
gif_url = "https://media.giphy.com/media/J1kHMf6nUktpPsaK9j/giphy.gif"
gif_response = requests.get(gif_url)
gif_bytes = BytesIO(gif_response.content)

# Título
st.title("SANTA ANGELA - LUGAR DE MORAR BEM")

# Cabeçalho
st.header("Essa construtora é D+")

# Subcabeçalho
st.subheader("Notícia: A melhor construtora da América Latina")

# Adicionando a imagem principal ao app
st.image(img, caption='Santa Angela - Excelência em Construção', use_column_width=True)

# Exibindo um GIF animado
st.image(gif_bytes, caption='A evolução nunca para!', use_column_width=True)

# Texto adicional
st.write("Empresa de Sucesso")
