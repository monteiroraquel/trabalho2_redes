#!/usr/bin/env python3
# =====================================================================
# Trabalho 2 - Redes de Computadores 2  (Prof. Alessandro Vivas Andrade)
# Exercício 2 - Cliente Echo UDP
#
# Grupo: Maria Eduarda Fernandes, Quezia Oliveira e Raquel Monteiro
# =====================================================================
"""
Cliente UDP: envia mensagens ao servidor e mostra o eco recebido.

Cuidados específicos do UDP tratados aqui:
  - o tamanho da mensagem não pode passar de 65.507 bytes;
  - o UDP não garante entrega, então usamos TIMEOUT para não ficar
    esperando para sempre por uma resposta que pode ter se perdido.

Como executar (com o servidor já rodando):
  python3 cliente.py --host 127.0.0.1 --porta 6000 --timeout 3
Digite "sair" para encerrar.
"""
import argparse
import socket

# Maior payload possível de um datagrama UDP sobre IPv4 (65535 - 20 - 8)
TAMANHO_MAXIMO = 65507


def main():
    parser = argparse.ArgumentParser(description="Cliente Echo UDP")
    parser.add_argument("--host", default="127.0.0.1", help="IP do servidor")
    parser.add_argument("--porta", type=int, default=6000, help="porta do servidor")
    parser.add_argument("--timeout", type=float, default=3.0,
                        help="segundos de espera pela resposta (padrão: 3)")
    args = parser.parse_args()

    # Socket UDP (SOCK_DGRAM). Não há connect(): enviamos direto com sendto().
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Como o UDP não garante entrega, definimos um tempo máximo de espera.
    # Sem isso, o recvfrom() ficaria travado para sempre se o pacote se perdesse.
    # Quando o tempo acaba, o Python lança socket.timeout.
    cliente.settimeout(args.timeout)

    print("Enviando para", args.host, args.porta, "- digite 'sair' para encerrar")

    try:
        while True:
            mensagem = input("Mensagem: ")

            if mensagem.strip().lower() == "sair":
                break

            if mensagem.strip() == "":
                print("Digite alguma coisa antes de enviar.")
                continue

            # Transforma o texto em bytes para poder enviar pela rede
            dados = mensagem.encode("utf-8")

            # Validação do tamanho: o UDP não aceita mais que 65507 bytes.
            # Medimos em BYTES (len(dados)), não em caracteres, porque
            # letras acentuadas ocupam mais de 1 byte em UTF-8.
            if len(dados) > TAMANHO_MAXIMO:
                print("Mensagem grande demais:", len(dados), "bytes (máximo", TAMANHO_MAXIMO, ")")
                continue

            try:
                # Envia o datagrama para o servidor
                cliente.sendto(dados, (args.host, args.porta))
                # Espera o eco (até estourar o timeout)
                eco, _ = cliente.recvfrom(TAMANHO_MAXIMO + 1)
                print("Eco:", eco.decode("utf-8", errors="replace"))
            except socket.timeout:
                print("Sem resposta em", args.timeout, "segundos.")
            except ConnectionRefusedError:
                # O sistema recebeu um aviso ICMP de "porta fechada"
                print("Servidor inacessível (porta fechada).")
            except OSError as erro:
                print("Erro de comunicação:", erro)

    except (EOFError, KeyboardInterrupt):
        print("\nEncerrando.")
    finally:
        cliente.close()
        print("Cliente encerrado.")


if __name__ == "__main__":
    main()
