# Exercício 10 — Chat com WebSockets

Requisitos: Python 3.10+ e a biblioteca `websockets`.

## Instalação
```bash
pip install -r requirements.txt     # ou: pip install websockets
```

## Como executar

Terminal 1 (servidor):
```bash
python3 servidor.py --porta 8765
```

Cliente Python (um terminal por usuário):
```bash
python3 cliente.py --host 127.0.0.1 --porta 8765 --nome Maria
```

Cliente web: abra `cliente.html` no navegador, confira a URL (`ws://localhost:8765`), informe seu nome e clique em **Entrar**.
Os clientes Python e web conversam entre si. Mensagens aparecem como `[nome] texto`; entradas e saídas são avisadas.
Desconexões inesperadas não derrubam o servidor.
