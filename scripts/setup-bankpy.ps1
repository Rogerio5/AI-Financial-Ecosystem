# Sobe apenas o banco
docker-compose up -d db

# Aguarda alguns segundos para o banco ficar saudável
Start-Sleep -Seconds 10

# Aplica migrations
docker-compose run --rm app python cli.py init-db

# Popula dados iniciais
docker-compose run --rm app python cli.py seed

# Lista clientes para confirmar
docker-compose run --rm app python cli.py listar-clientes

# (Opcional) roda ETL
docker-compose run --rm app python cli.py gerar-etl
