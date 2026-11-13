# Exercício 1 — Cliente-Servidor TCP

Requisitos: Python 3.10+ (apenas biblioteca padrão, sem dependências extras).

## Como executar

Terminal 1 (servidor):
```bash
python3 servidor.py --porta 5000
```
Terminal 2, 3, ... (clientes — podem ser vários ao mesmo tempo):
```bash
python3 cliente.py --host 127.0.0.1 --porta 5000
```

Parâmetros: `--host` (servidor: padrão `0.0.0.0`; cliente: padrão `127.0.0.1`) e `--porta` (padrão `5000`).

Digite mensagens no cliente e veja a confirmação "Mensagem recebida". Digite `sair` para encerrar.
Mensagens vazias são rejeitadas pelo cliente. Se o servidor estiver desligado, o cliente mostra uma mensagem de "conexão recusada".
