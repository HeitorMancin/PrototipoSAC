import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(layout="wide", page_title="Análise SAC Biolab")

# Layout do cabeçalho com logo e slogan
col1, col2 = st.columns([1, 1])
with col1:
    st.image("https://www.biolabfarma.com.br/wp-content/themes/biolabtheme/assets/images/logo-menu.png", width=150)
with col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end;">
            <img src="https://www.biolabfarma.com.br/wp-content/themes/biolabtheme/assets/images/tagline-viva-evolucao.png" style="max-width: 100%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

# HTML do banner de rodapé
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
components.html(html_code, height=50)

# Carregamento de dados - escolha uma fonte (URL ou arquivo local)
# Use @st.cache_data para otimizar o carregamento de dados
@st.cache_data
def carregar_dados():
    try:
        # Tenta carregar do GitHub URL
        url = "https://raw.githubusercontent.com/HeitorMancin/PrototipoSAC/refs/heads/main/DF.xlsx"
        df = pd.read_excel(url)
    except:
        # Recorre ao arquivo local se a URL falhar
        try:
            df = pd.read_excel("DF.xlsx", engine='openpyxl')
        except:
            st.error("Não foi possível carregar os dados. Verifique se o arquivo DF.xlsx está disponível.")
            return None
    
    # Processa a coluna de duração
    if 'duracao' in df.columns:
        df['duracao'] = pd.to_timedelta(df['duracao'].astype(str))
    
    return df

# Carrega os dados
df = carregar_dados()

if df is not None:
    # Exibe dados brutos com uma seção expansível
    with st.expander("Ver Dados Brutos"):
        st.dataframe(df)
    
    # Título principal
    st.title("Análise de Sentimentos de Atendentes")
    
    # Seção de visualização principal
    st.header("Visão Geral por Atendente")
    
    # Primeiro gráfico - sentimento geral por atendente
    sentimentos_por_atendente = df.groupby(['atendente', 'sentimento']).size().reset_index(name='contagem')
    
    fig1, ax1 = plt.subplots(figsize=(16, 6))
    sns.barplot(x='atendente', y='contagem', hue='sentimento', data=sentimentos_por_atendente, ax=ax1)
    ax1.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax1.set_title('Sentimento por Atendente')
    ax1.set_xlabel('Atendente')
    ax1.set_ylabel('Contagem')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    st.pyplot(fig1)
    
    # Seção de filtros
    st.header("Análise Detalhada com Filtros")
    
    # Filtra dados para chamadas com mais de 5 minutos
    df_filtrado = df[df['duracao'] > pd.Timedelta(minutes=5)]
    
    # Filtros da barra lateral
    todos_atendentes = sorted(df_filtrado['atendente'].unique().tolist())
    atendente_selecionado = st.selectbox("Selecione um atendente:", todos_atendentes)
    
    todos_sentimentos = sorted(df_filtrado['sentimento'].unique().tolist())
    sentimentos_selecionados = st.multiselect("Selecione sentimentos:", todos_sentimentos, default=todos_sentimentos)
    
    # Função para plotar dados filtrados
    def plotar_sentimentos_filtrados(df, atendente, sentimentos):
        df_atendente = df[df['atendente'] == atendente]
        dados_filtrados = df_atendente[df_atendente['sentimento'].isin(sentimentos)]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if len(dados_filtrados) == 0:
            st.warning(f"Nenhum dado encontrado para o atendente {atendente} com os sentimentos selecionados.")
            dados_dummy = pd.DataFrame({'sentimento': sentimentos, 'contagem': [0] * len(sentimentos)})
            sns.barplot(x='sentimento', y='contagem', data=dados_dummy, palette='Dark2', ax=ax)
        else:
            # Gráfico de contagem para dados filtrados
            contagem_sentimentos = dados_filtrados['sentimento'].value_counts().reset_index()
            contagem_sentimentos.columns = ['sentimento', 'contagem']
            
            # Filtra para incluir apenas sentimentos selecionados
            contagem_sentimentos = contagem_sentimentos[contagem_sentimentos['sentimento'].isin(sentimentos)]
            
            # Cria o gráfico
            sns.barplot(x='sentimento', y='contagem', data=contagem_sentimentos, palette='Dark2', ax=ax)
        
        ax.set_title(f"Sentimentos do Atendente: {atendente}")
        ax.set_xlabel("Sentimento")
        ax.set_ylabel("Contagem")
        ax.spines[['top', 'right']].set_visible(False)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig
    
    # Botão para gerar o gráfico filtrado
    if st.button("Gerar Gráfico"):
        if sentimentos_selecionados:
            fig2 = plotar_sentimentos_filtrados(df_filtrado, atendente_selecionado, sentimentos_selecionados)
            st.pyplot(fig2)
        else:
            st.warning("Por favor, selecione pelo menos um sentimento.")
    
    # Métricas e insights adicionais
    st.header("Métricas Adicionais")
    
    col_metricas1, col_metricas2, col_metricas3 = st.columns(3)
    
    with col_metricas1:
        total_atendimentos = len(df)
        st.metric("Total de Atendimentos", total_atendimentos)
    
    with col_metricas2:
        tempo_medio = df['duracao'].mean()
        st.metric("Tempo Médio de Atendimento", f"{tempo_medio.total_seconds() / 60:.2f} min")
    
    with col_metricas3:
        sentimento_predominante = df['sentimento'].value_counts().idxmax()
        st.metric("Sentimento Predominante", sentimento_predominante)
else:
    st.error("Não foi possível processar os dados. Verifique o formato do arquivo.")
