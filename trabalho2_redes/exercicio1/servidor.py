#!/usr/bin/env python3
# =====================================================================
# Trabalho 2 - Redes de Computadores 2  (Prof. Alessandro Vivas Andrade)
# Exercício 1 - Servidor TCP multithread
#
# Grupo: Maria Eduarda Fernandes, Quezia Oliveira e Raquel Monteiro
# =====================================================================
"""
Servidor TCP que atende vários clientes ao mesmo tempo.

Como funciona:
  1. O servidor reserva uma porta e fica esperando conexões (accept).
  2. Quando um cliente conecta, criamos uma THREAD só para ele.
     Assim o servidor volta a esperar o próximo cliente sem ficar
     preso conversando com o primeiro.
  3. Cada mensagem recebida é impressa com data/hora e IP:porta do
     cliente, e o servidor responde "Mensagem recebida".

Como executar:
  python3 servidor.py --porta 5000
"""
import argparse    # lê os parâmetros da linha de comando (--host, --porta)
import socket      # biblioteca de sockets (comunicação em rede)
import threading   # permite atender vários clientes em paralelo
from datetime import datetime  # para mostrar data e hora nos logs

# Quantidade máxima de bytes que lemos de uma vez em cada recv()
TAMANHO_BUFFER = 4096


def hora_atual():
    # Devolve a data e a hora atuais já formatadas como texto
    # (ex.: "13/11/2026 14:30:05"). Usamos nos logs do servidor.
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def atender_cliente(conexao, endereco):
    # Esta função roda em uma thread, uma para cada cliente conectado.
    #   conexao  -> socket exclusivo para falar com ESTE cliente
    #   endereco -> tupla (ip, porta) de onde o cliente está conectando
    ip = endereco[0]
    porta = endereco[1]
    print(hora_atual(), "- cliente conectado:", ip, porta)

    try:
        while True:
            # recv() fica parado (bloqueado) até o cliente enviar algo.
            # Se o cliente fechar a conexão, recv() devolve b"" (vazio).
            dados = conexao.recv(TAMANHO_BUFFER)
            if not dados:
                break  # cliente saiu, então encerramos o laço

            # Os dados chegam em bytes; decode() transforma em texto
            # e strip() tira espaços e quebras de linha das pontas.
            mensagem = dados.decode("utf-8").strip()

            # Validação pedida no exercício: não aceita mensagem vazia.
            # "continue" volta ao início do laço para esperar a próxima.
            if mensagem == "":
                conexao.sendall("Mensagem vazia ignorada".encode("utf-8"))
                continue

            # Log no console: data/hora + IP:porta + o que o cliente disse
            print(hora_atual(), "-", ip + ":" + str(porta), "disse:", mensagem)

            # sendall() garante que TODA a resposta seja enviada.
            # encode() faz o caminho inverso do decode (texto -> bytes).
            conexao.sendall("Mensagem recebida".encode("utf-8"))

    except OSError as erro:
        # OSError cobre queda de conexão, reset pelo cliente etc.
        # Só ESTA thread é afetada: o servidor e os outros clientes
        # continuam funcionando normalmente.
        print("Erro com o cliente", ip, porta, "->", erro)

    finally:
        # O finally roda SEMPRE, com erro ou sem erro.
        # Garante que a conexão com este cliente seja fechada.
        conexao.close()
        print(hora_atual(), "- cliente desconectado:", ip, porta)


def main():
    # --- Parâmetros de linha de comando (evita valores fixos no código) ---
    parser = argparse.ArgumentParser(description="Servidor TCP")
    parser.add_argument("--host", default="0.0.0.0",
                        help="endereço de escuta (0.0.0.0 = todas as interfaces)")
    parser.add_argument("--porta", type=int, default=5000,
                        help="porta do servidor (padrão: 5000)")
    args = parser.parse_args()

    # Cria o socket TCP: AF_INET = IPv4, SOCK_STREAM = TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permite reiniciar o servidor logo após fechar, sem o erro
    # "porta em uso" (o sistema demora um pouco para liberar a porta)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((args.host, args.porta))  # reserva o endereço e a porta
        servidor.listen()                       # começa a aceitar conexões
        print("Servidor ativo em", args.host, args.porta, "(Ctrl+C para parar)")

        while True:
            # accept() espera um cliente conectar e devolve:
            #   - um NOVO socket só para falar com esse cliente
            #   - o endereço (ip, porta) dele
            conexao, endereco = servidor.accept()

            # Cria uma thread para esse cliente e já volta a esperar o próximo
            thread = threading.Thread(target=atender_cliente, args=(conexao, endereco))
            thread.daemon = True  # a thread não impede o programa de fechar
            thread.start()

    except KeyboardInterrupt:
        # Usuário apertou Ctrl+C: encerramos sem mostrar erro feio
        print("\nServidor encerrado pelo usuário.")
    except OSError as erro:
        # Ex.: porta já está sendo usada por outro programa
        print("Erro ao iniciar o servidor:", erro)
    finally:
        servidor.close()  # libera a porta, aconteça o que acontecer


# Só executa main() quando o arquivo é rodado diretamente
# (e não quando é importado por outro programa)
if __name__ == "__main__":
    main()
