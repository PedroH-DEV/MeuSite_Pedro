import streamlit as st

# Configurações gerais do layout e título da página
st.set_page_config(
    page_title="Calculadora de Blocos - UniConstruction",
    page_icon="🏠",
    layout="centered"
)

# Título do site
st.title("Calculadora de Blocos | UniConstruction")

# Introdução
st.header("Introdução")
st.write("""
Bem-vindo à Calculadora de Blocos da UniConstruction! Este programa foi desenvolvido para ajudá-lo a calcular os materiais necessários para a construção de uma parede, incluindo blocos estruturais, canaletas e argamassa. A ferramenta fornece uma estimativa de custos e permite uma visualização detalhada dos resultados.
""")

# Bibliotecas Utilizadas
st.header("Bibliotecas Utilizadas")
st.write("""
Este programa foi desenvolvido utilizando as seguintes bibliotecas Python:
- **Streamlit**: Para criar a interface web interativa.
- **PIL (Python Imaging Library)**: Para manipulação e exibição de imagens.
- **Requests**: Para carregar imagens a partir de URLs.
- **BytesIO**: Para manipulação de dados em memória.
- **Math**: Para cálculos matemáticos.
- **Pandas**: Para manipulação e exibição de dados tabulares.
""")

# Funcionalidades do Programa
st.header("Funcionalidades do Programa")
st.write("""
O programa possui as seguintes funcionalidades:
- **Carregamento de Imagem**: Carrega e redimensiona imagens a partir de URLs.
- **Obtenção de Preços**: Retorna um dicionário com os preços médios dos materiais.
- **Campos de Entrada**: Permite inserir as dimensões da parede.
- **Cálculo de Materiais**: Calcula a quantidade necessária de blocos, canaletas e argamassa.
- **Visualização dos Resultados**: Exibe os resultados em uma tabela detalhada, incluindo imagens ilustrativas.
""")

# Exibição de Imagem Principal
st.header("Exibição de Imagem Principal")
img_url = "https://www.cronoshare.com.br/blog/wp-content/uploads/2019/02/Quanto-custa-a-construcao-de-um-muro.jpg"
st.image(img_url, caption="Imagem de exemplo de uma parede", use_column_width=True)

# Como Utilizar
st.header("Como Utilizar")
st.write("""
1. **Informe o Tamanho da Parede**: Insira a largura e altura da parede em metros, e a espessura do reboco em centímetros.
2. **Calcular Blocos Necessários**: Clique no botão "Calcular Blocos Necessários" para calcular a quantidade de materiais.
3. **Visualização dos Resultados**: Veja os resultados detalhados na tabela, incluindo a quantidade de blocos, canaletas e argamassa necessárias, bem como os custos totais.
""")

# Conclusão
st.header("Conclusão")
st.write("""
A Calculadora de Blocos da UniConstruction é uma ferramenta prática e eficiente para planejar a construção de paredes. Ela ajuda a determinar com precisão os materiais necessários, economizando tempo e recursos. Experimente nossa ferramenta e veja como ela pode facilitar o seu projeto de construção!
""")

# Rodapé
st.write("© 2024 UniConstruction. Todos os direitos reservados.")
