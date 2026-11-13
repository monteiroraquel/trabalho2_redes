#!/usr/bin/env python3
# =====================================================================
# Trabalho 2 - Redes de Computadores 2  (Prof. Alessandro Vivas Andrade)
# Exercício 4 - Servidor de hora multithread (TCP)
#
# Grupo: Maria Eduarda Fernandes, Quezia Oliveira e Raquel Monteiro
# =====================================================================
"""
Servidor que informa a hora atual a vários clientes ao mesmo tempo.

  - O cliente envia o comando "HORA";
  - o servidor responde com a hora no formato HH:MM:SS;
  - um CONTADOR global guarda quantos clientes já foram atendidos.
    Como várias threads mexem nele ao mesmo tempo, ele é protegido por
    um threading.Lock (controle explícito de concorrência);
  - toda linha de log mostra data/hora, contador e cliente.

Como executar:
  python3 servidor.py --porta 7000
  (opcional: --atraso 2 simula demora para testar vários clientes juntos)
"""
import argparse
import socket
import threading
import time
from datetime import datetime

# Contador global de atendimentos e o lock que protege esse contador
total_atendidos = 0
trava = threading.Lock()


def hora_atual():
    # Data e hora completas, para os logs
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def somar_atendimento():
    # Incrementa o contador de forma thread-safe.
    # "total_atendidos = total_atendidos + 1" parece uma operação só, mas
    # na verdade é: LER o valor, SOMAR 1, GRAVAR. Se duas threads fizerem
    # isso ao mesmo tempo sem lock, as duas podem ler o MESMO valor e uma
    # contagem se perde (condição de corrida). O lock impede isso.
    global total_atendidos
    with trava:
        total_atendidos = total_atendidos + 1


def ler_contador():
    # Lê o valor atual também com o lock, para nunca pegar um valor "no meio"
    with trava:
        return total_atendidos


def registrar_log(cliente, texto):
    # Toda linha de log tem: data/hora, contador e o cliente (IP:porta).
    # flush=True força o texto a aparecer na hora, mesmo com várias threads.
    print("[" + hora_atual() + "]", "[atendidos:", ler_contador(), "]", cliente, "-", texto, flush=True)


def atender_cliente(conexao, endereco, atraso):
    # Roda em uma thread por cliente.
    cliente = endereco[0] + ":" + str(endereco[1])

    try:
        # Se o cliente não mandar nada em 30 segundos, desistimos dele.
        # Isso evita threads presas para sempre em clientes inativos.
        conexao.settimeout(30)

        # Lê o pedido do cliente. upper() faz "hora" e "HORA" funcionarem igual.
        pedido = conexao.recv(1024).decode("utf-8").strip().upper()
        registrar_log(cliente, "pedido recebido: " + pedido)

        if pedido == "HORA":
            if atraso > 0:
                # Só para teste: simula uma demora, assim dá para ver
                # vários clientes sendo atendidos em paralelo
                time.sleep(atraso)

            # Hora do servidor no formato pedido: HH:MM:SS
            hora = datetime.now().strftime("%H:%M:%S")
            conexao.sendall((hora + "\n").encode("utf-8"))

            # Só contamos como "atendido" depois de responder com sucesso
            somar_atendimento()
            registrar_log(cliente, "atendido, hora enviada: " + hora)
        else:
            conexao.sendall("ERRO: comando desconhecido, use HORA\n".encode("utf-8"))
            registrar_log(cliente, "comando inválido")

    except (socket.timeout, OSError) as erro:
        # Se um cliente falhar, só esta thread é afetada: o servidor
        # continua funcionando para os outros (exigência do exercício)
        registrar_log(cliente, "falha: " + str(erro))

    finally:
        conexao.close()


def main():
    parser = argparse.ArgumentParser(description="Servidor de hora")
    parser.add_argument("--host", default="0.0.0.0", help="endereço de escuta")
    parser.add_argument("--porta", type=int, default=7000, help="porta do servidor (padrão: 7000)")
    parser.add_argument("--atraso", type=float, default=0,
                        help="atraso (s) antes de responder, só para testes")
    args = parser.parse_args()

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((args.host, args.porta))
        servidor.listen()
        print("Servidor de hora ativo em", args.host, args.porta, "(Ctrl+C para parar)")

        while True:
            conexao, endereco = servidor.accept()
            # Uma thread por cliente; passamos o atraso como argumento extra
            thread = threading.Thread(target=atender_cliente, args=(conexao, endereco, args.atraso))
            thread.daemon = True
            thread.start()

    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
    except OSError as erro:
        print("Erro ao iniciar o servidor:", erro)
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
