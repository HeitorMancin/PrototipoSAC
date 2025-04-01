import pandas as pd
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

dados = "https://raw.githubusercontent.com/HeitorMancin/PrototipoSAC/refs/heads/main/DF.xlsx"  # Substitua pelo caminho real para o seu arquivo
df = pd.read_excel(dados)


st.set_page_config(layout="wide")

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

df

# Agrupa os dados por atendente e sentimento e conta as ocorrências
sentimentos_por_atendente = df.groupby(['atendente', 'sentimento']).size().reset_index(name='contagem')

# Cria o gráfico de barras
plt.figure(figsize=(16, 6))  # Ajusta o tamanho da figura
sns.barplot(x='atendente', y='contagem', hue='sentimento', data=sentimentos_por_atendente)
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.title('Sentimento por Atendente')
plt.xlabel('Atendente')
plt.ylabel('Contagem')
plt.xticks(rotation=45, ha='right')  # Rotaciona os rótulos do eixo x para melhor legibilidade
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de elementos
st.pyplot(plt.gcf())  # Exibir o gráfico no Streamlit#

# Carregamento e pré-processamento de dados
df = pd.read_excel("DF.xlsx", engine='openpyxl')  # Substitua "DF.xlsx" pelo caminho real do seu arquivo
df['duracao'] = pd.to_timedelta(df['duracao'].astype(str))
df_filtrado = df[df['duracao'] > pd.Timedelta(minutes=5)]

# Função para plotar o gráfico
def plot_filtered_sentiments(atendente, sentimentos):
    df_atendente = df_filtrado[df_filtrado['atendente'] == atendente]
    filtered_data = df_atendente[df_atendente['sentimento'].isin(sentimentos)]

    plt.figure(figsize=(10, 6))

    if len(filtered_data) == 0:
        filtered_data = pd.DataFrame({'sentimento': sentimentos, 'count': [0] * len(sentimentos)})
        sns.barplot(x='sentimento', y='count', data=filtered_data, palette='Dark2')
    else:
        sns.countplot(x='sentimento', data=filtered_data, palette='Dark2')

    plt.title(f"Sentimentos do Atendente: {atendente} (Filtrado)")
    plt.xlabel("Sentimento")
    plt.ylabel("Contagem")
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.xticks(rotation=45, ha='right') # Rotação dos rótulos do eixo x

    plt.tight_layout()
    st.pyplot(plt)  # Exibir o gráfico no Streamlit

# Interface do Streamlit
st.title("Análise de Sentimentos de Atendentes")

# Seleção de Atendente
todos_atendentes = df_filtrado['atendente'].unique().tolist()
atendente_selecionado = st.selectbox("Selecione um atendente:", todos_atendentes)

# Seleção de Sentimentos
todos_sentimentos = df_filtrado['sentimento'].unique().tolist()
sentimentos_selecionados = st.multiselect("Selecione sentimentos:", todos_sentimentos, default=todos_sentimentos)

# Botão para gerar o gráfico
if st.button("Gerar Gráfico"):
    plot_filtered_sentiments(atendente_selecionado, sentimentos_selecionados)
