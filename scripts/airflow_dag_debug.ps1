# scripts/airflow_dag_debug.ps1
param(
  [string]$WEB_CONTAINER = "airflow_webserver",
  [string]$SCHEDULER_SERVICE = "airflow_scheduler",
  [string]$DAG_ID = "",
  [string]$TASK_ID = "",
  [string]$EXEC_DATE = "2026-03-25T00:00:00",
  [string]$CONN_ID = "conn_postgres",
  [string]$CONN_URI = "postgresql+psycopg2://user:pass@db:5432/airflow29",
  [string]$VAR_KEY = "my_var",
  [string]$VAR_VAL = "valor"
)

function Run-ListDags {
  Write-Host "== Listando DAGs =="
  & docker exec -it $WEB_CONTAINER airflow dags list
}

function Run-TestTask {
  if (-not $DAG_ID -or -not $TASK_ID) {
    Write-Host "Use -DAG_ID e -TASK_ID para testar uma task."
    return
  }
  Write-Host "== Testando task $TASK_ID do DAG $DAG_ID para $EXEC_DATE =="
  & docker exec -it $WEB_CONTAINER airflow tasks test $DAG_ID $TASK_ID $EXEC_DATE
}

function Run-TriggerDag {
  if (-not $DAG_ID) {
    Write-Host "Use -DAG_ID para disparar um DAG."
    return
  }
  Write-Host "== Disparando DAG $DAG_ID =="
  & docker exec -it $WEB_CONTAINER airflow dags trigger $DAG_ID
}

function Run-ShowLogs {
  if (-not $DAG_ID -or -not $TASK_ID) {
    Write-Host "Use -DAG_ID e -TASK_ID para ver logs de task."
    return
  }
  Write-Host "== Mostrando logs do scheduler e do webserver (últimas linhas) =="
  docker-compose logs --tail=200 --no-color $SCHEDULER_SERVICE
  docker-compose logs --tail=200 --no-color $WEB_CONTAINER
  Write-Host "== Listando arquivos de log da task =="
  & docker exec -it $WEB_CONTAINER bash -lc "ls -la /opt/airflow/logs/$DAG_ID/$TASK_ID || true"
}

function Run-CreateConnection {
  Write-Host "== Criando conexão $CONN_ID =="
  & docker exec -it $WEB_CONTAINER airflow connections add $CONN_ID --conn-uri "$CONN_URI"
}

function Run-SetVariable {
  Write-Host "== Definindo variável $VAR_KEY = $VAR_VAL =="
  & docker exec -it $WEB_CONTAINER airflow variables set $VAR_KEY "$VAR_VAL"
}

# Menu simples
Write-Host "Airflow DAG debug helper"
Write-Host "Opções: list | test | trigger | logs | conn | var"
$choice = Read-Host "Escolha uma opção"
switch ($choice) {
  "list"   { Run-ListDags }
  "test"   { Run-TestTask }
  "trigger"{ Run-TriggerDag }
  "logs"   { Run-ShowLogs }
  "conn"   { Run-CreateConnection }
  "var"    { Run-SetVariable }
  default  { Write-Host "Opção inválida." }
}
