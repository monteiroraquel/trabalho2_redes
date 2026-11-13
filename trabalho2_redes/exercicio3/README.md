# Exercício 3 — Chat em rede (TCP)

Requisitos: Python 3.10+ (apenas biblioteca padrão).

## Como executar

Terminal 1 (servidor):
```bash
python3 servidor.py --porta 5001
```
Terminais 2, 3, 4... (um por usuário):
```bash
python3 cliente.py --host 127.0.0.1 --porta 5001
```
Cada cliente pede um nickname (sem espaços, único). As mensagens são enviadas aos demais no formato `[nick] texto`,
e o servidor avisa quando alguém entra ou sai. Digite `sair` para sair sem derrubar o servidor nem os outros clientes.
