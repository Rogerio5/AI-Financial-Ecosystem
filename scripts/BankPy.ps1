# BankPy.ps1 - Script de automação para ambiente Dev/BankPy

param(
    [string]$Action = "help"
)

function Up {
    Write-Host "🔧 Subindo ambiente com docker-compose..."
    docker-compose up -d --build
}

function Down {
    Write-Host "🛑 Derrubando containers..."
    docker-compose down
}

function Logs {
    Write-Host "📜 Logs da aplicação..."
    docker-compose logs -f app
}

function Seed {
    Write-Host "🌱 Aplicando seed no banco..."
    docker-compose run --rm app python cli.py seed
}

function Etl {
    Write-Host "📊 Rodando ETL e exportando CSV..."
    docker-compose run --rm app python cli.py gerar-etl
}

function Test {
    Write-Host "🧪 Executando testes..."
    docker-compose run --rm app pytest -v
}

function Clean {
    Write-Host "🧹 Limpando containers, volumes e imagens..."
    docker-compose down -v --rmi all --remove-orphans
}

function Help {
    Write-Host "Comandos disponíveis:"
    Write-Host "  .\BankPy.ps1 up     -> subir ambiente"
    Write-Host "  .\BankPy.ps1 down   -> derrubar ambiente"
    Write-Host "  .\BankPy.ps1 logs   -> ver logs da aplicação"
    Write-Host "  .\BankPy.ps1 seed   -> aplicar seed no banco"
    Write-Host "  .\BankPy.ps1 etl    -> rodar ETL e gerar CSV"
    Write-Host "  .\BankPy.ps1 test   -> rodar testes"
    Write-Host "  .\BankPy.ps1 clean  -> limpar tudo"
}

switch ($Action) {
    "up"    { Up }
    "down"  { Down }
    "logs"  { Logs }
    "seed"  { Seed }
    "etl"   { Etl }
    "test"  { Test }
    "clean" { Clean }
    default { Help }
}
