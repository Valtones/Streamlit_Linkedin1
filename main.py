import streamlit as st
import plotly.express as px
import pandas as pd


st.set_page_config(layout="wide")

df = pd.read_csv('Vendas.csv', sep=";",decimal=".")
#configura para o formato data o padrão Brasileiro dd/mm/aa
df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")

#Apagar as colunas com configuração de pontuação incorreta
del df['Taxa de 5%']
del df['Total']

##Criei novamente essas colunas com cálculo:
# Calcula 5% do valor (Quantidade × Preço Unitário)
df["Taxa 5%"] = (df['Quantidade'] * df['Preço Unitário']) * 0.05
# Calcula o TOTAL (Quantidade × Preço Unitário + 5%)
df['Total'] = (df['Quantidade'] * df['Preço Unitário']) + df["Taxa 5%"]

#Coloca em ordem alfanumérica as datas
df=df.sort_values('Data')

#Incluimos uma coluna chamada mês e Concatenamos "ANO" + "-" + "MÊS"
df['Mês']=df["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))

#Barra Lateral(SideBar) separando pela coluna Mês deixando apenas uma ocorrencia(Unique)
Mês = st.sidebar.selectbox("Mês",df["Mês"].unique())
#Filial = st.sidebar.

#Apresentação da tabela filtrada
df_filtrado = df[df["Mês"] == Mês]
#df_filtrado

#Título
#st.title('Dashboard Simples - Linkedin - Valter Gomes')
st.markdown("<h1 style='text-align: center;'>Dash Vendas - LinkedIn - Valter Gomes</h1>", 
            unsafe_allow_html=True)

#Criação de colunas para apresentação dos Graficos
coluna1, coluna2 = st.columns(2)
coluna3, coluna4, coluna5 = st.columns(3)

#1 - Faturamento por Unidade
Total_Dia = df_filtrado.groupby(["Data", "Cidade"])["Total"].sum().reset_index()
Graf1 = px.bar(Total_Dia, x="Data", y="Total", color="Cidade", 
               title="Faturamento por dia")
Graf1.update_layout(title_x=0.3)  # Centraliza o título
coluna1.plotly_chart(Graf1,use_container_width=True)

#2 - Tipo de Produto mais vendido
Total_Tipo = df_filtrado.groupby(["Linha de Produtos","Cidade"])["Quantidade"].sum().reset_index()
Graf2 = px.bar(Total_Tipo, x="Quantidade", y="Linha de Produtos", color = "Cidade",title="Qtde de vendas por tipo de Produto",orientation="h")
Graf2.update_layout(title_x=0.2)  # Centraliza o título
coluna2.plotly_chart(Graf2,use_container_width=True)

#3 - Contribuição por Filial
Total_Cidade = df_filtrado.groupby('Cidade')[['Total']].sum().reset_index()
Graf3 = px.bar(Total_Cidade, x="Cidade", y="Total",title="Faturamento por Filial")
Graf3.update_layout(title_x=0.3)  # Centraliza o título
coluna3.plotly_chart(Graf3,use_container_width=True)

#4 - Desempenho das Formas de Pagamento
Graf4 = px.pie(df_filtrado,values = "Total", names ="Forma de Pagamento",title="Faturamento por Forma de Pagamento")
Graf4.update_layout(title_x=0.1)  # Centraliza o título
coluna4.plotly_chart(Graf4,use_container_width=True)

#5 - Como estão as avaliações das filiais
Avaliacoes = df_filtrado.groupby('Cidade')[['Classificação']].mean().reset_index()
Graf5 = px.bar(Avaliacoes, x="Cidade", y="Classificação",title="Avaliação média por Filial")
Graf5.update_layout(title_x=0.3)  # Centraliza o título
coluna5.plotly_chart(Graf5,use_container_width=True)


#python3 -m streamlit run main.py