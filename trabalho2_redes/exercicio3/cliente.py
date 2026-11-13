#!/usr/bin/env python3
# =====================================================================
# Trabalho 2 - Redes de Computadores 2  (Prof. Alessandro Vivas Andrade)
# Exercício 3 - Cliente de chat TCP
#
# Grupo: Maria Eduarda Fernandes, Quezia Oliveira e Raquel Monteiro
# =====================================================================
"""
Cliente do chat. Usa DUAS threads para enviar e receber ao mesmo tempo:
  - uma thread só para RECEBER e mostrar as mensagens do servidor;
  - a thread principal para LER o que o usuário digita e ENVIAR.
Sem a segunda thread, o programa ficaria travado no input() e só
mostraria as mensagens dos outros depois que o usuário digitasse algo.

Como executar (com o servidor já rodando):
  python3 cliente.py --host 127.0.0.1 --porta 5001
Digite "sair" para sair do chat.
"""
import argparse
import socket
import threading


def receber_mensagens(conexao, terminou):
    # Roda na SEGUNDA thread: imprime tudo o que o servidor mandar.
    #   conexao  -> socket já conectado
    #   terminou -> Event usado para avisar a thread principal que acabou
    try:
        # Lê o socket linha por linha (mesmo esquema do servidor)
        arquivo = conexao.makefile("r", encoding="utf-8")
        for linha in arquivo:
            # "\r" volta o cursor ao início da linha para não misturar
            # a mensagem recebida com o que o usuário estava digitando
            print("\r" + linha.strip())
    except OSError:
        pass  # socket foi fechado: é o fim normal da conexão

    # Chegamos aqui quando o servidor fecha a conexão (ou o socket é fechado).
    # O Event avisa a thread principal para parar de pedir mensagens.
    terminou.set()
    print("[Desconectado do servidor. Pressione Enter para sair.]")


def main():
    parser = argparse.ArgumentParser(description="Cliente de chat TCP")
    parser.add_argument("--host", default="127.0.0.1", help="IP do servidor")
    parser.add_argument("--porta", type=int, default=5001, help="porta do servidor (padrão: 5001)")
    args = parser.parse_args()

    # Pede o apelido até o usuário digitar algo válido (sem espaços)
    apelido = ""
    while apelido == "" or " " in apelido:
        apelido = input("Apelido (sem espaços): ").strip()

    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        conexao.connect((args.host, args.porta))
    except ConnectionRefusedError:
        print("Servidor indisponível.")
        conexao.close()
        return
    except OSError as erro:
        print("Erro ao conectar:", erro)
        conexao.close()
        return

    # Event = "bandeirinha" compartilhada entre as threads:
    # a thread de recebimento levanta (set) quando a conexão acaba.
    terminou = threading.Event()

    try:
        # Protocolo: a primeira linha enviada é SEMPRE o apelido
        conexao.sendall((apelido + "\n").encode("utf-8"))

        # Inicia a thread que fica recebendo mensagens em segundo plano.
        # daemon=True: ela não impede o programa de fechar.
        thread = threading.Thread(target=receber_mensagens, args=(conexao, terminou))
        thread.daemon = True
        thread.start()

        # Thread principal: lê o teclado e envia, até o usuário sair
        while not terminou.is_set():
            texto = input("").strip()

            if terminou.is_set():
                break  # servidor caiu enquanto o usuário digitava
            if texto == "":
                continue

            conexao.sendall((texto + "\n").encode("utf-8"))

            if texto.lower() == "sair":
                break  # o servidor também entende "sair" e nos desconecta

    except (EOFError, KeyboardInterrupt):
        # Ctrl+C / Ctrl+D também sai de forma limpa, avisando o servidor
        try:
            conexao.sendall("sair\n".encode("utf-8"))
        except OSError:
            pass
    except OSError as erro:
        print("Erro de rede:", erro)
    finally:
        conexao.close()
        print("Você saiu do chat.")


if __name__ == "__main__":
    main()
