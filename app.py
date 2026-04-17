import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import re

# Configuração da página
st.set_page_config(
    page_title="Dashboard Amazon Eletrônicos",
    page_icon="📊",
    layout="wide"
)

# =====================================
# TEMA (CLARO / ESCURO)
# =====================================

if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

def toogle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# Sidebar com toggle de tema
with st.sidebar:
    st.button("Alterar Tema", on_click=toogle_theme)
    st.markdown("---")

# Aplicar tema baseado na escolha do usuário
if st.session_state.theme == 'dark':
    primary_color = "#00FF00" # Verde Vibrante
    bg_color = "#0E1117" # Preto Profundo
    text_color = "#FFFFFF" # Branco Puro
else:
    primary_color = "#FF4B4B" # Vermelho Vibrante
    bg_color = "#FFFFFF" # Branco Puro
    text_color = "#000000" # Preto Puro


# =========================================
# CARREGAR DADOS (cache para performance)
# =========================================

@st.cache_data
def load_data():
    df = pd.read_csv('.assets/amazon.csv')
    # Limpeza básica
    # (vamos adicionar depois)
    return df

df = load_data()

# =========================================
# FILTROS LATERAIS
# =========================================

with st.sidebar:
    st.header("🔍 Filtros")

    # Filtro por categoria
    categorias = sorted(df['category'].unique())
    selected_categories = st.multiselect(
        "Categorias",
        categorias,
        default=categorias[:5] if len(categorias) > 5 else categorias
    )

    # Filtro por rating mínimo
    min_rating = st.slider("Rating mínimo", 0.0, 5.0, 3.0, 0.1)

    # Filtro por preço máximo
    max_price = st.slider("Preço máximo (₹)", 0, 50000, 50000, 1000)

    st.markdown("---")
    st.caption(f"Dados: Amazon India | Produtos: {len(df):,}")

# Aplicar filtros
df_filtered = df[
    (df['category'].isin(selected_categories)) &
    (df['rating'] >= min_rating) &
    (df['discounted_price'] <= max_price)
]

# =========================================
# TÍTULO PRINCIPAL
# =========================================
st.title("📊 Análise de Produtos Eletrônicos - Amazon India")
st.markdown(f"<small>Produtos analisados: {len(df_filtered):,} | Tema: {st.session_state.theme}</small>", unsafe_allow_html=True)
st.markdown("---")

# =========================================
# ABAS
# =========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Visão Geral",
    "⭐ Análise de Avaliações",
    "📂 Análise por Categoria",
    "💬 Análise de Sentimentos (Reviews)"
])

with tab1:
    st.header("Visão Geral do Dataset")
    st.info("Aqui virão os KPIs e gráficos principais. Vamos preencher no próximo passo.")

with tab2:
    st.header("Relação entre Preço e Avaliações")
    st.info("Gráfico de dispersão e correlação entre preço e rating.")

with tab3:
    st.header("Performance por Categoria")
    st.info("Métricas agregadas por categoria.")

with tab4:
    st.header("Análise de Sentimentos dos Reviews")
    st.info("Nuvem de palavras e análise de texto das avaliações.")

# Rodapé
st.markdown("---")
st.caption("Dashboard desenvolvido por Willian Ferreira com Streamlit | Dados: Amazon India")