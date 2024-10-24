import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

# Configurações gerais do layout e título da página
st.set_page_config(
    page_title="Santa Angela - Lugar de Morar Bem",
    page_icon="🏠",
    layout="wide"
)

# Função para carregar imagens a partir de URLs
def carregar_imagem(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# Imagem principal
img_url = "https://santaangelaconstrutora.com.br/wp-content/uploads/2021/07/Implantacao-JB.jpg"
img = carregar_imagem(img_url)

# Adicionando título e layout com colunas
st.title("🏢 SANTA ANGELA - LUGAR DE MORAR BEM")

col1, col2 = st.columns([2, 1])
with col1:
    st.image(img, caption='Santa Angela - Excelência em Construção', use_column_width=True)

with col2:
    st.subheader("Essa construtora é D+")
    st.write("""
        A **Santa Angela** é referência no mercado imobiliário, destacando-se pela 
        **qualidade, inovação e compromisso** com seus clientes. A empresa foi premiada 
        como a **melhor construtora da América Latina** e se mantém em constante crescimento.
    """)
    st.button("Saiba mais")

# Adicionando gráfico de exemplo com Matplotlib
st.subheader("Evolução dos Projetos")

fig, ax = plt.subplots()
anos = ["2019", "2020", "2021", "2022", "2023"]
projetos = [5, 8, 12, 15, 20]
ax.plot(anos, projetos, marker='o', linestyle='-', color='#FF6347', linewidth=2)
ax.set_title("Crescimento Anual de Projetos", fontsize=16)
ax.set_xlabel("Ano")
ax.set_ylabel("Número de Projetos")
st.pyplot(fig)

# Rodapé com uma mensagem
st.markdown("---")
st.write("Santa Angela - **Construindo Sonhos** desde 1990.")
