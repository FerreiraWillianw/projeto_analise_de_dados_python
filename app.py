import streamlit as st
import pandas as pd

# =========================================================================
# 1. CONFIGURAÇÃO DA PÁGINA DO STREAMLIT
# =========================================================================
# Deixa o layout do app aproveitando toda a largura da tela do monitor
st.set_page_config(
    page_title="Dashboard Amazon",
    page_icon="📊",
    layout="wide"
)

# Título principal do aplicativo na página web
st.title("📊 Dashboard de Análise de Vendas - Amazon")
st.markdown("Uma análise interativa sobre produtos, preços, descontos e avaliações.")
st.markdown("---") # Cria uma linha divisória elegante na tela

# =========================================================================
# 2. CARREGAMENTO E LIMPEZA DOS DADOS (Nosso motor)
# =========================================================================
# Carrega o arquivo original
caminho_arquivo = 'assets/amazon.csv'
df = pd.read_csv(caminho_arquivo)

# Aplica as limpezas que desenvolvemos juntos:
# Categoria
df['category_limpa'] = df['category'].str.split('|').str[0]
traducao_categorias = {
    'Computers&Accessories': 'Computadores e Acessórios',
    'Electronics': 'Eletrónicos',
    'Home&Kitchen': 'Casa e Cozinha',
    'OfficeProducts': 'Produtos de Escritório',
    'MusicalInstruments': 'Instrumentos Musicais',
    'HomeImprovement': 'Bricolage e Ferramentas',
    'Toys&Games': 'Brinquedos e Jogos',
    'Car&Motorbike': 'Automóvel e Moto',
    'Health&PersonalCare': 'Saúde e Cuidados Pessoais'
}
df['category_limpa'] = df['category_limpa'].map(traducao_categorias).fillna(df['category_limpa'])

# Preços
df['actual_price'] = df['actual_price'].str.replace('₹', '').str.replace(',', '').astype(float)
df['discounted_price'] = df['discounted_price'].str.replace('₹', '').str.replace(',', '').astype(float)

# Avaliações
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating_count'] = df['rating_count'].str.replace(',', '')
df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')

# Filtro final e remoção de nulos
colunas_finais = ['product_name', 'category_limpa', 'actual_price', 'discounted_price', 'rating', 'rating_count']
df_limpo = df[colunas_finais].dropna()

# =========================================================================
# 3. EXIBIÇÃO DA TABELA TRATADA (Agora oculta por um botão)
# =========================================================================

# Criamos o botão e salvamos o estado dele em uma condição 'if'
if st.button("🔍 Ver tabela de dados tratados"):
    # Tudo o que estiver identado (com quatro espaços para a direita) 
    # dentro deste 'if' só vai aparecer quando o botão for clicado.
    st.subheader("📋 Visualização dos Dados Tratados")
    st.markdown("Abaixo você pode ordenar, rolar e inspecionar a base de dados já limpa e traduzida:")
    
    # Exibe a tabela interativa
    st.dataframe(df_limpo, use_container_width=True)

# =========================================================================
# 4. CALCULO DOS INDICADORES (KPIs)
# =========================================================================

# Calculo dos valores
total_produtos = len(df_limpo)
preco_medio = df_limpo['discounted_price'].mean()
nota_media = df_limpo['rating'].mean()

# Criaremos 3 colunas para apresentar os dados
col1, col2, col3 = st.columns(3)

# =========================================================================
# 5. EXIBIÇÃO DOS CARTÕES (KPIs)
# =========================================================================

# Coluna 1: Total de Produtos
with col1:
    st.metric(label="Total de Produtos Analisados", value=total_produtos)

# Coluna 2: Preço Médio (formatado com o símbolo da moeda indiana)
with col2:
    st.metric(label="Preço Médio (Com Desconto)", value=f"₹ {preco_medio:.2f}")

# Coluna 3: Nota Média Geral
with col3:
    st.metric(label="Nota Média Geral", value=f"{nota_media:.2f} / 5.0")

# =========================================================================
# 6. ANÁLISE DE PRODUTOS POR CATEGORIA (Gráfico de Impacto)
# =========================================================================
st.markdown("### 📈 Quantidade de Produtos por Categoria")

# Agrupamos e contamos os produtos por categoria, ordenando do maior para o menor
produtos_por_categoria = df_limpo['category_limpa'].value_counts().reset_index()
# Renomeamos as colunas para o gráfico entender corretamente
produtos_por_categoria.columns = ['Categoria', 'Quantidade']

# Criamos o gráfico de barras usando o Plotly
import plotly.express as px

