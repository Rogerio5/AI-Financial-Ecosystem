import subprocess
import sys
from pathlib import Path

def test_seed_and_etl():
    # Executa script que popula o banco com Customers, Accounts e Transactions
    subprocess.run([sys.executable, "-m", "scripts.seed_db"], check=True)
    # Executa script que exporta transações para CSV
    subprocess.run([sys.executable, "scripts/etl_db.py"], check=True)

    csv_file = Path("data") / "transactions_flat.csv"
    assert csv_file.exists()

    # Verifica se o CSV tem conteúdo
    with open(csv_file, encoding="utf-8") as f:
        content = f.read()
        assert "id" in content
        assert "amount" in content
