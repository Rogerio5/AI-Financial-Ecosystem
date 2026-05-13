from sqlalchemy import inspect, text, create_engine
import sys, os

# tenta importar o modelo User
try:
    try:
        from airflow.models.user import User as AFUser
    except Exception:
        from airflow.models import User as AFUser
except Exception as e:
    print("ERRO: não foi possível importar User do Airflow:", e, file=sys.stderr)
    sys.exit(2)

print("User model table name:", AFUser.__table__.name)

db_url = os.environ.get("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN")
if not db_url:
    print("ERRO: AIRFLOW__DATABASE__SQL_ALCHEMY_CONN não encontrada", file=sys.stderr)
    sys.exit(3)

engine = create_engine(db_url)
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tabelas no DB (primeiras 50):", tables[:50])

if AFUser.__table__.name not in tables:
    print("A tabela do modelo User NÃO existe no banco:", AFUser.__table__.name)
    print("Rode: airflow db init  (ou restaure backup) e depois repita este script.")
    sys.exit(4)

# verificar se admin já existe
with engine.connect() as conn:
    res = conn.execute(text(f"SELECT id, username, email FROM {AFUser.__table__.name} WHERE username='admin' LIMIT 1")).fetchone()
    if res:
        print("Usuário admin já existe:", res)
        sys.exit(0)

# criar admin com hash pbkdf2_sha256
try:
    from passlib.hash import pbkdf2_sha256
    hashed = pbkdf2_sha256.hash("admin")
except Exception as e:
    print("Aviso: passlib não disponível ou falhou ao gerar hash:", e, file=sys.stderr)
    hashed = "admin"

try:
    with engine.begin() as conn:
        conn.execute(text(f"INSERT INTO {AFUser.__table__.name} (username, first_name, last_name, email, password, is_active) VALUES (:u,:fn,:ln,:e,:p,true)"),
                     {"u":"admin","fn":"Admin","ln":"Admin","e":"admin@example.com","p":hashed})
    print("Tentativa de inserir admin concluída. Verifique com SELECT na tabela.")
except Exception as e:
    print("Erro ao inserir admin:", e, file=sys.stderr)
    sys.exit(5)
