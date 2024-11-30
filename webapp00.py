import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import datetime

# Configurações gerais do layout e título da página
st.set_page_config(
    page_title="Cadastro de visitantes - UniConstruction",
    page_icon="🏠",
    layout="wide"
)

# Função para carregar imagens a partir de URLs
def carregar_imagem(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# Imagem principal
img_url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fbraverengenharia.com%2Fmateriais-mais-usados-na-engenharia-civil%2F&psig=AOvVaw0qo36BK05TC5Fsn2KdTTCH&ust=1733081763055000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCPihofDmhIoDFQAAAAAdAAAAABAE"
img = carregar_imagem(img_url)

# Adicionando título e imagem principal
st.title("👷🏼‍♂️ Quer visitar nossa obra? | Realize seu cadastro:")
st.image(img, use_column_width=True)

# Criando campos de cadastro
st.header("Preencha o formulário abaixo:")

nome_completo = st.text_input("Nome completo")
email = st.text_input("E-mail")
telefone = st.text_input("Telefone")
data_visita = st.date_input("Data que gostaria", datetime.date.today())
cargo = st.text_input("Cargo")
empresa = st.text_input("Empresa")

# Botão de submissão
if st.button("Enviar Cadastro"):
    st.success(f"Cadastro realizado com sucesso!\n\n"
               f"Nome completo: {nome_completo}\n"
               f"E-mail: {email}\n"
               f"Telefone: {telefone}\n"
               f"Data da visita: {data_visita}\n"
               f"Cargo: {cargo}\n"
               f"Empresa: {empresa}")
