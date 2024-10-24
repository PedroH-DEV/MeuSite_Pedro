# MEU PRIMEIRO WEB APP
import streamlit as st
  
# Use st.title("") para adicionar um TÍTULO ao seu Web app
st.title("SANTA ANGELA - LUGAR DE MORAR BEM")

import requests
from PIL import Image
from io import BytesIO

# URL da imagem
url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRTTIDwib3TUNXUOFc6gCmXQJwtbqFdtNpJpsllc96pVLRvIaGzw_Q8wG-RuvEUqniSoo&usqp=CAU"

# Fazendo a requisição da imagem
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# Exibindo a imagem
img.show()

# Use st.header("") para adicionar um CABEÇALHO ao seu Web app
st.header("Essa construtora é D+")

# Use st.subheader("") para adicionar um SUB CABEÇALHO ao seu Web app
st.subheader("Notícia: A melhor construtira da América Latina")

# Use st.write("") para adicionar um texto ao seu Web app
st.write("Empresa de Sucesso")
