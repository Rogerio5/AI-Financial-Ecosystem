# 📂 CI/CD - GitHub Actions para BankPy

Este projeto utiliza **GitHub Actions** para automatizar o processo de build, testes e publicação da imagem Docker do BankPy.

---

## 📌 Arquivo `ci.yml`

### Disparadores

- **Push** para a branch `master`.
- **Pull Request** para a branch `master`.
- **Tags** no formato `vX.Y.Z` (exemplo: `v1.0.0`).

---

## 📌 Jobs

### 1. `build-and-test`

Executa o ciclo completo de build, seed, ETL e testes.

Etapas:

1. **Checkout** → baixa o repositório.
2. **Set up Docker Buildx** → prepara ambiente para build multi-plataforma.
3. **Build and start services** → sobe os containers com `docker compose up -d --build`.
4. **Apply seed** → popula dados iniciais no banco (`cli.py seed`).
5. **Run ETL** → exporta transações para CSV (`cli.py gerar-etl`).
6. **Run tests** → executa testes com `pytest -v`.
7. **Shutdown** → derruba os containers (`docker compose down`).

---

### 2. `publish-docker`

Publica a imagem Docker no Docker Hub **apenas se os testes passarem**.

Etapas:

1. **Checkout** → baixa o repositório.
2. **Set up Docker Buildx** → prepara ambiente.
3. **Login no Docker Hub** → usa secrets configurados no repositório.
4. **Build and push Docker image** → publica a imagem com duas tags:
   - `latest`
   - `${{ github.ref_name }}` (nome da tag criada, ex: `v1.0.0`)

---

## 📌 Configuração de Secrets

No repositório do GitHub, vá em **Settings > Secrets and variables > Actions** e configure:

- `DOCKERHUB_USERNAME` → seu usuário no Docker Hub.
- `DOCKERHUB_TOKEN` → token de acesso gerado no Docker Hub.

---

## 📌 Arquitetura resumida

O fluxo de dados do projeto BankPy é:

```PostgreSQL → Airflow (ETL) → MongoDB → Redis
```

- **Postgres**: fonte de dados estruturados (clientes, transações).  
- **Airflow**: orquestração do ETL (extração, transformação, carga).  
- **MongoDB**: armazenamento documental flexível.  
- **Redis**: cache em memória com TTL para consultas rápidas.  

---

## 📌 Comandos usados

- **Subir containers**:

  ```bash
  docker compose up -d --build

## Derrubar containers

```docker compose down
