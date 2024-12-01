import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import math
import pandas as pd

# Configurações gerais do layout e título da página
st.set_page_config(
    page_title="UniConstruction",
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

# Tela inicial com opções
def tela_inicial():
    st.title("🏠 Bem-vindo ao UniConstruction!")
    st.subheader("Escolha uma das opções abaixo:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔢 Calculadora de Blocos"):
            st.session_state["pagina"] = "calculadora"
    with col2:
        if st.button("📋 Orçamento Simples"):
            st.session_state["pagina"] = "orcamento_simples"
    with col3:
        if st.button("🛒 Comprar Materiais"):
            st.session_state["pagina"] = "comprar"
    with col4:
        if st.button("📚 Curiosidades"):
            st.session_state["pagina"] = "curiosidades"

# Tela da calculadora de blocos
def tela_calculadora():
    st.title("🧱 Calculadora de Blocos | UniConstruction")
    
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
        "Canaleta estrutural 14 x 19 x 29cm": {"largura": 0.29, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/F29-L14-Canaleta-Desenho-t%C3%A9cnico-1.jpg"},
        "Canaleta estrutural 14 x 19 x 39cm": {"largura": 0.39, "altura": 0.19, "quantidade": 0, "imagem": "https://pavibloco.com.br/wp-content/uploads/2018/01/Veda%C3%A7%C3%A3o-F39-L14-Canaleta-Desenho-t%C3%A9cnico.jpg"}
    }

    imagem_argamassa = "https://redeconstrulider.com.br/uploads/pagina/elemento/campo/2022/04/Hno9M4VNQBgHgVYJ/09.jpg"

    if st.button("Calcular Blocos Necessários"):
        if largura_parede > 0 and altura_parede > 0 and espessura_reboco_cm > 0:
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

            st.header("💵 Resumo dos Custos")
            resultados = pd.DataFrame({
                "Material": ["Blocos", "Canaletas", "Argamassa", "Total"],
                "Custo Total (R$)": [f"R$ {custo_total_blocos:.2f}", f"R$ {custo_total_canaletas:.2f}", f"R$ {custo_total_argamassa:.2f}", f"R$ {custo_total_blocos + custo_total_canaletas + custo_total_argamassa:.2f}"]
            })

            def highlight_total

            # Tela do orçamento simples
def tela_orcamento_simples():
    st.title(" Orçamento Simples")
    # ... (implementar a lógica para um orçamento mais simplificado, talvez com um formulário para o usuário inserir algumas informações básicas)

# Tela de compra de materiais
def tela_comprar():
    st.title(" Comprar Materiais")
    # ... (redirecionar para uma loja online ou fornecer uma lista de fornecedores)

# Tela de curiosidades
def tela_curiosidades():
    st.title(" Curiosidades sobre Construção")
    # ... (exibir textos, imagens ou vídeos sobre temas relacionados à construção)

# Função principal que renderiza a página correta com base no estado da sessão
def main():
    if "pagina" not in st.session_state:
        tela_inicial()
    else:
        pagina = st.session_state["pagina"]
        if pagina == "calculadora":
            tela_calculadora()
        elif pagina == "orcamento_simples":
            tela_orcamento_simples()
        elif pagina == "comprar":
            tela_comprar()
        elif pagina == "curiosidades":
            tela_curiosidades()

if __name__ == "__main__":
    main()
