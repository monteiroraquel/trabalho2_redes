#!/usr/bin/env python3
# =====================================================================
# Trabalho 2 - Redes de Computadores 2  (Prof. Alessandro Vivas Andrade)
# Exercício 10 - Cliente de chat WebSocket (Python)
#
# Grupo: Maria Eduarda Fernandes, Quezia Oliveira e Raquel Monteiro
# =====================================================================
"""
Cliente de chat em Python usando a biblioteca "websockets".
Digite mensagens e tecle Enter. Para sair, digite "sair".

Como executar (com o servidor já rodando):
  pip install websockets
  python3 cliente.py --host 127.0.0.1 --porta 8765 --nome Maria
"""
import argparse
import asyncio

import websockets
from websockets.exceptions import ConnectionClosed


async def receber_mensagens(ws):
    # Fica em segundo plano mostrando tudo o que o servidor enviar
    try:
        async for mensagem in ws:
            # "\r" evita misturar a mensagem recebida com o que está sendo digitado
            print("\r" + mensagem)
    except ConnectionClosed:
        pass  # servidor fechou a conexão: fim normal
    print("[Conexão encerrada. Pressione Enter para sair.]")


async def conversar(endereco, nome):
    try:
        # "async with" abre a conexão e a fecha sozinho no final
        async with websockets.connect(endereco) as ws:
            # Protocolo: a primeira mensagem enviada é o nome de usuário
            await ws.send(nome)

            # create_task() roda o recebimento "ao mesmo tempo" que o teclado
            # (é o equivalente assíncrono da segunda thread do exercício 3)
            tarefa = asyncio.create_task(receber_mensagens(ws))

            while not tarefa.done():
                # input() trava a execução, então rodamos ele em outra thread
                # (to_thread) para o recebimento continuar funcionando.
                texto = await asyncio.to_thread(input, "")
                texto = texto.strip()

                if tarefa.done() or texto.lower() == "sair":
                    break
                if texto != "":
                    await ws.send(texto)

            tarefa.cancel()  # encerra a tarefa de recebimento

    except OSError as erro:
        # Servidor desligado, endereço errado, sem rede...
        print("Não foi possível conectar em", endereco, "->", erro)
    except websockets.exceptions.WebSocketException as erro:
        print("Erro no WebSocket:", erro)

    print("Você saiu do chat.")


def main():
    parser = argparse.ArgumentParser(description="Cliente de chat WebSocket")
    parser.add_argument("--host", default="127.0.0.1", help="IP do servidor")
    parser.add_argument("--porta", type=int, default=8765, help="porta do servidor (padrão: 8765)")
    parser.add_argument("--nome", default="", help="nome de usuário (se vazio, será perguntado)")
    args = parser.parse_args()

    # Garante que o nome não fique vazio
    nome = args.nome.strip()
    while nome == "":
        nome = input("Nome de usuário: ").strip()

    # Endereço WebSocket: "ws://" é o equivalente de "http://"
    endereco = "ws://" + args.host + ":" + str(args.porta)

    try:
        asyncio.run(conversar(endereco, nome))
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando.")


if __name__ == "__main__":
    main()
