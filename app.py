import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns

# Desativa avisos para evitar mensagens de aviso no Streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)

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

# Carregamento de dados - optando pela abordagem mais simples para depuração
try:
    # Primeira tentativa: Carregar da URL
    url = "https://raw.githubusercontent.com/HeitorMancin/PrototipoSAC/refs/heads/main/DF.xlsx"
    df = pd.read_excel(url)
    st.success("Dados carregados com sucesso da URL GitHub.")
except Exception as e:
    st.warning(f"Erro ao carregar dados da URL: {e}")
    try:
        # Segunda tentativa: Carregar do arquivo local
        df = pd.read_excel("DF.xlsx", engine='openpyxl')
        st.success("Dados carregados com sucesso do arquivo local.")
    except Exception as e:
        st.error(f"Erro ao carregar dados do arquivo local: {e}")
        # Criar dados de exemplo para testar a interface
        st.warning("Usando dados de exemplo para testes.")
        df = pd.DataFrame({
            'atendente': ['Ana', 'Ana', 'Carlos', 'Carlos', 'Maria', 'Maria'] * 5,
            'sentimento': ['Positivo', 'Negativo', 'Neutro', 'Positivo', 'Neutro', 'Negativo'] * 5,
            'duracao': ['00:06:00', '00:07:30', '00:10:00', '00:05:30', '00:08:00', '00:09:30'] * 5
        })

# Processa a coluna de duração se existir
if 'duracao' in df.columns:
    try:
        df['duracao'] = pd.to_timedelta(df['duracao'].astype(str))
    except Exception as e:
        st.error(f"Erro ao processar a coluna de duração: {e}")
        # Criar coluna de duração simulada
        df['duracao'] = pd.to_timedelta(['00:07:00'] * len(df))

# Exibe dados brutos com uma seção expansível
with st.expander("Ver Dados Brutos"):
    st.dataframe(df)

# Título principal
st.title("Análise de Sentimentos de Atendentes")

# Separação clara para depuração
st.markdown("---")
st.header("Visão Geral por Atendente")

# Gráfico 1: Visão Geral - Abordagem simplificada usando pyplot diretamente
try:
    # Prepara os dados
    sentimentos_por_atendente = df.groupby(['atendente', 'sentimento']).size().reset_index(name='contagem')
    
    # Limpa qualquer gráfico anterior (importante para o Streamlit)
    plt.clf()
    
    # Cria a figura 
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='atendente', y='contagem', hue='sentimento', data=sentimentos_por_atendente)
    
    # Configurações do gráfico
    plt.title('Sentimento por Atendente')
    plt.xlabel('Atendente')
    plt.ylabel('Contagem')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Exibe o gráfico
    st.pyplot()
    
except Exception as e:
    st.error(f"Erro ao gerar o gráfico de visão geral: {e}")

# Separação clara para depuração
st.markdown("---")
st.header("Análise Detalhada com Filtros")

# Filtra dados para chamadas com mais de 5 minutos
try:
    df_filtrado = df[df['duracao'] > pd.Timedelta(minutes=5)]
    st.write(f"Número de registros após filtro de duração: {len(df_filtrado)}")
except Exception as e:
    st.error(f"Erro ao filtrar dados por duração: {e}")
    df_filtrado = df  # Usa todos os dados se o filtro falhar

# Filtros para o segundo gráfico
try:
    todos_atendentes = sorted(df_filtrado['atendente'].unique().tolist())
    atendente_selecionado = st.selectbox("Selecione um atendente:", todos_atendentes)
    
    todos_sentimentos = sorted(df_filtrado['sentimento'].unique().tolist())
    sentimentos_selecionados = st.multiselect("Selecione sentimentos:", todos_sentimentos, default=todos_sentimentos)
except Exception as e:
    st.error(f"Erro ao configurar filtros: {e}")
    atendente_selecionado = df_filtrado['atendente'].iloc[0] if not df_filtrado.empty else "Nenhum"
    sentimentos_selecionados = df_filtrado['sentimento'].unique().tolist() if not df_filtrado.empty else []

# Função para plotar dados filtrados (versão simplificada)
def plotar_sentimentos_filtrados():
    try:
        # Filtrar dados
        df_atendente = df_filtrado[df_filtrado['atendente'] == atendente_selecionado]
        dados_filtrados = df_atendente[df_atendente['sentimento'].isin(sentimentos_selecionados)]
        
        # Limpar gráficos anteriores
        plt.clf()
        
        # Criar novo gráfico
        plt.figure(figsize=(10, 6))
        
        if len(dados_filtrados) == 0:
            st.warning(f"Nenhum dado encontrado para o atendente {atendente_selecionado} com os sentimentos selecionados.")
            # Criar gráfico vazio
            plt.bar(sentimentos_selecionados, [0] * len(sentimentos_selecionados))
        else:
            # Contar ocorrências
            contagem = dados_filtrados['sentimento'].value_counts()
            
            # Garantir que todos os sentimentos selecionados apareçam
            for sentimento in sentimentos_selecionados:
                if sentimento not in contagem:
                    contagem[sentimento] = 0
            
            # Filtrar apenas os sentimentos selecionados
            contagem = contagem[sentimentos_selecionados]
            
            # Criar gráfico
            plt.bar(contagem.index, contagem.values, color='skyblue')
        
        # Configurar gráfico
        plt.title(f"Sentimentos do Atendente: {atendente_selecionado}")
        plt.xlabel("Sentimento")
        plt.ylabel("Contagem")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Mostrar gráfico
        st.pyplot()
        
    except Exception as e:
        st.error(f"Erro ao gerar gráfico filtrado: {e}")
        # Mostra a exceção completa para depuração
        st.exception(e)

# Botão para gerar o gráfico filtrado
if st.button("Gerar Gráfico"):
    if sentimentos_selecionados:
        plotar_sentimentos_filtrados()
    else:
        st.warning("Por favor, selecione pelo menos um sentimento.")

# Separação clara para depuração
st.markdown("---")
st.header("Métricas Adicionais")

# Exibir métricas básicas
try:
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
except Exception as e:
    st.error(f"Erro ao exibir métricas: {e}")

# Informações de depuração
st.markdown("---")
with st.expander("Informações de Depuração"):
    st.write("Formato do DataFrame:")
    st.write(df.dtypes)
    st.write("Primeiras linhas:")
    st.write(df.head())
    st.write("Estatísticas:")
    st.write(df.describe())
    st.write("Informações da coluna de duração:")
    if 'duracao' in df.columns:
        st.write(f"Tipo da coluna duracao: {type(df['duracao'].iloc[0])}")
        st.write(f"Valores únicos de duracao: {df['duracao'].unique()[:5]}")
