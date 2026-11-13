#!/usr/bin/env python3
# =====================================================================
# Trabalho 2 - Redes de Computadores 2  (Prof. Alessandro Vivas Andrade)
# Exercício 1 - Cliente TCP
#
# Grupo: Maria Eduarda Fernandes, Quezia Oliveira e Raquel Monteiro
# =====================================================================
"""
Cliente TCP: conecta ao servidor, envia várias mensagens digitadas pelo
usuário e mostra a resposta de cada uma. Para terminar, digite "sair".

Como executar (com o servidor já rodando em outro terminal):
  python3 cliente.py --host 127.0.0.1 --porta 5000
"""
import argparse   # parâmetros da linha de comando
import socket     # comunicação em rede

TAMANHO_BUFFER = 4096  # máximo de bytes lidos por vez na resposta


def main():
    parser = argparse.ArgumentParser(description="Cliente TCP")
    parser.add_argument("--host", default="127.0.0.1",
                        help="IP do servidor (127.0.0.1 = este mesmo computador)")
    parser.add_argument("--porta", type=int, default=5000,
                        help="porta do servidor (padrão: 5000)")
    args = parser.parse_args()

    # Cria o socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect() tenta abrir a conexão com o servidor.
        # Se o servidor estiver desligado, lança ConnectionRefusedError.
        cliente.connect((args.host, args.porta))
        print("Conectado em", args.host, args.porta, "- digite 'sair' para encerrar")

        while True:
            # input() espera o usuário digitar; strip() tira espaços das pontas
            mensagem = input("Mensagem: ").strip()

            # Comando de saída: quebra o laço e vai para o finally
            if mensagem.lower() == "sair":
                break

            # Validação: não envia mensagem vazia (exigência do exercício)
            if mensagem == "":
                print("Digite alguma coisa antes de enviar.")
                continue

            # Envia a mensagem (texto -> bytes com encode)
            cliente.sendall(mensagem.encode("utf-8"))

            # Espera a resposta do servidor (fica parado até chegar algo)
            resposta = cliente.recv(TAMANHO_BUFFER)
            if not resposta:
                # recv() vazio = o servidor fechou a conexão
                print("O servidor fechou a conexão.")
                break
            print("Servidor:", resposta.decode("utf-8"))

    except ConnectionRefusedError:
        # Ninguém está ouvindo naquela porta (servidor desligado ou porta errada)
        print("Não foi possível conectar: o servidor está desligado ou a porta está errada.")
    except OSError as erro:
        # Outros problemas de rede (queda de conexão, endereço inválido...)
        print("Erro de rede:", erro)
    except (EOFError, KeyboardInterrupt):
        # Ctrl+D / Ctrl+C: encerra de forma educada
        print("\nEncerrando.")
    finally:
        # Sempre fecha o socket, aconteça o que acontecer
        cliente.close()
        print("Conexão encerrada.")


if __name__ == "__main__":
    main()
