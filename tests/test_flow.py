import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Criar cliente
customer_payload = {
    "cpf": "12345678901",
    "name": "Rogerio Silva",
    "email": "rogerio@example.com"
}
r = requests.post(f"{BASE_URL}/customers/", json=customer_payload)
print("Create customer:", r.status_code, r.json())

# 2. Criar conta
account_payload = {
    "id": "ACC001",
    "owner_cpf": "12345678901",
    "balance": 1000.0
}
r = requests.post(f"{BASE_URL}/accounts", json=account_payload)
print("Create account:", r.status_code, r.json())

# 3. Depósito
deposit_payload = {
    "account_id": "ACC001",
    "amount": 500.0
}
r = requests.post(f"{BASE_URL}/accounts/deposit", params=deposit_payload)
print("Deposit:", r.status_code, r.json())

# 4. Saque
withdraw_payload = {
    "account_id": "ACC001",
    "amount": 200.0
}
r = requests.post(f"{BASE_URL}/accounts/withdraw", params=withdraw_payload)
print("Withdraw:", r.status_code, r.json())

# 5. Criar segunda conta para transferência
account_payload2 = {
    "id": "ACC002",
    "owner_cpf": "12345678901",
    "balance": 0.0
}
r = requests.post(f"{BASE_URL}/accounts", json=account_payload2)
print("Create second account:", r.status_code, r.json())

# 6. Transferência
transfer_payload = {
    "from_id": "ACC001",
    "to_id": "ACC002",
    "amount": 300.0
}
r = requests.post(f"{BASE_URL}/accounts/transfer", params=transfer_payload)
print("Transfer:", r.status_code, r.json())

# 7. Listar transações
r = requests.get(f"{BASE_URL}/transactions")
print("Transactions:", r.status_code, r.json())
