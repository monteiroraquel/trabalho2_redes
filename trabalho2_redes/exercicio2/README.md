# Exercício 2 — Servidor Echo UDP

Requisitos: Python 3.10+ (apenas biblioteca padrão).

## Como executar

Terminal 1:
```bash
python3 servidor.py --porta 6000
```
Terminal 2:
```bash
python3 cliente.py --host 127.0.0.1 --porta 6000 --timeout 3
```

Parâmetros: `--host`, `--porta` (padrão `6000`) e, no cliente, `--timeout` (segundos, padrão `3`).

- Mensagens maiores que 65.507 bytes são recusadas pelo cliente.
- Se o servidor não responder dentro do tempo limite, o cliente avisa e continua.
- Digite `sair` para encerrar.
