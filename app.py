import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados
URL_DADOS = "https://raw.githubusercontent.com/HeitorMancin/PrototipoSAC/main/DF.xlsx"

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel(URL_DADOS)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None

df = carregar_dados()

st.set_page_config(layout="wide")

if df is not None:
    # Verificar se as colunas esperadas existem
    colunas_esperadas = {'atendente', 'sentimento', 'duracao'}
    if not colunas_esperadas.issubset(df.columns):
        st.error("O arquivo não contém todas as colunas necessárias.")
    else:
        # Converter a coluna 'duracao' para timedelta corretamente
        df['duracao'] = pd.to_timedelta(df['duracao'], errors='coerce')
        df_filtrado = df[df['duracao'] > pd.Timedelta(minutes=5)]
        
        # Sidebar para filtros
        with st.sidebar:
            st.header("Filtros")
            atendente_selecionado = st.selectbox("Selecione um atendente:", df['atendente'].unique())
            sentimentos_selecionados = st.multiselect("Selecione sentimentos:", df['sentimento'].unique(), default=df['sentimento'].unique())
            gerar_grafico = st.button("Gerar Gráfico")
        
        # Header com logo
        st.image("https://www.biolabfarma.com.br/wp-content/themes/biolabtheme/assets/images/logo-menu.png", width=150)
        st.markdown("## Transcrições do SAC")
        
        # Exibir tabela de dados
        st.write("### Tabela de Dados")
        selected_row = st.data_editor(df_filtrado, use_container_width=True, hide_index=True)
        
        # Botão para baixar arquivo
        def gerar_txt(dataframe):
            texto = dataframe.to_string(index=False)
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(texto)
            return "output.txt"
        
        if not selected_row.empty:
            if st.button("Baixar Arquivo Selecionado em .txt"):
                arquivo = gerar_txt(selected_row)
                with open(arquivo, "rb") as f:
                    st.download_button("Baixar Arquivo .txt", data=f, file_name="selecao.txt", mime="text/plain")
        
        # Gerar gráficos
        if gerar_grafico:
            def plot_graficos():
                df_atendente = df_filtrado[df_filtrado['atendente'] == atendente_selecionado]
                df_atendente = df_atendente[df_atendente['sentimento'].isin(sentimentos_selecionados)]
                
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.countplot(x='sentimento', data=df_atendente, palette='pastel', ax=ax)
                ax.set_title(f"Sentimentos do Atendente: {atendente_selecionado}")
                ax.set_xlabel("Sentimento")
                ax.set_ylabel("Contagem")
                plt.xticks(rotation=45)
                
                st.pyplot(fig)
            
            plot_graficos()
