#!/usr/bin/env python3
# =====================================================================
# Trabalho 2 - Redes de Computadores 2  (Prof. Alessandro Vivas Andrade)
# Exercício 4 - Cliente do servidor de hora
#
# Grupo: Maria Eduarda Fernandes, Quezia Oliveira e Raquel Monteiro
# =====================================================================
"""
Cliente simples: conecta ao servidor, pede a hora e mostra a resposta.

Como executar (com o servidor já rodando):
  python3 cliente.py --host 127.0.0.1 --porta 7000
"""
import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description="Cliente do servidor de hora")
    parser.add_argument("--host", default="127.0.0.1", help="IP do servidor")
    parser.add_argument("--porta", type=int, default=7000, help="porta do servidor (padrão: 7000)")
    args = parser.parse_args()

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Tempo máximo de espera (conexão e resposta): 5 segundos.
    # Sem isso, o cliente poderia ficar travado se o servidor não respondesse.
    cliente.settimeout(5)

    try:
        cliente.connect((args.host, args.porta))
        # Protocolo do servidor: o pedido é a palavra HORA
        cliente.sendall("HORA\n".encode("utf-8"))
        resposta = cliente.recv(1024).decode("utf-8").strip()
        print("Hora do servidor:", resposta)

    except ConnectionRefusedError:
        print("Servidor indisponível.")
    except socket.timeout:
        print("O servidor demorou demais para responder.")
    except OSError as erro:
        print("Erro de rede:", erro)
    finally:
        # Sempre fecha o socket, mesmo se der erro
        cliente.close()


if __name__ == "__main__":
    main()
