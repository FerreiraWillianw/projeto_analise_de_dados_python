import streamlit as st
import pandas as pd

# 1. Configuração da página do Streamlit (deixa a tela mais larga)
st.set_page_config(layout="wide")

# 2. Título do seu aplicativo web
st.title("📊 Análise de Dados - Amazon Products")
st.markdown("Aqui está a visualização completa e interativa da nossa base de dados.")

# 3. Carregar os dados
caminho_arquivo = 'assets/amazon.csv'
df = pd.read_csv(caminho_arquivo)

# 4. Exibir a tabela interativa na página web (e NÃO no terminal)
st.dataframe(df)