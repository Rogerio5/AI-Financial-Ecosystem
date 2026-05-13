import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import ml_utils

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("FraudeDetect")

def main():
    df = ml_utils.load_transactions()
    log.info(f"Transações carregadas: {df.shape}")

    # Criar variável alvo (fraude simulada: valores muito altos)
    df['fraude'] = (df['valor'] > 10000).astype(int)

    X = df[['valor', 'saldo']]
    y = df['fraude']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    log.info(f"Acurácia do modelo fraude_detect: {score}")

    ml_utils.save_result("fraude_detect", {"acuracia": score})

if __name__ == "__main__":
    main()
