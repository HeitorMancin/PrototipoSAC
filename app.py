import pandas as pd
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

st.pyplot(plt.gcf())  # Exibir o gráfico no Streamlit
