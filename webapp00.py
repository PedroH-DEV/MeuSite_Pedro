import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Carregando a imagem a partir da URL
url = "https://cdn-app-privally-io.s3.amazonaws.com/env/suite/images/context/asset/centrals/0003/00002667/darkLogo/20211228211245.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# Título
st.title("SANTA ANGELA - LUGAR DE MORAR BEM")

# Cabeçalho
st.header("Essa construtora é D+")

# Subcabeçalho
st.subheader("Notícia: A melhor construtora da América Latina")

# Adicionando a imagem ao app
st.image(img, caption='Santa Angela - Excelência em Construção', use_column_width=True)

# Texto
st.write("Empresa de Sucesso")
