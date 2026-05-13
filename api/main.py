from fastapi import FastAPI
from api.routers import clients, transactions
from datetime import datetime
import requests

# Configuração Databricks
DATABRICKS_HOST = "https://<sua-instancia>.azuredatabricks.net"
DATABRICKS_TOKEN = "<seu-token>"
CLUSTER_ID = "<seu-cluster-id>"

app = FastAPI(
    title="BankPy API",
    version="1.0.0",
    description="API para gerenciamento de clientes, contas, transações bancárias e modelos de ML"
)

# Inclui os routers com prefixos distintos
app.include_router(clients.router, prefix="/customers", tags=["Customers"])
app.include_router(transactions.router, prefix="/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

# Endpoint raiz informativo
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "BankPy API is running!",
        "version": "1.0.0",
        "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "available_endpoints": [
            "/customers",
            "/accounts",
            "/transactions",
            "/ml/predict-saldo",
            "/ml/detect-fraude",
            "/ml/segmentacao-clientes",
            "/ml/recomendacao-produtos"
        ]
    }

# Endpoint /health minimalista (para monitoramento)
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -----------------------------
# Função auxiliar para disparar Jobs no Databricks
# -----------------------------
def run_databricks_job(run_name: str, notebook_path: str):
    headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
    payload = {
        "run_name": run_name,
        "existing_cluster_id": CLUSTER_ID,
        "notebook_task": {"notebook_path": notebook_path}
    }
    response = requests.post(f"{DATABRICKS_HOST}/api/2.1/jobs/runs/submit",
                             json=payload, headers=headers)
    return response.json()

# -----------------------------
# Endpoints de Machine Learning (via Databricks)
# -----------------------------

@app.get("/ml/predict-saldo")
def predict_saldo():
    return run_databricks_job("predict_saldo", "/Repos/bankpy/ml/saldo_predict")

@app.get("/ml/detect-fraude")
def detect_fraude():
    return run_databricks_job("detect_fraude", "/Repos/bankpy/ml/fraude_detect")

@app.get("/ml/segmentacao-clientes")
def segmentacao_clientes():
    return run_databricks_job("segmentacao_clientes", "/Repos/bankpy/ml/segmentacao_clientes")

@app.get("/ml/recomendacao-produtos")
def recomendacao_produtos():
    return run_databricks_job("recomendacao_produtos", "/Repos/bankpy/ml/recomendacao_produtos")
