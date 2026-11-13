#!/usr/bin/env python3
# =====================================================================
# Trabalho 2 - Redes de Computadores 2  (Prof. Alessandro Vivas Andrade)
# Exercício 3 - Servidor de chat TCP
#
# Grupo: Maria Eduarda Fernandes, Quezia Oliveira e Raquel Monteiro
# =====================================================================
"""
Servidor de chat em rede (várias pessoas na mesma sala).

Regras do nosso protocolo (texto, UMA mensagem por linha, terminada em \\n):
  - a primeira linha enviada por um cliente é o apelido (nickname);
  - as linhas seguintes são mensagens, que o servidor repassa para
    TODOS os outros clientes, precedidas do nome de quem enviou;
  - o servidor avisa a sala quando alguém entra ou sai;
  - se o cliente enviar "sair", só ele é desconectado.

Como executar:
  python3 servidor.py --porta 5001
"""
import argparse
import socket
import threading

# Dicionário com todos os clientes online:  {socket_do_cliente: apelido}
clientes = {}

# Várias threads (uma por cliente) mexem nesse dicionário ao mesmo tempo.
# O Lock faz com que só UMA thread por vez leia/altere os dados, evitando
# erros como "dicionário mudou de tamanho durante a leitura".
trava = threading.Lock()


def enviar_para_todos(texto, quem_enviou=None):
    # Envia 'texto' para todos os clientes online, exceto 'quem_enviou'.

    # Copiamos a lista de conexões DENTRO do lock (rápido) e fazemos os
    # envios FORA dele, para que um cliente lento não trave os demais.
    with trava:
        destinos = list(clientes.keys())

    for conexao in destinos:
        if conexao == quem_enviou:
            continue  # não manda a mensagem de volta para quem escreveu
        try:
            # O "\n" no fim marca o final da mensagem (nosso protocolo)
            conexao.sendall((texto + "\n").encode("utf-8"))
        except OSError:
            pass  # esse cliente caiu; a thread dele fará a limpeza


def atender_cliente(conexao, endereco):
    # Roda em uma thread por cliente, do início ao fim da conexão.

    # makefile() transforma o socket em algo parecido com um arquivo de texto,
    # assim podemos ler LINHA POR LINHA. Isso evita um problema do TCP: ele é
    # um "fluxo de bytes", então duas mensagens podem chegar coladas ou uma
    # mensagem pode chegar partida. Com linhas isso fica resolvido.
    arquivo = conexao.makefile("r", encoding="utf-8")
    apelido = None

    try:
        # A primeira linha recebida é o apelido
        apelido = arquivo.readline().strip()

        # Valida o apelido (não pode ser vazio nem ter espaços)
        if apelido == "" or " " in apelido:
            conexao.sendall("ERRO: apelido inválido (não pode ter espaços)\n".encode("utf-8"))
            apelido = None
            return  # o finally abaixo ainda será executado

        # Confere se o apelido já existe E registra o cliente, tudo dentro do
        # mesmo lock. Assim dois clientes não conseguem pegar o mesmo nome
        # ao mesmo tempo.
        with trava:
            ja_existe = apelido in clientes.values()
            if not ja_existe:
                clientes[conexao] = apelido

        if ja_existe:
            conexao.sendall("ERRO: esse apelido já está em uso\n".encode("utf-8"))
            apelido = None
            return

        print(apelido, "entrou", endereco)
        conexao.sendall(("Bem-vindo(a), " + apelido + "! Digite 'sair' para sair.\n").encode("utf-8"))
        # Avisa os OUTROS participantes que alguém entrou
        enviar_para_todos("*** " + apelido + " entrou na sala ***", conexao)

        # Fica lendo as mensagens do cliente até ele sair ou desconectar.
        # O "for" termina sozinho quando o cliente fecha a conexão.
        for linha in arquivo:
            mensagem = linha.strip()
            if mensagem == "":
                continue
            if mensagem.lower() == "sair":
                break  # comando de saída: só este cliente é desconectado
            # Retransmite para todos os demais, com o nome do remetente
            enviar_para_todos("[" + apelido + "] " + mensagem, conexao)

    except OSError:
        # Cliente caiu de repente: só esta thread termina, o servidor continua
        pass

    finally:
        # Limpeza: remove o cliente da lista (se ele chegou a ser registrado).
        # A variável 'estava_online' evita avisar "saiu" de quem nunca entrou
        # (por exemplo, apelido inválido).
        estava_online = False
        with trava:
            if conexao in clientes:
                del clientes[conexao]
                estava_online = True

        if estava_online:
            print(apelido, "saiu")
            enviar_para_todos("*** " + apelido + " saiu da sala ***")

        arquivo.close()
        conexao.close()


def main():
    parser = argparse.ArgumentParser(description="Servidor de chat TCP")
    parser.add_argument("--host", default="0.0.0.0", help="endereço de escuta")
    parser.add_argument("--porta", type=int, default=5001, help="porta do servidor (padrão: 5001)")
    args = parser.parse_args()

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reiniciar o servidor rapidamente na mesma porta
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((args.host, args.porta))
        servidor.listen()
        print("Chat ativo em", args.host, args.porta, "(Ctrl+C para parar)")

        while True:
            # Cada cliente novo ganha a sua própria thread
            conexao, endereco = servidor.accept()
            thread = threading.Thread(target=atender_cliente, args=(conexao, endereco))
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
