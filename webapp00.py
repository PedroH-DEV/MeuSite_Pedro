import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import math
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
        "custo_bloco": 5.0,
        "custo_canaleta": 6.0,
        "custo_argamassa": 300.0
    }

# Função para criar PDF
def criar_pdf(resultados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Calculadora de Blocos | UniConstruction", ln=True, align="C")
    pdf.ln(10)

    for index, row in resultados.iterrows():
        pdf.cell(200, 10, txt=f"{row['Material']}: {row['Custo Total (R$)']}", ln=True, align="L")

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Função para enviar e-mail
def enviar_email(destinatario, pdf_anexo):
    remetente = "seu_email@gmail.com"
    senha = "sua_senha"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = "Resumo de Custos - UniConstruction"

    corpo_email = "Segue em anexo o resumo dos custos gerado pela Calculadora de Blocos - UniConstruction."
    msg.attach(MIMEText(corpo_email, 'plain'))

    anexo = MIMEText(pdf_anexo.getvalue(), 'base64', 'utf-8')
    anexo.add_header('Content-Disposition', 'attachment', filename="resumo_custos.pdf")
    msg.attach(anexo)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha)
        texto = msg.as_string()
        server.sendmail(remetente, destinatario, texto)
        server.quit()
        st.success(f"E-mail enviado com sucesso para {destinatario}!")
    except Exception as e:
        st.error(f"Falha ao enviar e-mail: {e}")

# URL da imagem de argamassa
imagem_argamassa = "https://redeconstrulider.com.br/uploads/pagina/elemento/campo/2022/04/Hno9M4VNQBgHgVYJ/09.jpg"

# Parâmetros de entrada
largura_parede = st.number_input("Largura da parede (em metros):", min_value=0.0, step=0.1)
altura_parede = st.number_input("Altura da parede (em metros):", min_value=0.0, step=0.1)
espessura_reboco_cm = st.number_input("Espessura do reboco (em centímetros):", min_value=1.0, max_value=10.0, step=0.1, value=1.5)

# Cálculo do número de blocos e canaletas necessários
if st.button("Calcular Blocos Necessários"):
    if largura_parede > 0 and altura_parede > 0 and espessura_reboco_cm > 0:
        area_parede = largura_parede * altura_parede
        espessura_reboco_m = espessura_reboco_cm / 100

        blocos = {
            "Bloco estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "quantidade": 0, "imagem": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhsTOAT5hTiZ8dSyQCYxJqhCT0lnBHHcJu1Q&s"},
            "Bloco estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/Veda%C3%A7%C3%A3o-F39-L14-Canaleta-Desenho-t%C3%A9cnico.jpg"},
            "Bloco estrutural 14 x 19 x 44cm": {"largura": 0.44, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/F29-L14-Bloco-44-Desenho-t%C3%A9cnico.jpg"},
            "Bloco estrutural 14 x 19 x 14cm": {"largura": 0.14, "altura": 0.19, "quantidade": 0, "imagem": "https://orcamentor.com/media/insumos/44904.png"}
        }

        canaletas = {
            "Canaleta estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/F29-L14-Canaleta-Desenho-t%C3%A9cnico-1.jpg"},
            "Canaleta estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/Veda%C3%A7%C3%A3o-F39-L14-Canaleta-Desenho-t%C3%A9cnico.jpg"}
        }

        volume_reboco = area_parede * espessura_reboco_m
        precos = obter_precos()
        custo_bloco = precos["custo_bloco"]
        custo_canaleta = precos["custo_canaleta"]
        custo_argamassa = precos["custo_argamassa"]

        st.header("Resultados:")
        custo_total_blocos = 0
        custo_total_canaletas = 0

        for tipo_bloco, dimensoes in blocos.items():
            area_bloco = dimensoes["largura"] * dimensoes["altura"]
            quantidade = math.ceil(area_parede / area_bloco)
            blocos[tipo_bloco]["quantidade"] = quantidade
            custo_total_blocos += quantidade * custo_bloco
            st.image(dimensoes["imagem"], width=150)
            st.write(f"{tipo_bloco}: {quantidade} blocos")

        for tipo_canaleta, dimensoes in canaletas.items():
            area_canaleta = dimensoes["largura"] * dimensoes["altura"]
            quantidade = math.ceil(area_parede / area_canaleta * 0.1)
            canaletas[tipo_canaleta]["quantidade"] = quantidade
            custo_total_canaletas += quantidade * custo_canaleta
            st.image(dimensoes["imagem"], width=150)
            st.write(f"{tipo_canaleta}: {quantidade} canaletas")

        st.image(imagem_argamassa, width=150)
        st.write(f"Argamassa: {volume_reboco:.2f} m³")
        custo_total_argamassa = volume_reboco * custo_argamassa

        resultados = pd.DataFrame({
            "Material": ["Blocos", "Canaletas", "Argamassa", "Total"],
            "Custo Total (R$)": [
                f"R$ {custo_total_blocos:.2f}",
                f"R$ {custo_total_canaletas:.2f}",
                f"R$ {custo_total_argamassa:.2f}",
                f"R$ {custo_total_blocos + custo_total_canaletas + custo_total_argamassa:.2f}"
            ]
        })

        def highlight_total(row):
            return ['background-color: yellow; color: red; font-weight: bold' if row.name == 3 else '' for _ in row]

        st.table(resultados.style.apply(highlight_total, axis=1))
        pdf_file = criar_pdf(resultados)
        st.download_button(
            label="📄 Baixar PDF",
            data=pdf_file,
            file_name="resumo_custos.pdf",
            mime="application/pdf"
        )

        # Adicionar campo de e-mail e botão para enviar
st.header("📧 Enviar Resumo por E-mail")
email = st.text_input("Digite seu e-mail:")

if st.button("Enviar E-mail"):
    if email:
        enviar_email(email, pdf_file)
    else:
        st.error("Por favor, insira um e-mail válido.")

# Adicionar link para compra dos materiais
st.markdown("### [Compre os materiais necessários aqui](https://pavibloco.com.br/)")
