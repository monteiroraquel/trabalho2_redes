# Exercício 4 — Servidor de hora com threads (TCP)

Requisitos: Python 3.10+ (apenas biblioteca padrão).

## Como executar

Terminal 1 (servidor):
```bash
python3 servidor.py --porta 7000
# opcional, para demonstrar atendimento paralelo: --atraso 2
```
Terminal 2 (cliente, pode ser executado várias vezes ao mesmo tempo):
```bash
python3 cliente.py --host 127.0.0.1 --porta 7000
```
O cliente envia `HORA` e mostra a resposta `HH:MM:SS`. Cada linha de log do servidor traz data/hora, cliente (IP:porta) e o
contador de atendimentos (`threading.Lock`). Falhas de um cliente não derrubam o servidor.

Teste de concorrência (5 clientes em paralelo, com `--atraso 2` no servidor):
```bash
for i in 1 2 3 4 5; do python3 cliente.py & done; wait
```
