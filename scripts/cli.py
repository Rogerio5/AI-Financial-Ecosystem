import typer
import subprocess
from sqlalchemy import text
from bankpy.db import SessionLocal
from bankpy.crud import create_customer, create_account, deposit, withdraw, transfer
import scripts.etl_db as etl

app = typer.Typer()

@app.command()
def init_db():
    """Aplica migrations via Alembic."""
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    typer.echo("✅ Schema atualizado via Alembic.")

@app.command()
def seed():
    """Popula dados iniciais no banco."""
    import scripts.seed_db as s
    s.run_seed()

@app.command()
def listar_clientes():
    """Lista todos os clientes cadastrados."""
    with SessionLocal() as db:
        rows = db.execute(text("SELECT cpf, name, email FROM customers")).all()
        for r in rows:
            typer.echo(f"{r.name} | CPF: {r.cpf} | Email: {r.email}")

@app.command()
def criar_cliente(nome: str, cpf: str, email: str = ""):
    """Cria um novo cliente."""
    with SessionLocal() as db:
        try:
            create_customer(db, nome, cpf, email)
            typer.echo(f"✅ Cliente {nome} criado.")
        except Exception as e:
            typer.echo(f"❌ Erro: {e}")

@app.command()
def abrir_conta(account_id: str, cpf: str, saldo_inicial: float = 0.0):
    """Abre uma nova conta para um cliente."""
    with SessionLocal() as db:
        try:
            create_account(db, account_id, cpf, saldo_inicial)
            typer.echo(f"✅ Conta {account_id} aberta para {cpf}.")
        except Exception as e:
            typer.echo(f"❌ Erro: {e}")

@app.command()
def depositar(account_id: str, amount: float):
    """Realiza um depósito em uma conta."""
    with SessionLocal() as db:
        try:
            deposit(db, account_id, amount, "deposit via CLI")
            typer.echo(f"✅ Depósito de {amount:.2f} realizado.")
        except Exception as e:
            typer.echo(f"❌ Erro: {e}")

@app.command()
def sacar(account_id: str, amount: float):
    """Realiza um saque em uma conta."""
    with SessionLocal() as db:
        try:
            withdraw(db, account_id, amount, "saque via CLI")
            typer.echo(f"✅ Saque de {amount:.2f} realizado.")
        except Exception as e:
            typer.echo(f"❌ Erro: {e}")

@app.command()
def transferir(from_id: str, to_id: str, amount: float):
    """Transfere valores entre contas."""
    with SessionLocal() as db:
        try:
            transfer(db, from_id, to_id, amount, "transfer via CLI")
            typer.echo(f"✅ Transferência de {amount:.2f} realizada.")
        except Exception as e:
            typer.echo(f"❌ Erro: {e}")

@app.command()
def gerar_etl():
    """Exporta transações para CSV via ETL."""
    try:
        etl.run_etl()
        typer.echo("✅ ETL concluído. Arquivo CSV gerado em data/transactions_flat.csv")
    except Exception as e:
        typer.echo(f"❌ Erro ao rodar ETL: {e}")

if __name__ == "__main__":
    app()
