import pandas as pd
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

dados = "https://raw.githubusercontent.com/HeitorMancin/PrototipoSAC/refs/heads/main/DF.xlsx"
df = pd.read_excel(dados)

st.set_page_config(layout="wide")

# Sidebar
with st.sidebar:
    st.header("Filtros")
    todos_atendentes = df['atendente'].unique().tolist()
    atendente_selecionado = st.selectbox("Selecione um atendente:", todos_atendentes)
    todos_sentimentos = df['sentimento'].unique().tolist()
    sentimentos_selecionados = st.multiselect("Selecione sentimentos:", todos_sentimentos, default=todos_sentimentos)
    if st.button("Gerar Gráfico"):
        gerar_grafico = True
    else:
        gerar_grafico = False

# Colunas para logo e tagline
col1, col2 = st.columns([1, 1])  # Duas colunas de tamanho igual

# Logotipo na primeira coluna (alinhada à esquerda)
with col1:
    st.image("https://www.biolabfarma.com.br/wp-content/themes/biolabtheme/assets/images/logo-menu.png", width=150)

# TAG 'Viva a Evolução' na segunda coluna (alinhada à direita)
with col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end;">
            <img src="https://www.biolabfarma.com.br/wp-content/themes/biolabtheme/assets/images/tagline-viva-evolucao.png" style="max-width: 100%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

# Código HTML e CSS para a faixa no cabeçalho
html_code = """
<div style='
    background: #bfd730;
    background: linear-gradient(133deg, #bfd730 10%, #008fc4 60%);
    background: -webkit-linear-gradient(133deg, #bfd730 10%, #008fc4 60%);
    background: -moz-linear-gradient(133deg, #bfd730 10%, #008fc4 60%);
    margin: 0px 0px 0px 0px;
    width: 100%;
    position: fixed;
    padding: 10px;
    bottom: 0;
    left: 0;
    text-align: center;
    color: white;
    font-family: Arial, sans-serif;
    font-size: 24px;
    font-weight: bold;
'>
    Transcrições do SAC
</div>
"""
# Renderiza o HTML na aplicação Streamlit
components.html(html_code, height=50)

# Visualização da tabela toda
df

# Carregamento e pré-processamento de dados
df['duracao'] = pd.to_timedelta(df['duracao'].astype(str))
df_filtrado = df[df['duracao'] > pd.Timedelta(minutes=5)]

# Função para plotar o gráfico
def plot_filtered_sentiments(atendente, sentimentos):
    df_atendente = df_filtrado[df_filtrado['atendente'] == atendente]
    filtered_data = df_atendente[df_atendente['sentimento'].isin(sentimentos)]

    fig, ax = plt.subplots(figsize=(8, 4))  # Tamanho do gráfico
    sns.set_style('whitegrid')
    cores = sns.color_palette('pastel')

    if len(filtered_data) == 0:
        filtered_data = pd.DataFrame({'sentimento': sentimentos, 'count': [0] * len(sentimentos)})
        sns.barplot(x='sentimento', y='count', data=filtered_data, palette=cores, ax=ax)
    else:
        sns.countplot(x='sentimento', data=filtered_data, palette=cores, ax=ax)

    ax.set_title(f"Sentimentos do Atendente: {atendente} (Filtrado)", fontsize=16, fontweight='bold')
    ax.set_xlabel("Sentimento", fontsize=12)
    ax.set_ylabel("Contagem", fontsize=12)
    ax.spines[['top', 'right']].set_visible(False)
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotação dos rótulos do eixo x

    plt.tight_layout()
    return fig  # Retorna a figura

# Botão para gerar o gráfico
if gerar_grafico:
    fig_sentimentos = plot_filtered_sentiments(atendente_selecionado, sentimentos_selecionados)

    # Colunas para gráfico e outra visualização
    col_grafico, col_outra_visualizacao = st.columns(2)

    # Gráfico de barras na coluna da esquerda
    with col_grafico:
        st.pyplot(fig_sentimentos)

    # Gráfico de pizza na coluna da direita
    with col_outra_visualizacao:
        st.title("Distribuição de Sentimentos")
        df_pizza = df_filtrado[df_filtrado["atendente"] == atendente_selecionado]
        df_pizza = df_pizza[df_pizza["sentimento"].isin(sentimentos_selecionados)]

        sentimentos_contagem = df_pizza['sentimento'].value_counts()
        fig_pizza, ax_pizza = plt.subplots(figsize=(8, 4)) # Mesmo tamanho do outro gráfico
        cores = sns.color_palette('pastel')
        ax_pizza.pie(sentimentos_contagem, labels=sentimentos_contagem.index, autopct='%1.1f%%', startangle=90, colors=cores) # Usando a mesma paleta de cores
        st.pyplot(fig_pizza)
