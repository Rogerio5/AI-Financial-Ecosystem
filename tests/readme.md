# Testes do Projeto BankPy

Este diretório contém os testes automatizados para validar as principais funcionalidades do sistema bancário.

## Situação atual

✅ **Testes unitários**

- CRUD de **Customer** (clientes) passou com sucesso.
- CRUD de **Account** (contas) passou com sucesso.
- Operações de **Transfer** (transferências entre contas) passaram com sucesso.

✅ **Testes de integração**

- Script de **Seed + ETL** executado corretamente.
- Exportação de transações para CSV validada.

✅ **Validação do CSV**

- Arquivo `data/transactions_flat.csv` gerado com sucesso.
- Estrutura e colunas esperadas confirmadas.
- Arquivo em UTF-8 e legível.

---

## Como executar os testes

Na raiz do projeto, use:

```powershell
pytest -v
```

## Para rodar apenas os testes unitários

```powershell
pytest tests\test_crud_users.py tests\test_crud_products.py tests\test_crud_transfer.py -v
```

## Para rodar apenas os testes de integração

```powershell
pytest tests\test_db_integration.py tests\test_etl_output.py -v
```
