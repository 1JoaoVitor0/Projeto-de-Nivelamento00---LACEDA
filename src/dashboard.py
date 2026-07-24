import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="HR Analytics - LACEDA", layout="wide")

st.title("📊 Dashboard de Evasão e Clima Organizacional (HR Analytics)")
st.markdown("Análise de Turnover cruzada com Carga de Trabalho e Liderança.")

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CSV = os.path.join(DIRETORIO_ATUAL, '../data/processed/funcionarios_abt.csv')

@st.cache_data
def load_data():
    df = pd.read_csv(CAMINHO_CSV)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Base de dados não encontrada. Execute o pipeline ETL primeiro.")
    st.stop()

# --- KPIs Iniciais ---
st.subheader("Visão Geral do Escritório")
col1, col2, col3, col4 = st.columns(4)

total_funcionarios = len(df)
taxa_evasao_global = (df['status_atual'] == 'Desligado').mean() * 100
satisfacao_geral = df['score_satisfacao'].mean()
horas_extras_geral = df['horas_extras_mes'].mean()

col1.metric("Total de Colaboradores", total_funcionarios)
col2.metric("Taxa de Evasão Global", f"{taxa_evasao_global:.1f}%")
col3.metric("Satisfação Média", f"{satisfacao_geral:.1f} / 5.0")
col4.metric("Média Horas Extras/Mês", f"{horas_extras_geral:.0f}h")

st.divider()

# SEÇÃO 1: Burnout 
st.subheader("1. A Hipótese do Burnout: Carga de Trabalho por Nível")
st.markdown("Comparativo de Horas Extras e Processos Ativos entre funcionários **Ativos** e **Desligados**.")

burnout_df = df.groupby(['nivel', 'status_atual'])[['horas_extras_mes', 'processos_actifs']].mean().reset_index()

col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    fig_horas = px.bar(
        burnout_df, 
        x='nivel', y='horas_extras_mes', color='status_atual', barmode='group',
        title="Média de Horas Extras por Nível",
        labels={'horas_extras_mes': 'Horas Extras', 'nivel': 'Senioridade', 'status_atual': 'Status'},
        color_discrete_map={'Ativo': '#1f77b4', 'Desligado': '#d62728'}
    )
    st.plotly_chart(fig_horas, use_container_width=True)

with col_grafico2:
    fig_processos = px.bar(
        burnout_df, 
        x='nivel', y='processos_actifs', color='status_atual', barmode='group',
        title="Volume de Processos por Nível",
        labels={'processos_actifs': 'Qtd. Processos', 'nivel': 'Senioridade', 'status_atual': 'Status'},
        color_discrete_map={'Ativo': '#1f77b4', 'Desligado': '#d62728'}
    )
    st.plotly_chart(fig_processos, use_container_width=True)

st.info("💡 **Insight:** Fica evidente o esgotamento da base da pirâmide. Juniores que saem da empresa executam quase o triplo de horas extras e o dobro de processos em relação aos ativos.")

st.divider()

# SEÇÃO 2: Liderança Tóxica
st.subheader("2. Raio-X da Liderança: Gestores em Zona Crítica")

gestores_df = df[df['id_reporta_a'] != -1].groupby('id_reporta_a').agg(
    total_liderados=('status_atual', 'count'),
    taxa_evasao=('status_atual', lambda x: (x == 'Desligado').mean() * 100),
    satisfacao_media=('score_satisfacao', 'mean')
).reset_index()

gestores_df['Alerta'] = gestores_df.apply(
    lambda row: 'Crítico' if row['taxa_evasao'] > 30 else 'Estável',
    axis=1
)

gestores_df['id_reporta_a'] = gestores_df['id_reporta_a'].astype(int).astype(str)

fig_lideranca = px.scatter(
    gestores_df, 
    x='satisfacao_media', y='taxa_evasao', 
    color='Alerta', size='total_liderados', text='id_reporta_a',
    title="Taxa de Evasão vs Satisfação da Equipe (Tamanho do círculo = Qtd. Liderados)",
    labels={'satisfacao_media': 'Satisfação Média (1 a 5)', 'taxa_evasao': 'Taxa de Evasão (%)'},
    color_discrete_map={'Estável': '#2ca02c', 'Crítico': '#d62728'}
)

fig_lideranca.update_traces(textposition='top center')
st.plotly_chart(fig_lideranca, use_container_width=True)
st.warning("⚠️ **Alerta:** Os líderes com IDs **200, 400 e 501** operam na zona de risco severa, concentrando as piores notas de clima e os maiores índices de demissão.")
