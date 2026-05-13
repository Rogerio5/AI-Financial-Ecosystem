# 📂 BankPy - Módulos Principais

Este diretório contém os módulos centrais do projeto **BankPy**, responsáveis pela lógica de negócio, persistência de dados e segurança.

---

## 📌 `db.py`

Responsável pela configuração do banco de dados e sessão.

### O que faz

- Define a string de conexão para PostgreSQL (`bankpy_test`).
- Cria o `engine` via SQLAlchemy.
- Configura `SessionLocal` para gerenciar sessões.
- Define a `Base` para os modelos ORM.

---

## 📌 `models.py`

Define os modelos ORM que representam as tabelas do banco.

### Estrutura

- **Customer**
  - `cpf` (PK)
  - `name`
  - `email`
  - Relacionamento: `accounts`
- **Account**
  - `id` (PK)
  - `owner_cpf` (FK → Customer)
  - `balance`
  - Relacionamentos: `owner`, `transactions`
- **Transaction**
  - `id` (PK autoincrement)
  - `account_id` (FK → Account)
  - `date`
  - `type` (deposit, withdraw, transfer)
  - `amount`
  - `balance_after`
  - `description`
  - Relacionamento: `account`

---

## 📌 `crud.py`

Contém as funções de manipulação de dados (CRUD + operações financeiras).

### Funções principais

- `create_customer(db, name, cpf, email="")` → cria cliente.
- `create_account(db, account_id, owner_cpf, initial_balance=0.0)` → cria conta e registra depósito inicial.
- `deposit(db, account_id, amount, description="")` → realiza depósito.
- `withdraw(db, account_id, amount, description="")` → realiza saque com verificação de saldo.
- `transfer(db, from_id, to_id, amount, description="")` → transfere valores entre contas de forma atômica.

### Observações

- Todas as operações usam `datetime.now(timezone.utc)` para registrar datas em UTC.
- Nenhuma função faz `commit` diretamente; o chamador controla a transação.

---

## 📌 `security.py`

Responsável pela segurança de senhas.

### Funções

- `hash_password(password: str) -> str`  
  Gera hash seguro usando `bcrypt`.
- `verify_password(password: str, hashed: str) -> bool`  
  Verifica se a senha corresponde ao hash armazenado.

---

## ✅ Situação atual

- Banco configurado com PostgreSQL local (`bankpy_test`).  
- Modelos ORM (`Customer`, `Account`, `Transaction`) definidos e funcionando.  
- Operações CRUD implementadas e testadas com sucesso.  
- Segurança de senhas garantida via `bcrypt`.  
- Testes unitários e de integração confirmam que todos os módulos estão operando corretamente.

---

## ✅ Agora você tem todos os arquivos melhorados

db.py configurável via env.

models.py com relacionamentos.

schemas.py com validações extras.

security.py com hash de senha + JWT.

crud.py integrado com senha e operações robustas