# Imports
import threading
import socket
import select
import queue
import time

# Configurações do programa
## Configurações do servidor
HOST = '192.168.0.40'  # '0.0.0.0' Escuta em todas as interfaces de rede
PORT = 7777       # Porta que o servidor vai escutar
max_connections = 5

# Variável para controlar se o servidor está rodando
server_running = True

# Métodos do programa
# 1.2. Função para gerenciar as conexões diretas de vários clientes e servidores
def handle_clients(client_sockets):
    print("Servidor iniciado. \n\nAguardando conexões...")

    while True:
        # Lista de sockets para seleção
        read_sockets, _, _ = select.select(client_sockets, [], [])

        for sock in read_sockets:
            # Se for um novo cliente se conectando
            if sock in client_sockets:
                try:
                    data = sock.recv(1024)
                    if not data:
                        print(f"Cliente {sock.getpeername()} desconectado")
                        sock.close()
                        client_sockets.remove(sock)
                        continue

                    message = data.decode()
                    print(f"Mensagem recebida do cliente {sock.getpeername()}: {message}")

                    # Verifica se o cliente quer encerrar a conexão
                    if message.strip().lower() == "encerrar a conexão":
                        print(f"Cliente {sock.getpeername()} solicitou encerramento da conexão.")
                        sock.sendall("Fechando a conexão. \nAdeus!".encode())
                        sock.close()
                        client_sockets.remove(sock)
                        continue

                    # Verifica se o cliente quer encerrar o servidor
                    if message.strip().lower() == "encerrar o servidor":
                        print("Solicitado encerramento do servidor.")
                        # Adiciona uma mensagem de encerramento para todos os clientes
                        for client_sock in client_sockets:
                            client_sock.sendall(b"Servidor sendo encerrado. Adeus!")
                            client_sock.close()
                        client_sockets.clear()
                        continue

                    # Aqui você pode processar a mensagem ou encaminhá-la para outros clientes, etc.
                    # Vamos apenas responder para o exemplo
                    response = b"Recebido pelo servidor: " + data
                    sock.sendall(response)
                except Exception as e:
                    print(f"Erro ao lidar com cliente {sock.getpeername()}: {str(e)}")
                    sock.close()
                    client_sockets.remove(sock)


def is_socket_connected(sock):
    """Verifica se o socket está conectado."""
    try:
        # Tenta enviar uma mensagem pequena
        sock.send(b'Done!')
        return True
    except Exception as e:
        # Se ocorrer um erro, o socket não está conectado
        return False


# 2. Função para tratar solicitações dos clientes e servidores
def tratar_solicitacoes():
    while True:
        # Clientes
        if not fila_solicitacoes_clientes.empty():
            solicitacao = fila_solicitacoes_clientes.get()
            # Realizar tratamento da solicitação dos clientes, organizar informações, etc.
            
            # Simulando envio para servidores
            enviar_para_servidores(solicitacao)
            
            fila_solicitacoes_clientes.task_done()

        time.sleep(1)


#-------------Início-do-Programa----------------------

# 1. Estabelecer a conexão em rede para clientes e servidores via socket;

# 1.1. Listas de sockets de clientes e servidores
client_sockets = []

# 2. Lidar com a solicitação de n-clientes
# 2.1. Iniciando a thread para lidar com clientes e servidores
thread_clients = threading.Thread(target=handle_clients, args=(client_sockets))
thread_clients.daemon = True
thread_clients.start()

# Aguardando comando para encerrar o servidor
while server_running:

    # Entrada cliente
    comando = input("\nDigite 'encerrar o servidor' para fechar o servidor: ")

    if comando.lower() == "encerrar o servidor":
        print("Encerrando servidor...")
        
        # Adiciona uma mensagem de encerramento para todos os clientes
        for sock in client_sockets:
            sock.sendall(b"Servidor sendo encerrado... Boa vida a todes!")
            sock.close()
        client_sockets.clear()
        
        # Fecha todos os sockets do servidor
        for sock in server_sockets:
            sock.close()
        server_sockets.clear()
        
        # Fim do programa
        server_running = False

