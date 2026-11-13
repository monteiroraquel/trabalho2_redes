#!/usr/bin/env python3
# =====================================================================
# Trabalho 2 - Redes de Computadores 2  (Prof. Alessandro Vivas Andrade)
# Exercício 10 - Servidor de chat com WebSockets
#
# Grupo: Maria Eduarda Fernandes, Quezia Oliveira e Raquel Monteiro
# =====================================================================
"""
Servidor de chat com WebSockets (biblioteca "websockets").

O WebSocket é uma conexão que fica ABERTA e permite comunicação nos dois
sentidos: o servidor pode enviar mensagens para os clientes a qualquer
momento, sem o cliente precisar pedir (diferente do HTTP comum).

Protocolo do nosso chat:
  - a primeira mensagem de cada cliente é o NOME DE USUÁRIO;
  - as mensagens seguintes são repassadas (broadcast) aos outros clientes
    no formato "[nome] texto".

Diferença para os exercícios anteriores: aqui usamos asyncio em vez de
threads. Cada cliente é uma "corrotina" (async def): enquanto uma espera
dados ("await"), o Python aproveita para atender as outras.

Como executar:
  pip install websockets
  python3 servidor.py --porta 8765
"""
import argparse
import asyncio

import websockets                                   # biblioteca de WebSockets
from websockets.exceptions import ConnectionClosed  # erro de conexão encerrada

# Clientes conectados: {websocket: nome_de_usuario}
clientes = {}


async def enviar_para_todos(texto, quem_enviou=None):
    # Envia 'texto' para todos os clientes, exceto 'quem_enviou'.

    # Monta a lista de destinatários (todos menos quem enviou).
    # list(...) faz uma cópia, pois o dicionário pode mudar durante o envio.
    destinos = []
    for ws in list(clientes.keys()):
        if ws != quem_enviou:
            destinos.append(ws)

    # gather() envia para todos ao mesmo tempo.
    # return_exceptions=True: se um cliente tiver problema, os outros
    # continuam recebendo normalmente (o erro não derruba o servidor).
    if len(destinos) > 0:
        await asyncio.gather(*(ws.send(texto) for ws in destinos), return_exceptions=True)


async def atender_cliente(websocket):
    # Esta corrotina roda uma vez para cada cliente conectado.
    nome = None

    try:
        # A primeira mensagem recebida é o nome do usuário.
        # "await" = espera chegar, sem travar os outros clientes.
        nome = (await websocket.recv()).strip()

        # Valida o nome (não vazio e até 20 caracteres)
        if nome == "" or len(nome) > 20:
            await websocket.send("ERRO: nome inválido (1 a 20 caracteres)")
            await websocket.close()
            nome = None
            return

        # Não permite dois usuários com o mesmo nome
        if nome in clientes.values():
            await websocket.send("ERRO: esse nome já está em uso")
            await websocket.close()
            nome = None
            return

        # Registra o cliente e avisa os outros que ele entrou
        clientes[websocket] = nome
        print(nome, "entrou. Online:", len(clientes))
        await websocket.send("Bem-vindo(a), " + nome + "!")
        await enviar_para_todos("*** " + nome + " entrou na sala ***", websocket)

        # Recebe mensagens até o cliente sair. O "async for" termina sozinho
        # quando a conexão é fechada.
        async for mensagem in websocket:
            mensagem = mensagem.strip()
            if mensagem != "":
                # Retransmite para os demais, identificando o remetente
                await enviar_para_todos("[" + nome + "] " + mensagem, websocket)

    except ConnectionClosed:
        # Cliente fechou a aba ou a conexão caiu de repente.
        # É um evento normal (desconexão inesperada), não derruba o servidor.
        pass
    except Exception as erro:
        # Qualquer outro erro inesperado também fica restrito a este cliente
        print("Erro com o cliente", nome, "->", erro)

    finally:
        # Limpeza: se o cliente estava registrado, remove e avisa os outros
        if websocket in clientes:
            del clientes[websocket]
            print(nome, "saiu. Online:", len(clientes))
            await enviar_para_todos("*** " + nome + " saiu da sala ***")


async def iniciar(host, porta):
    # "async with" abre o servidor e garante o fechamento ao final
    async with websockets.serve(atender_cliente, host, porta):
        print("Servidor WebSocket ativo em ws://" + host + ":" + str(porta), "(Ctrl+C para parar)")
        await asyncio.Future()  # um Future que nunca termina: mantém o servidor rodando


def main():
    parser = argparse.ArgumentParser(description="Servidor de chat WebSocket")
    parser.add_argument("--host", default="0.0.0.0", help="endereço de escuta")
    parser.add_argument("--porta", type=int, default=8765, help="porta do servidor (padrão: 8765)")
    args = parser.parse_args()

    try:
        # asyncio.run() inicia o "motor" assíncrono e executa o servidor
        asyncio.run(iniciar(args.host, args.porta))
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
    except OSError as erro:
        # Ex.: porta já está em uso
        print("Erro ao iniciar o servidor:", erro)


if __name__ == "__main__":
    main()
