import logging
from sklearn.cluster import KMeans
import ml_utils

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("SegmentacaoClientes")

def main():
    df = ml_utils.load_clientes()
    log.info(f"Clientes carregados: {df.shape}")

    X = df[['renda_estimada', 'saldo_medio']]

    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)

    log.info("Segmentação concluída. Exemplo:")
    log.info(df[['nome', 'cluster']].head())

    for _, row in df.iterrows():
        ml_utils.save_result("segmentacao_clientes", {"cluster": int(row["cluster"])}, customer_id=int(row["id"]))

if __name__ == "__main__":
    main()
