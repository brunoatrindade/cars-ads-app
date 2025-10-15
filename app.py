import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# CONFIGURAÇÃO INICIAL DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Dashboard de Anúncios de Carros",
    page_icon="🚗",
    layout="wide"
)

# ==============================
# CABEÇALHO
# ==============================
st.title("🚘 Dashboard de Anúncios de Carros")
st.markdown(
    """
    Explore o dataset de anúncios de carros usados com modelos e valor.  
    Use os **filtros na barra lateral** para personalizar a análise e visualizar os dados de forma interativa.
    """
)
st.divider()

# ==============================
# CARREGAR DADOS
# ==============================


@st.cache_data
def load_data():
    df = pd.read_csv("vehicles_us.csv")
    df.dropna(subset=["price", "odometer", "model_year"], inplace=True)
    df["model_year"] = df["model_year"].astype(int)
    return df


df = load_data()

# ==============================
# SIDEBAR (FILTROS)
# ==============================
st.sidebar.header("🔍 Filtros de Pesquisa")

# Filtros dinâmicos
years = st.sidebar.slider(
    "Ano do modelo",
    int(df["model_year"].min()),
    int(df["model_year"].max()),
    (2010, 2020)
)

price_range = st.sidebar.slider(
    "Faixa de preço ($)",
    int(df["price"].min()),
    int(df["price"].max()),
    (5000, 30000)
)

# Filtragem
filtered_df = df[
    (df["model_year"].between(years[0], years[1])) &
    (df["price"].between(price_range[0], price_range[1]))
]

st.sidebar.markdown("---")
st.sidebar.write(f"**Total de anúncios filtrados:** {len(filtered_df)}")

# ==============================
# VISUALIZAÇÕES
# ==============================
st.subheader("📊 Visualizações Interativas")

# Checkboxes para gráficos
col1, col2 = st.columns(2)

with col1:
    show_hist = st.checkbox("Exibir histograma de preços", value=True)
with col2:
    show_scatter = st.checkbox(
        "Exibir gráfico de dispersão (Preço x Quilometragem)")

# Criar histogramas
if show_hist:
    st.write("### Distribuição de Preços")
    fig_hist = px.histogram(
        filtered_df,
        x="price",
        nbins=40,
        title="Distribuição dos Preços de Carros Filtrados",
        color_discrete_sequence=["#1f77b4"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Criar gráfico de dispersão
if show_scatter:
    st.write("### Relação entre Preço e Quilometragem")
    fig_scatter = px.scatter(
        filtered_df,
        x="odometer",
        y="price",
        color="model_year",
        title="Preço vs Quilometragem (com coloração por ano)",
        color_continuous_scale="Turbo"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ==============================
# EXIBIR TABELA
# ==============================
st.subheader("📋 Dados Filtrados")
st.dataframe(filtered_df.head(30))

# ==============================
# BOTÃO DE DOWNLOAD
# ==============================
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Clique aqui para baixar dados filtrados (CSV)",
    data=csv,
    file_name="filtered_cars.csv",
    mime="text/csv"
)

# ==============================
# RODAPÉ
# ==============================
st.markdown("---")
st.caption("Desenvolvido por Bruno Trindade | Dados de anúncios de carros usados")
