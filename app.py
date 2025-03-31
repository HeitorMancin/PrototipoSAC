import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

dados = "DF.xlsx"  # Substitua pelo caminho real para o seu arquivo
df = pd.read_excel(dados)

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
