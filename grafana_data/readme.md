# 🔧 Passos que você executou

Banco de dados Postgres

Criou o banco grafana com usuário grafana_user e senha Engenharia10.

Confirmou a conexão via psql e verificou que o banco estava acessível.

Configuração do Grafana

Ajustou o grafana.ini para usar Postgres como backend:

ini
[database]
type = postgres
host = 127.0.0.1:5432
name = grafana
user = grafana_user
password = Engenharia10
ssl_mode = disable
Garantiu que o Grafana apontava para o banco correto.

Execução do Grafana

Inicialmente tentou rodar manualmente via PowerShell (grafana.exe server), mas descobriu que já havia um serviço Grafana ativo ocupando a porta 3000.

Identificou o processo com netstat e tasklist.

Confirmou que o Grafana estava rodando como serviço do Windows.

Port Forwarding na VM

Configurou o VirtualBox para expor o Grafana na porta 3001 (host → guest).

Isso permitiu acessar o Grafana externamente via <http://localhost:3001>.

Logs de inicialização

Conferiu os logs e viu mensagens como:

Código
INFO HTTP Server Listen address=[::]:3000
INFO All modules healthy
E depois:

Código
INFO Rendering dashboard via image renderer
Confirmando que o Grafana está rodando, conectado ao Postgres e pronto para renderizar dashboards.

🎯 Resultado
O Grafana está rodando como serviço do Windows, acessível na porta 3001 via VM.

O banco de dados Postgres está configurado corretamente.

Os módulos principais estão saudáveis, e os logs mostram que o sistema está ativo.

Agora você pode criar dashboards e eles serão salvos no Postgres.

## 📊 Em resumo

 Foi configurado Postgres, ajustou o grafana.ini, resolveu o conflito de porta com o serviço do Windows, configurou o VirtualBox para expor a porta 3001 e confirmou nos logs que o Grafana está rodando com sucesso.
