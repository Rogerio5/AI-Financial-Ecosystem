import streamlit as st
import pandas as pd
import psycopg2
import json

st.set_page_config(page_title="BankPy ML Dashboard", layout="wide")
st.title("📊 BankPy ML Dashboard")

# Conectar ao Postgres (onde você salva resultados dos modelos)
conn = psycopg2.connect("dbname=bankpy user=postgres password=123 host=db port=5432")
df = pd.read_sql("SELECT * FROM ml_results", conn)
conn.close()

# Converter JSON se necessário
def parse_json(x):
    try:
        return json.loads(x) if isinstance(x, str) else x
    except Exception:
        return x

df["prediction"] = df["prediction"].apply(parse_json)

# Filtro por modelo
model = st.selectbox("Escolha o modelo", df["model_name"].unique())
filtered = df[df["model_name"] == model]

st.write("Resultados do modelo:", model)
st.dataframe(filtered)

# Visualizações dinâmicas
if model == "saldo_predict":
    st.subheader("📈 Previsão de Saldo")
    # Supondo que prediction contenha saldo previsto
    saldo_df = pd.DataFrame(filtered["prediction"].tolist())
    saldo_df["run_date"] = filtered["run_date"].values
    st.line_chart(saldo_df.set_index("run_date"))

elif model == "fraude_detect":
    st.subheader("🚨 Detecção de Fraude")
    # Supondo que prediction contenha flag de fraude
    fraude_flags = [p.get("fraude", "desconhecido") for p in filtered["prediction"]]
    st.bar_chart(pd.Series(fraude_flags).value_counts())

elif model == "segmentacao_clientes":
    st.subheader("👥 Segmentação de Clientes")
    # Supondo que prediction contenha cluster_id
    clusters = [p.get("cluster", "N/A") for p in filtered["prediction"]]
    st.bar_chart(pd.Series(clusters).value_counts())

elif model == "recomendacao_produtos":
    st.subheader("💡 Recomendação de Produtos")
    # Supondo que prediction contenha lista de produtos
    recs = []
    for p in filtered["prediction"]:
        if isinstance(p, dict) and "produtos" in p:
            recs.extend(p["produtos"])
    st.bar_chart(pd.Series(recs).value_counts())
