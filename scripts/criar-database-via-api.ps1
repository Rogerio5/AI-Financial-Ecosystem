# criar-database-via-api.ps1
$SUP_URL = "http://localhost:8089"
$ADMIN_USER = "admin"
$ADMIN_PASS = "admin"
$DB_NAME = "airflow29"
$SQLALCHEMY_URI = "postgresql+psycopg2://user:password@host:5432/airflow29"

# 1) Autenticar e obter token (ajuste payload conforme sua versão do Superset)
$loginBody = @{ username = $ADMIN_USER; password = $ADMIN_PASS; provider = "db"; refresh = $true } | ConvertTo-Json
$loginResp = Invoke-RestMethod -Method Post -Uri "$SUP_URL/api/v1/security/login" -Body $loginBody -ContentType "application/json"
$access_token = $loginResp.access_token

# 2) Criar Database (payload de exemplo; adapte campos conforme versão)
$createBody = @{
  database_name = $DB_NAME
  sqlalchemy_uri = $SQLALCHEMY_URI
  expose_in_sqllab = $true
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "$SUP_URL/api/v1/database/" -Headers @{ Authorization = "Bearer $access_token" } -Body $createBody -ContentType "application/json"
