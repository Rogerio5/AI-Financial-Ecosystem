# 📂 Scripts de Seed e ETL

Este diretório contém scripts auxiliares para inicialização e exportação de dados do projeto **BankPy**.

---

## 📌 `seed_db.py`

Script responsável por popular o banco de dados com dados iniciais (clientes).

### Como executar

Na raiz do projeto:

```powershell
python scripts/seed_db.py
```

O que faz:

```Conecta ao banco configurado em bankpy/db.py.

Insere clientes de exemplo:

Rogério (CPF: 12345678901)

Maria (CPF: 98765432100)

Aplica commit e exibe mensagem de sucesso.

Em caso de erro faz rollback e mostra a mensagem de falha
```

## 📌 etl_db.py

Script responsável por exportar transações do banco para um arquivo CSV

Como executar:

Na raiz do projeto:

```python scripts/etl_db.py
```

O que faz:

```Executa uma query SQL que junta transactions e accounts.

Exporta os dados para data/transactions_flat.csv.

Estrutura do CSV gerado:

id

account_id

owner_cpf

date

type

amount

balance_after

description

Caso não existam transações, informa "Nenhuma transação encontrada."
```

Observações:

O arquivo é gerado em UTF-8.

O diretório data/ é criado automaticamente se não existir.

## ✅ Situação atual

seed_db.py funcionando e populando clientes iniciais.

etl_db.py funcionando e gerando CSV corretamente.

Testes automatizados confirmam que ambos os scripts estão operando conforme esperado.