fig_produtos = px.bar(
    produtos_por_categoria,
    x='Quantidade',
    y='Categoria',
    orientation='h',
    title="Total de Produtos Listados por Categoria Principal",
    labels={'Quantidade': 'Número de Produtos', 'Categoria': 'Categoria'},
    # Usamos o template escuro do Plotly para os textos do gráfico ficarem brancos automaticamente
    template='plotly_dark', 
    color='Quantidade',
    # Criamos um degradê que vai do cinza escuro do cartão até o Laranja Amazon
    color_continuous_scale=['#1F2633', '#FF9900'] 
)

# Esse comando extra serve para garantir que o fundo interno do gráfico fique transparente, 
# misturando-se perfeitamente com o fundo escuro do seu aplicativo do Streamlit
fig_produtos.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# Ajustamos o layout para o gráfico ficar ordenado corretamente
fig_produtos.update_layout(yaxis={'categoryorder': 'total ascending'})

# Exibimos o gráfico na página do Streamlit
st.plotly_chart(fig_produtos, use_container_width=True)

# =========================================================================
# 7. ANÁLISE DE PREÇOS E DESCONTOS POR CATEGORIA (Novo Gráfico)
# =========================================================================
st.markdown("### 💰 Comparativo de Preços Médios por Categoria")

# Agrupamos por categoria e calculamos a média do preço atual e preço com desconto
precos_por_categoria = df_limpo.groupby('category_limpa')[['actual_price', 'discounted_price']].mean().reset_index()

# Criamos o gráfico de barras comparativas (agrupadas)
fig_precos = px.bar(
    precos_por_categoria,
    x='category_limpa',
    y=['actual_price', 'discounted_price'],
    barmode='group', # Coloca as barras de uma mesma categoria lado a lado
    title="Preço Original Médio vs. Preço com Desconto Médio",
    labels={
        'category_limpa': 'Categoria', 
        'value': 'Preço Médio (₹)', 
        'variable': 'Tipo de Preço'
    },
    template='plotly_white',
    # Customizamos as cores: Azul escuro para preço cheio, Laranja/Ouro para desconto (padrão Amazon)
    color_discrete_map={
        'actual_price': '#141923',
        'discounted_price': '#FF9900'
    }
)

# Ajustamos os nomes das legendas para o usuário final ler em português
fig_precos.for_each_trace(lambda t: t.update(name='Preço Original' if t.name == 'actual_price' else 'Preço com Desconto'))

# Exibimos o gráfico na página
st.plotly_chart(fig_precos, use_container_width=True)

# =========================================================================
# 8. RELAÇÃO ENTRE PREÇO E NOTA DOS PRODUTOS (Gráfico de Dispersão)
# =========================================================================
st.markdown("### 🎯 Relação entre Preço, Avaliação e Popularidade")

# Criamos o gráfico de dispersão usando o Plotly Express
fig_dispersao = px.scatter(
    df_limpo,
    x='discounted_price',
    y='rating',
    size='rating_count', # Tamanho do ponto varia conforme o número de avaliações
    color='category_limpa', # Cor do ponto varia conforme a categoria
    title="Distribuição dos Produtos por Preço Atual (₹) vs. Nota Média",
    labels={
        'discounted_price': 'Preço com Desconto (₹)',
        'rating': 'Nota do Produto (0 a 5)',
        'category_limpa': 'Categoria',
        'rating_count': 'Total de Avaliações'
    },
    template='plotly_white',
    hover_name='product_name', # Mostra o nome do produto ao passar o rato por cima
    size_max=50 # Limita o tamanho máximo do ponto para não cobrir o gráfico todo
)

# Exibimos o gráfico na tela
st.plotly_chart(fig_dispersao, use_container_width=True)

# =========================================================================
# 9. TOP 10 PRODUTOS MAIS AVALIADOS (Os Campeões de Vendas)
# =========================================================================
st.markdown("### 🏆 Top 10 Produtos Mais Populares da Amazon")

# 1. Filtramos os 10 produtos com maior número de avaliações
top_10_populares = df_limpo.nlargest(10, 'rating_count').copy()

# 2. Truque de limpeza: Encurtamos o nome do produto para o gráfico ficar bonito
top_10_populares['nome_curto'] = top_10_populares['product_name'].str.slice(0, 40) + "..."

# 3. Criamos o gráfico de barras horizontais para os campeões
fig_top10 = px.bar(
    top_10_populares,
    x='rating_count',
    y='nome_curto',
    orientation='h',
    title="Produtos com o Maior Número Total de Avaliações",
    labels={
        'rating_count': 'Total de Avaliações',
        'nome_curto': 'Produto'
    },
    template='plotly_white',
    color='rating_count', # Intensidade da cor varia com o número de avaliações
    color_continuous_scale='Oranges', # Tom alaranjado para dar destaque de pódio
    hover_name='product_name' # Se passar o mouse, ainda mostra o nome completo original!
)

# Ajustamos para o produto número 1 ficar no topo do gráfico
fig_top10.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)

# Exibimos o gráfico no Streamlit
st.plotly_chart(fig_top10, use_container_width=True)