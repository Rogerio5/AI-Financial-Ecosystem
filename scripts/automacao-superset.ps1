# automacao-superset.ps1
param(
  [string]$SUPERSET_ADMIN_USER = "admin",
  [string]$SUPERSET_ADMIN_PASS = "admin",
  [string]$SUPERSET_ADMIN_EMAIL = "admin@example.com"
)

Write-Host "1) Removendo superset.db do volume (se existir)..."
& docker run --rm -v bankpy_superset_data:/data alpine sh -c "rm -f /data/superset.db || true; ls -la /data"

Write-Host "2) Rodando migrações e init usando a imagem customizada (venv)..."
& docker run --rm --network bankpy_etl_net -v bankpy_superset_data:/app/superset_home `
  -e SUPERSET_HOME=/app/superset_home `
  -e SUPERSET_CONFIG_PATH=/app/superset_home/superset_config.py `
  -e SUPERSET_ENV=production custom-superset:latest /app/.venv/bin/superset db upgrade

& docker run --rm --network bankpy_etl_net -v bankpy_superset_data:/app/superset_home `
  -e SUPERSET_HOME=/app/superset_home `
  -e SUPERSET_CONFIG_PATH=/app/superset_home/superset_config.py `
  -e SUPERSET_ENV=production custom-superset:latest /app/.venv/bin/superset init

Write-Host "3) Subindo o serviço superset via docker-compose..."
& docker-compose up -d superset

Write-Host "4) Criando usuário admin (idempotente)..."
$exe = "docker"
$dockerArgs = @(
  "exec","-i","bankpy_superset",
  "/app/.venv/bin/superset","fab","create-admin",
  "--username",$SUPERSET_ADMIN_USER,
  "--firstname","Admin",
  "--lastname","Admin",
  "--email",$SUPERSET_ADMIN_EMAIL,
  "--password",$SUPERSET_ADMIN_PASS
)

try {
  Start-Process -FilePath $exe -ArgumentList $dockerArgs -NoNewWindow -Wait -PassThru | Out-Null
} catch {
  Write-Host "Aviso: create-admin retornou erro (provavelmente usuário já existe). Continuando..."
}

Write-Host "5) Reiniciando superset para garantir recarga de config..."
& docker restart bankpy_superset

Write-Host "Automação concluída. Acesse http://localhost:8089 e faça login com $SUPERSET_ADMIN_USER"
