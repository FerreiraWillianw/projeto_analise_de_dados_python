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
# TEMA (FIXO - ESCURO)
# =====================================

primary_color = "#00FF00"
bg_color = "#0E1117"
text_color = "#FFFFFF"
plotly_template = "plotly_dark"

# CSS mínimo para o slider
st.markdown("""
    <style>
    input[type="range"] {
        accent-color: #00FF00 !important;
    }
    .stSlider label {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================
# CARREGAR DADOS
# =========================================

@st.cache_data
def load_data():
    df = pd.read_csv('assets/amazon.csv')
    
    # Extrair apenas a categoria principal
    df['category'] = df['category'].astype(str).str.split('|').str[0]
    
    # Limpar rating
    df['rating'] = df['rating'].astype(str).str.split(',').str[0]
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    # Limpar rating_count
    df['rating_count'] = df['rating_count'].astype(str).str.replace(',', '')
    df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')
    df = df.dropna(subset=['rating_count'])

    # Limpar discounted_price
    df['discounted_price'] = df['discounted_price'].astype(str)
    df['discounted_price'] = df['discounted_price'].str.replace('â‚¹', '')
    df['discounted_price'] = df['discounted_price'].str.replace('₹', '')
    df['discounted_price'] = df['discounted_price'].str.replace(',', '')
    df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')

    # Limpar actual_price
    df['actual_price'] = df['actual_price'].astype(str)
    df['actual_price'] = df['actual_price'].str.replace('â‚¹', '')
    df['actual_price'] = df['actual_price'].str.replace('₹', '')
    df['actual_price'] = df['actual_price'].str.replace(',', '')
    df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')

    # Limpar discount_percentage
    df['discount_percentage'] = df['discount_percentage'].astype(str).str.replace('%', '')
    df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')

    # Remover linhas com valores nulos
    df = df.dropna(subset=['rating', 'discounted_price', 'product_name', 'category'])

    # Garantir que rating esteja entre 0 e 5
    df = df[df['rating'] <= 5]

    # Remover preços negativos ou zero
    df = df[df['discounted_price'] > 0]

    return df

df = load_data()

# =========================================
# FILTROS
# =========================================

with st.sidebar:
    st.header("🔍 Filtros")

    categorias = sorted(df['category'].unique())
    selected_categories = st.multiselect(
        "Categorias",
        categorias,
        default=categorias[:5] if len(categorias) > 5 else categorias
    )

    min_rating = st.slider("⭐ Rating mínimo", 0.0, 5.0, 3.0, 0.1)
    
    min_preco = int(df['discounted_price'].min())
    max_preco = int(df['discounted_price'].max())
    
    max_price = st.slider(
        "💰 Preço máximo (₹)",
        min_value=min_preco,
        max_value=max_preco,
        value=max_preco,
        step=500
    )

    st.markdown("---")
    st.caption(f"Dados: Amazon India | Produtos: {len(df):,}")

# Aplicar filtros
df_filtered = df[
    (df['category'].isin(selected_categories)) &
    (df['rating'] >= min_rating) &
    (df['discounted_price'] <= max_price)
]

# =========================================
# TÍTULO
# =========================================
st.title("📊 Análise de Produtos Eletrônicos - Amazon India")
st.markdown(f"<small>Produtos analisados: {len(df_filtered):,}</small>", unsafe_allow_html=True)
st.markdown("---")

# =========================================
# ABAS (AGUARDANDO GRÁFICOS)
# =========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Visão Geral",
    "⭐ Análise de Avaliações",
    "📂 Análise por Categoria",
    "💬 Análise de Sentimentos (Reviews)"
])

with tab1:
    st.header("Visão Geral do Dataset")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Total de Produtos", f"{len(df_filtered):,}")
    with col2:
        st.metric("⭐ Rating Médio", f"{df_filtered['rating'].mean():.1f}")
    with col3:
        st.metric("💰 Preço Médio", f"₹{df_filtered['discounted_price'].mean():,.0f}")
    with col4:
        st.metric("🎯 Desconto Médio", f"{df_filtered['discount_percentage'].mean():.0f}%")
    
    st.markdown("---")
    st.info("📊 Gráficos serão adicionados em breve.")

with tab2:
    st.header("Relação entre Preço e Avaliações")
    st.info("📊 Gráficos serão adicionados em breve.")

with tab3:
    st.header("Performance por Categoria")
    st.info("📊 Gráficos serão adicionados em breve.")

with tab4:
    st.header("Análise de Sentimentos das Reviews")
    st.info("📊 Gráficos serão adicionados em breve.")

# Rodapé
st.markdown("---")
st.caption("Dashboard desenvolvido por Willian Ferreira | Dados: Amazon India")