import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import math
import pandas as pd

st.set_page_config(page_title="Relatório Detalhado do Programa: Calculadora de Blocos", page_icon="📊", layout="wide")

# Função para carregar imagens
def carregar_imagem(url, width=150):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img.resize((width, int(img.height * (width / img.width))))
    except (requests.exceptions.RequestException, UnidentifiedImageError) as e:
        st.error(f"Erro ao carregar a imagem: {e}")
        return None

# Função para obter preços médios
def obter_precos():
    return {"custo_bloco": 5.0, "custo_canaleta": 6.0, "custo_argamassa": 300.0}

img_url = "https://www.cronoshare.com.br/blog/wp-content/uploads/2019/02/Quanto-custa-a-construcao-de-um-muro.jpg"
img = carregar_imagem(img_url, width=600)

st.title("Relatório Detalhado do Programa: Calculadora de Blocos")
if img:
    st.image(img, use_column_width=True)

st.header("Informe o tamanho da parede:")
largura_parede = st.number_input("Largura da parede (em metros):", min_value=0.0, step=0.1)
altura_parede = st.number_input("Altura da parede (em metros):", min_value=0.0, step=0.1)
espessura_reboco_cm = st.number_input("Espessura do reboco (em centímetros):", min_value=1.0, max_value=10.0, step=0.1, value=1.5)

blocos = {
    "Bloco estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "quantidade": 0, "imagem": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhsTOAT5hTiZ8dSyQCYxJqhCT0lnBHHcJu1Q&s"},
    "Bloco estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/Veda%C3%A7%C3%A3o-F39-L14-Canaleta-Desenho-t%C3%A9cnico.jpg"},
    "Bloco estrutural 14 x 19 x 44cm": {"largura": 0.44, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/F29-L14-Bloco-44-Desenho-t%C3%A9cnico.jpg"},
    "Bloco estrutural 14 x 19 x 14cm": {"largura": 0.14, "altura": 0.19, "quantidade": 0, "imagem": "https://orcamentor.com/media/insumos/44904.png"}
}

canaletas = {
    "Canaleta estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/F29-L14-Canaleta-Desenho-técnico-1.jpg"},
    "Canaleta estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/Veda%C3%A7%C3%A3o-F39-L14-Canaleta-Desenho-técnico.jpg"}
}

imagem_argamassa = "https://redeconstrulider.com.br/uploads/pagina/elemento/campo/2022/04/Hno9M4VNQBgHgVYJ/09.jpg"

if st.button("Calcular Blocos Necessários"):
    if largura_parede > 0 and altura_parede > 0 and espessura_reboco_cm > 0:
        area_parede = largura_parede * altura_parede
        espessura_reboco_m = espessura_reboco_cm / 100

        for tipo_bloco, dimensoes in blocos.items():
            area_bloco = dimensoes["largura"] * dimensoes["altura"]
            quantidade = math.ceil(area_parede / area_bloco)
            blocos[tipo_bloco]["quantidade"] = quantidade

        for tipo_canaleta, dimensoes in canaletas.items():
            area_canaleta = dimensoes["largura"] * dimensoes["altura"]
            quantidade = math.ceil(area_parede / area_canaleta * 0.1)
            canaletas[tipo_canaleta]["quantidade"] = quantidade

        volume_reboco = area_parede * espessura_reboco_m

        precos = obter_precos()
        custo_bloco = precos["custo_bloco"]
        custo_canaleta = precos["custo_canaleta"]
        custo_argamassa = precos["custo_argamassa"]

        st.header("Resultados:")
        custo_total_blocos = 0
        custo_total_canaletas = 0

        for tipo_bloco, dimensoes in blocos.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(dimensoes["imagem"], width=150)
            with col2:
                st.write(f"{tipo_bloco}: {dimensoes['quantidade']} blocos")
            custo_total_blocos += dimensoes["quantidade"] * custo_bloco

        for tipo_canaleta, dimensoes in canaletas.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(dimensoes["imagem"], width=150)
            with col2:
                st.write(f"{tipo_canaleta}: {dimensoes['quantidade']} canaletas")
            custo_total_canaletas += dimensoes["quantidade"] * custo_canaleta

        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(imagem_argamassa, width=150)
        with col2:
            st.write(f"Argamassa: {volume_reboco:.2f} m³")
        custo_total_argamassa = volume_reboco * custo_argamassa

        # Mostrar resultados totais em forma de tabela
        st.header("💵 Resumo dos Custos")
        resultados = pd.DataFrame({
            "Material": ["Blocos", "Canaletas", "Argamassa", "Total"],
            "Custo Total (R$)": [f"R$ {custo_total_blocos:.2f}", f"R$ {custo_total_canaletas:.2f}", f"R$ {custo_total_argamassa:.2f}", f"R$ {custo_total_blocos + custo_total_canaletas + custo_total_argamassa:.2f}"]
        })

        def highlight_total(row):
            return ['background-color: yellow; color: red; font-weight: bold' if row.name == 3 else '' for _ in row]

        st.table(resultados.style.apply(highlight_total, axis=1))

        # Adicionar link para compra dos materiais
        st.markdown("### [Compre os materiais necessários aqui](https://pavibloco.com.br/)")

# Mensagem de erro para valores inválidos
else:
    st.error("Por favor, insira valores válidos para a largura, altura da parede e espessura do reboco.")

