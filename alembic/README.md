# 📂 Alembic - Configuração e Migrations

Este diretório contém os arquivos de configuração e migrations do **BankPy**, usados para versionar o schema do banco de dados com Alembic.

---

## 📌 Arquivos principais

### `env.py`

Arquivo de configuração que conecta o Alembic ao SQLAlchemy.

- Lê a variável de ambiente `DATABASE_URL` (boa prática para não fixar credenciais).
- Importa `Base.metadata` de `bankpy/db.py` para detectar mudanças nos modelos.
- Define execução em:
  - **Modo offline** → gera SQL sem conectar ao banco.
  - **Modo online** → aplica migrations diretamente no banco.
- Configura comparação de tipos e defaults (`compare_type=True`, `compare_server_default=True`).

---

### `versions/0166e30db912_init_schema.py`

Migration inicial que cria as tabelas principais do sistema.

#### Estrutura criada

- **customers**
  - `cpf` (PK)
  - `name`
  - `email`

- **accounts**
  - `id` (PK)
  - `owner_cpf` (FK → customers.cpf)
  - `balance` (default 0.0)

- **transactions**
  - `id` (PK autoincrement)
  - `account_id` (FK → accounts.id)
  - `date` (default `now()`)
  - `type`
  - `amount`
  - `balance_after`
  - `description`

#### Downgrade

Remove as tabelas na ordem inversa (`transactions`, `accounts`, `customers`).

---

### `script.py.mako`

Template usado pelo Alembic para gerar novas migrations automaticamente.

- Define cabeçalho com:
  - `Revision ID`
  - `Revises`
  - `Create Date`
- Estrutura padrão com funções:
  - `upgrade()` → aplica mudanças.
  - `downgrade()` → desfaz mudanças.
- Substituído dinamicamente pelo Alembic ao criar novas migrations.

---

## 📌 Fluxo de uso

1. **Criar migration inicial** (já feita)

   ```powershell
    alembic revision --autogenerate -m "init schema     
    ```

## Aplicar migration

```powershell
alembic upgrade head
```

## Gerar novas migrations sempre que alterar models.py

```powershell
alembic revision --autogenerate -m "add new field"
alembic upgrade head
```

## ✅ Situação atual

env.py configurado corretamente para usar Base.metadata.

Migration inicial (init_schema) criada e pronta para aplicar.

Template script.py.mako disponível para gerar novas migrations.

Alembic integrado ao projeto e pronto para versionar o schema do banco

---

## env.py

É o coração do Alembic: define como as migrations são executadas (offline/online).

Com a integração de métricas que adicionamos, você ganha observabilidade: quantas migrations rodaram, tempo de execução e falhas.

Isso ajuda a monitorar a saúde do ciclo de versionamento do banco, especialmente em ambientes com CI/CD.

init_schema.py

É a migration inicial que cria as tabelas base (customers, accounts, transactions).

Manter garante que o Alembic saiba de onde começa o histórico do banco.

Se você retirar, perde consistência: Alembic não terá referência da versão inicial.