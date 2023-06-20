import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import humanize


table = '/home/felipecastro/personal/project/github_streamlit/streamlit_dash/dashboard/data_source/teste_streamlit.csv'

@st.cache_data
def load_data():

    orders = pd.read_csv(table, index_col='id')
    new = orders['created_at'].str.split('-', expand=True)
    new = new.rename(columns={
        0: 'ano',
        1: 'mes',
        2: 'dia'
    })
    orders = pd.concat([orders, new], axis=1)

    return orders


## carregar dados
df = load_data()
labels = df.order_type.unique().tolist()

# SIDEBAR
## Parâmetros e números de ocorrências
st.sidebar.header("Orders Analysis")
st.sidebar.subheader(
    """
    Análise de ordens e indicadores
    """)
infos_sb = st.sidebar.empty()  ## Placeholder de informações de qtd.
## Options by month
st.sidebar.subheader('Filtros')
month_sb = st.sidebar.multiselect('Escolha o mês desejado', df['mes'].unique(), default=df.mes.max())

## checkbox da tabela
st.sidebar.subheader('Mostrar tabela de dados?')
table = st.sidebar.empty() ## show table :true or :false

## Filter by order_type
order_type_filter = st.sidebar.multiselect(
    label="Order Type",
    options=labels,
    default=["Deposit", "Withdrawal"]
)

filter_dash = df[(df.mes.isin(month_sb)) & (df.order_type.isin(order_type_filter))] ## filtrar o dashboard

## aplicar dados no placeholder
infos_sb.info(f"{filter_dash.shape[0]} Ordens encontradas.")

# MAIN
st.title("Order Analysis")

## Raw data (tabela) depende do checkbox
if table.checkbox("Mostrar tabela de dados?"):
    st.title("Order Analysis - Database")
    st.write(filter_dash)
## Gráfico de kpi - Gera as métrias importantes
def kpi (dataframe):
    withdrawal_data = df[df['order_type'] == "Withdrawal"]
    soma_amount = withdrawal_data['amount'].sum()
    formatado = humanize.intword(soma_amount)
    
    deposit_data = df[df['order_type'] == "Deposit"]
    soma_dep_amount = deposit_data['amount'].sum()
    dep_formatado = humanize.intword(soma_dep_amount)
    
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Withdrawals", formatado)
    kpi2.metric("Deposits", dep_formatado)
    return kpi1, kpi2



## Gráfico
def bars (dash_filtred):
    title = st.title('Orders Insights')
    barras = st.bar_chart(dash_filtred.order_type.value_counts())
    return barras


kpi(df)
bars(filter_dash)