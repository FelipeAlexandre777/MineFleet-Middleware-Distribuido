# MineFleet — Middleware Distribuído para Monitoramento de Caminhões de Mineração

Projeto acadêmico da disciplina **Sistemas Distribuídos**, Bacharelado em Sistemas de Informação, IFMG — Campus Ouro Branco.

## Objetivo
Simular o monitoramento da temperatura de caminhões de mineração, demonstrando MQTT, middleware, replicação de dados, quórum e verificação de integridade.

## Tecnologias
Python, FastAPI, Eclipse Mosquitto, Paho-MQTT, SQLite, HMAC-SHA256 e Docker Compose.

## Arquitetura
- Sensor publica telemetria no tópico `minefleet/caminhoes/telemetria`.
- Broker Mosquitto distribui mensagens MQTT.
- Middleware FastAPI coordena quatro réplicas lógicas.
- Cada controlador mantém um arquivo SQLite independente.
- As respostas são verificadas por HMAC e comparadas.
- Três respostas iguais (quórum 3/4) aprovam o resultado.
- Temperatura igual ou superior a 80 °C gera indicação de alerta.

## Como executar no Windows
1. Instale Python 3.10+, Docker Desktop, Git e VS Code.
2. Extraia a pasta e abra `MineFleet` no VS Code.
3. Abra o Docker Desktop e, no terminal do VS Code, execute:
   ```powershell
   docker compose up -d
   ```
4. Crie o ambiente virtual:
   ```powershell
   py -m venv .venv
   ```
5. Ative:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   Se houver bloqueio:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```
6. Instale as dependências:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
7. Inicie a API:
   ```powershell
   python -m uvicorn app.main:app --reload
   ```
8. Abra http://127.0.0.1:8000/docs.

## Teste normal
Na documentação, abra `POST /telemetry`, clique em **Try it out**, use e execute:
```json
{"vehicle_id":"CAM-042","sequence":1,"temperature":85}
```
O esperado é `success: true` e `Quórum aprovado: 4/4`.

## Teste de queda de controlador
Em `POST /controllers/controlador-4/simulate`, envie:
```json
{"online":false}
```
Repita `POST /telemetry`. Esperado: quórum 3/4 aprovado. Restaure com `POST /controllers/restore` e `{}`.

## Teste de divergência
Em `POST /controllers/controlador-4/simulate`, envie:
```json
{"divergent":true}
```
Envie uma telemetria com temperatura 85. Os três controladores restantes devem concordar. Restaure com `POST /controllers/restore` e `{}`.

## Sensor e atuador MQTT
Com o broker ativo, em terminais separados execute:
```powershell
python sensor.py
```
e
```powershell
python atuador.py
```
O sensor publica telemetria no broker. O atuador assina o tópico de alertas. Nesta versão, a decisão do middleware ocorre pela API HTTP; o sensor e o atuador demonstram o publish/subscribe MQTT.

## Endpoints
| Método | Rota | Finalidade |
|---|---|---|
| GET | `/` | Verificar API |
| GET | `/controllers` | Estado das réplicas |
| POST | `/telemetry` | Processar dados e aplicar quórum |
| POST | `/controllers/{controller_id}/simulate` | Simular falha ou divergência |
| POST | `/controllers/restore` | Restaurar controladores |

## Limitações importantes
Protótipo acadêmico local. Os quatro controladores são instâncias lógicas dentro do processo da API, não quatro máquinas/serviços independentes. A decisão de quórum ocorre na API HTTP. MQTT é usado pelos programas de sensor e atuador para demonstrar publicação e assinatura. HMAC usa segredo didático local e não representa segurança de produção. O quórum 3/4 tolera uma réplica indisponível e identifica uma resposta divergente quando as outras três concordam; não é protocolo formal de tolerância a falhas bizantinas.

## Encerrar
Pare a API com `Ctrl+C` e o broker com:
```powershell
docker compose down
```

**IFMG — Campus Ouro Branco | Sistemas Distribuídos**
