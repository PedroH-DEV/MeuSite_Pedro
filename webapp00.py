import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Carregando a imagem a partir da URL
url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8aa0IZFQ8QgRXejr2v_YOivOKzpoR80gRu5LBAIsVNnz5Q5PBGCQ1MU_PoSUhvlnEYgE&usqp=CAU"
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
