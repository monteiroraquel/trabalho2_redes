#!/usr/bin/env python3
# =====================================================================
# Trabalho 2 - Redes de Computadores 2  (Prof. Alessandro Vivas Andrade)
# Exercício 2 - Servidor Echo UDP
#
# Grupo: Maria Eduarda Fernandes, Quezia Oliveira e Raquel Monteiro
# =====================================================================
"""
Servidor de eco UDP: tudo que chega é devolvido para quem enviou.

Diferenças em relação ao TCP:
  - No UDP NÃO existe conexão (sem connect/listen/accept). Cada mensagem
    é um "datagrama" independente, que pode até se perder.
  - Por isso usamos recvfrom(), que devolve os dados E o endereço de
    quem enviou, e sendto(), onde dizemos para quem vamos responder.

Como executar:
  python3 servidor.py --porta 6000
"""
import argparse
import socket

# Maior payload possível de um datagrama UDP sobre IPv4:
# 65535 (máximo do IP) - 20 (cabeçalho IP) - 8 (cabeçalho UDP) = 65507
TAMANHO_MAXIMO = 65507


def main():
    parser = argparse.ArgumentParser(description="Servidor Echo UDP")
    parser.add_argument("--host", default="0.0.0.0",
                        help="endereço de escuta (0.0.0.0 = todas as interfaces)")
    parser.add_argument("--porta", type=int, default=6000,
                        help="porta do servidor (padrão: 6000)")
    args = parser.parse_args()

    # SOCK_DGRAM = UDP (datagramas). Compare com SOCK_STREAM do TCP.
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # bind() reserva a porta. No UDP não precisamos de listen().
        servidor.bind((args.host, args.porta))
        print("Servidor echo UDP ativo em", args.host, args.porta, "(Ctrl+C para parar)")

        while True:
            try:
                # recvfrom() espera um datagrama e devolve:
                #   dados    -> o conteúdo (bytes)
                #   endereco -> (ip, porta) de quem enviou
                # Lemos um byte a mais que o máximo para não cortar a mensagem.
                dados, endereco = servidor.recvfrom(TAMANHO_MAXIMO + 1)
                texto = dados.decode("utf-8", errors="replace")

                # Mostra o remetente e só os primeiros 100 caracteres
                # (para não encher a tela com mensagens enormes)
                print("Recebido de", endereco[0] + ":" + str(endereco[1]), "->", texto[:100])

                # Devolve exatamente o que recebeu (eco) para o remetente
                servidor.sendto(dados, endereco)
            except OSError as erro:
                # Um erro isolado não deve derrubar o servidor inteiro
                print("Erro de comunicação:", erro)

    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
    except OSError as erro:
        print("Erro ao iniciar o servidor:", erro)
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
