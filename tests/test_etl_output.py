import csv
from pathlib import Path

def test_etl_csv_exists():
    csv_file = Path("data") / "transactions_flat.csv"
    assert csv_file.exists()

def test_etl_csv_structure():
    csv_file = Path("data") / "transactions_flat.csv"
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        # Estrutura esperada para transações bancárias
        assert "id" in headers
        assert "account_id" in headers
        assert "amount" in headers
        assert "date" in headers
        assert "type" in headers
        assert "balance_after" in headers

def test_etl_csv_encoding():
    csv_file = Path("data") / "transactions_flat.csv"
    with open(csv_file, encoding="utf-8") as f:
        content = f.read()
        assert isinstance(content, str)
