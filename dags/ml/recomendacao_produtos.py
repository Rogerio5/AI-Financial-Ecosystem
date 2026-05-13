import logging
from sklearn.metrics.pairwise import cosine_similarity
import ml_utils

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("RecomendacaoProdutos")

def main():
    df = ml_utils.load_transactions()
    log.info(f"Transações carregadas: {df.shape}")

    pivot = df.pivot_table(index='cpf', columns='tipo', values='valor', aggfunc='sum').fillna(0)
    similarity = cosine_similarity(pivot)

    cliente_idx = 0
    similar_scores = list(enumerate(similarity[cliente_idx]))
    similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)

    log.info(f"Clientes mais semelhantes ao cliente {cliente_idx}: {similar_scores[:5]}")

    ml_utils.save_result("recomendacao_produtos", {"cliente_idx": cliente_idx, "similaridade": similar_scores[:5]})

if __name__ == "__main__":
    main()
