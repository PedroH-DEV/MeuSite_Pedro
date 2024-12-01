import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import math
import pandas as pd
from fpdf import FPDF

# Configurações gerais do layout e título da página
st.set_page_config(
    page_title="Calculadora de Blocos - UniConstruction",
    page_icon="🏠",
    layout="wide"
)

# Função para carregar imagens a partir de URLs
def carregar_imagem(url, width=150):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se o pedido foi bem-sucedido
        img = Image.open(BytesIO(response.content))
        return img.resize((width, int(img.height * (width / img.width))))
    except (requests.exceptions.RequestException, UnidentifiedImageError) as e:
        st.error(f"Erro ao carregar a imagem: {e}")
        return None

# Função para obter preços médios (simulação)
def obter_precos():
    return {
        "custo_bloco": 5.0,  # R$ por bloco
        "custo_canaleta": 6.0,  # R$ por canaleta
        "custo_argamassa": 300.0  # R$ por m³
    }

# URL da imagem principal
img_url = "https://www.cronoshare.com.br/blog/wp-content/uploads/2019/02/Quanto-custa-a-construcao-de-um-muro.jpg"
img = carregar_imagem(img_url, width=600)

# Título e imagem principal
st.title("🧱 Calculadora de Blocos | UniConstruction")
if img:
    st.image(img, use_column_width=True)

# Entrada de dimensões da parede
st.header("Informe o tamanho da parede:")
largura_parede = st.number_input("Largura da parede (em metros):", min_value=0.0, step=0.1)
altura_parede = st.number_input("Altura da parede (em metros):", min_value=0.0, step=0.1)
espessura_reboco_cm = st.number_input("Espessura do reboco (em centímetros):", min_value=1.0, max_value=10.0, step=0.1, value=1.5)

# Dimensões dos blocos e canaletas
blocos = {
    "Bloco estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "imagem": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhsTOAT5hTiZ8dSyQCYxJqhCT0lnBHHcJu1Q&s"},
    "Bloco estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/Veda%C3%A7%C3%A3o-F39-L14-Canaleta-Desenho-t%C3%A9cnico.jpg"},
    "Bloco estrutural 14 x 19 x 44cm": {"largura": 0.44, "altura": 0.19, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/F29-L14-Bloco-44-Desenho-t%C3%A9cnico.jpg"},
    "Bloco estrutural 14 x 19 x 14cm": {"largura": 0.14, "altura": 0.19, "imagem": "https://orcamentor.com/media/insumos/44904.png"}
}

canaletas = {
    "Canaleta estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/F29-L14-Canaleta-Desenho-t%C3%A9cnico-1.jpg"},
    "Canaleta estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/Veda%C3%A7%C3%A3o-F39-L14-Canaleta-Desenho-t%C3%A9cnico.jpg"}
}

# URL da imagem de argamassa
imagem_argamassa = "https://redeconstrulider.com.br/uploads/pagina/elemento/campo/2022/04/Hno9M4VNQBgHgVYJ/09.jpg"

# Cálculo
if st.button("Calcular Blocos Necessários"):
    if largura_parede > 0 and altura_parede > 0 and espessura_reboco_cm > 0:
        area_parede = largura_parede * altura_parede
        espessura_reboco_m = espessura_reboco_cm / 100

        precos = obter_precos()
        custo_total_blocos = 0
        custo_total_canaletas = 0

        st.header("Resultados:")
        for tipo_bloco, dimensoes in blocos.items():
            area_bloco = dimensoes["largura"] * dimensoes["altura"]
            quantidade = math.ceil(area_parede / area_bloco)
            blocos[tipo_bloco]["quantidade"] = quantidade
            custo_total_blocos += quantidade * precos["custo_bloco"]

            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(dimensoes["imagem"], width=150)
            with col2:
                st.write(f"{tipo_bloco}: {quantidade} blocos")

        for tipo_canaleta, dimensoes in canaletas.items():
            area_canaleta = dimensoes["largura"] * dimensoes["altura"]
            quantidade = math.ceil(area_parede / area_canaleta * 0.1)
            canaletas[tipo_canaleta]["quantidade"] = quantidade
            custo_total_canaletas += quantidade * precos["custo_canaleta"]

            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(dimensoes["imagem"], width=150)
            with col2:
                st.write(f"{tipo_canaleta}: {quantidade} canaletas")

        volume_reboco = area_parede * espessura_reboco_m
        custo_total_argamassa = volume_reboco * precos["custo_argamassa"]

        st.image(imagem_argamassa, width=150)
        st.write(f"Argamassa: {volume_reboco:.2f} m³")

        # Tabela de custos
        resultados = pd.DataFrame({
            "Material": ["Blocos", "Canaletas", "Argamassa", "Total"],
            "Custo Total (R$)": [
                f"R$ {custo_total_blocos:.2f}",
                f"R$ {custo_total_canaletas:.2f}",
                f"R$ {custo_total_argamassa:.2f}",
                f"R$ {custo_total_blocos + custo_total_canaletas + custo_total_argamassa:.2f}"
            ]
        })

        st.table(resultados)

        # Geração do PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório de Custos", ln=1, align="C")
        pdf.ln(10)

        for index, row in resultados.iterrows():
            pdf.cell(200, 10, txt=f"{row['Material']}: {row['Custo Total (R$)']}", ln=1, align="L")

        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        st.download_button(
            label="📄 Baixar PDF",
            data=pdf_output,
            file_name="relatorio_custos.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Por favor, insira valores válidos para a largura, altura da parede e espessura do reboco.")
