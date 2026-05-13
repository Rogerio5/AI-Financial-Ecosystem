import logging
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import ml_utils

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("SaldoPredict")

def main():
    df = ml_utils.load_transactions()
    log.info(f"Transações carregadas: {df.shape}")

    df['valor_medio'] = df.groupby('cpf')['valor'].transform('mean')
    X = df[['valor_medio']]
    y = df['saldo']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    coef = model.coef_.tolist()
    intercept = model.intercept_
    score = model.score(X_test, y_test)

    log.info(f"Modelo saldo_predict treinado. Score={score}")

    ml_utils.save_result("saldo_predict", {"coef": coef, "intercepto": intercept, "score": score})

if __name__ == "__main__":
    main()
