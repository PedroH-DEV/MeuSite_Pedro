import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import math
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pdfkit

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
    # Simulação de preços médios dos materiais
    return {
        "custo_bloco": 5.0,  # R$ por bloco
        "custo_canaleta": 6.0,  # R$ por canaleta
        "custo_argamassa": 300.0  # R$ por m³
    }

# Função para criar PDF usando HTML e CSS
def criar_pdf_html(resultados):
    html_content = """
    <html>
    <head>
    <style>
    body { font-family: Arial, sans-serif; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid black; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; }
    .total { background-color: yellow; color: red; font-weight: bold; }
    </style>
    </head>
    <body>
    <h1>Calculadora de Blocos | UniConstruction</h1>
    <h2>Resumo dos Custos</h2>
    <table>
      <tr>
        <th>Material</th>
        <th>Custo Total (R$)</th>
      </tr>
    """
    
    for index, row in resultados.iterrows():
        class_name = "total" if index == 3 else ""
        html_content += f"""
        <tr class="{class_name}">
          <td>{row['Material']}</td>
          <td>{row['Custo Total (R$)']}</td>
        </tr>
        """
    
    html_content += """
    </table>
    </body>
    </html>
    """
    
    pdf_output = BytesIO()
    pdfkit.from_string(html_content, pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Função para enviar e-mail
def enviar_email(destinatario, pdf_anexo, assunto="Resumo de Custos - UniConstruction"):
    remetente = "seu_email@gmail.com"
    senha = "sua_senha"  # Use uma senha de app gerada para sua conta Google para maior segurança

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

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

# Cálculo do número de blocos e canaletas necessários
if st.button("Calcular Blocos Necessários"):
    if largura_parede > 0 and altura_parede > 0 e espessura_reboco_cm > 0:
        area_parede = largura_parede * altura_parede
        espessura_reboco_m = espessura_reboco_cm / 100  # Converter cm para metros

        for tipo_bloco, dimensoes in blocos.items():
            area_bloco = dimensoes["largura"] * dimensoes["altura"]
            quantidade = math.ceil(area_parede / area_bloco)
            blocos[tipo_bloco]["quantidade"] = quantidade

        for tipo_canaleta, dimensoes in canaletas.items():
            area_canaleta = dimensoes["largura"] * dimensoes["altura"]
            quantidade = math.ceil(area_parede / area_canaleta * 0.1)  # Suposição: 10% são canaletas
            canaletas[tipo_canaleta]["quantidade"] = quantidade

        volume_reboco = area_parede * espessura_reboco_m  # Volume de argamassa para reboco

        # Obter preços médios dos materiais
        precos = obter_precos()
        custo_bloco = precos["custo_bloco"]
        custo_canaleta = precos["custo_canaleta"]
        custo_argamassa = precos["custo_argamassa"]

        st.header("Resultados:")
        custo_total_blocos = 0
        custo_total_canaletas = 0

        # Exibir imagens e quantidades lado a lado
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

        # Exibir resultado da argamassa lado a lado com a imagem
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
            "Custo Total (R$)": [
                f"R$ {custo_total_blocos:.2f}",
                f"R$ {custo_total_canaletas:.2f}",
                f"R$ {custo_total_argamassa:.2f}",
                f"R$ {custo_total_blocos + custo_total_canaletas + custo_total_argamassa:.2f}"
            ]
        })

        # Estilizar a última linha (Total) em amarelo com texto vermelho
        def highlight_total(row):
            return ['background-color: yellow; color: red; font-weight: bold' if row.name == 3 else '' for _ in row]

        st.table(resultados.style.apply(highlight_total, axis=1))

        # Criar PDF e adicionar botão para download
        pdf_file = criar_pdf_html(resultados)
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

    else:
        st.error("Por favor, insira valores válidos para a largura, altura da parede e espessura do reboco.")
