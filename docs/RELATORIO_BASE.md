# Relatório — MineFleet

## 1. Introdução
O MineFleet é um protótipo acadêmico de middleware para monitoramento da temperatura de caminhões em uma operação de mineração.

## 2. Arquitetura
O sensor publica telemetria por MQTT. O broker Mosquitto distribui as mensagens. A API FastAPI atua como middleware e coordena quatro instâncias lógicas de controladores, cada uma com banco SQLite próprio.

## 3. Replicação e disponibilidade
Os controladores armazenam os registros em arquivos SQLite separados. O middleware exige três respostas iguais (quórum 3/4), permitindo concluir a operação quando uma réplica está indisponível.

## 4. Integridade e divergência
As respostas incluem assinatura HMAC-SHA256. O middleware verifica a assinatura e compara os resultados. A solução identifica uma resposta divergente quando as outras três concordam. Não constitui protocolo formal de tolerância a falhas bizantinas.

## 5. Testes
Preencher com os resultados realmente observados:
- Execução normal;
- Queda simulada de um controlador;
- Resposta divergente simulada;
- Restauração das réplicas.
Adicionar capturas de tela da execução e da página `/docs`.

## 6. Limitações
Os controladores são instâncias lógicas dentro do processo da API, não serviços em máquinas separadas. Sensor e atuador demonstram MQTT; a decisão de quórum ocorre pela API HTTP. HMAC utiliza segredo didático local.

## 7. Conclusão
O protótipo demonstra middleware, MQTT, replicação, quórum, integridade e simulação de falhas.
