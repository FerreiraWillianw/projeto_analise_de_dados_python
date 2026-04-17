import pandas as pd
import plotly.express as px

df = pd.read_csv('assets/amazon.csv')

df['discounted_price'] = df['discounted_price'].astype(str).str.replace('₹', '').str.replace(',', '')
df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
df = df.dropna(subset=['discounted_price'])
df = df[df['discounted_price'] > 0]

fig = px.histogram(
    df,
    x='discounted_price',
    nbins=50,
    title='Teste - Borda em Toda a Área do Gráfico',
    template='plotly_dark'
)

# Fundo uniforme
fig.update_layout(
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117'
)

# Adicionar borda ao redor de TODO o gráfico (paper)
fig.update_layout(
    shapes=[dict(
        type="rect",
        xref="paper", yref="paper",
        x0=0, y0=0, x1=1, y1=1,
        line=dict(color="#00FF00", width=2),
        fillcolor="rgba(0,0,0,0)",
        layer="above"
    )]
)

fig.show()