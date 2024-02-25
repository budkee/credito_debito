"""
    Código para coordenação da comunicação entre clientes e servidores de uma mesma rede local utilizando threading.

    * As funcionalidades a serem implementadas são:
    
    1. Estabelecer a conexão em rede para clientes e servidores via socket;
    2. Lidar com as solicitações (e retornos) de n-clientes e n-servidores;


"""

# Imports
import threading
import socket
import select
import queue
import time

# Configurações do programa
## Configurações do servidor
HOST = '0.0.0.0'  # Escuta em todas as interfaces de rede
PORT = 7777       # Porta que o servidor vai escutar
max_connections = 5

# Variável para controlar se o servidor está rodando
server_running = True

# Métodos do programa
# 1.2. Função para gerenciar as conexões diretas de vários clientes e servidores
def handle_clients_and_servers(client_sockets, server_sockets):
    
    print("Servidor iniciado. \n\nAguardando conexões...")

    while True:
        # Lista de sockets para seleção
        sockets_list = client_sockets + server_sockets

        # Usando select para lidar com múltiplos sockets
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for sock in read_sockets:
            # Se for um novo cliente se conectando
            if sock in client_sockets:
                client_socket, client_address = sock.accept()
                print(f"Novo cliente conectado: {client_address}")
                client_sockets.append(client_socket)

                # Inicia uma nova thread para lidar com o cliente
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_sockets))
                client_thread.daemon = True
                client_thread.start()

            # Se for um cliente existente enviando mensagem
            else:
                try:
                    data = sock.recv(1024)
                    if data:
                        print(f"Mensagem recebida de {sock.getpeername()}: {data.decode()}")
                        # Aqui você pode processar a mensagem ou encaminhá-la para servidores, etc.
                        # Vamos apenas responder para o exemplo
                        response = b"Recebido pelo servidor: " + data
                        sock.sendall(response)
                    else:
                        print(f"Cliente {sock.getpeername()} desconectado")
                        sock.close()
                        client_sockets.remove(sock)
                except Exception as e:
                    print(f"Erro ao lidar com cliente {sock.getpeername()}: {str(e)}")
                    sock.close()
                    client_sockets.remove(sock)

            # Se for um servidor recebendo mensagem
            if sock in server_sockets:
                try:
                    data = sock.recv(1024)
                    if data:
                        print(f"Mensagem recebida de servidor {sock.getpeername()}: {data.decode()}")
                        # Aqui você pode processar a mensagem recebida do servidor
                        # Por exemplo, encaminhar para os clientes correspondentes
                    else:
                        print(f"Servidor {sock.getpeername()} desconectado")
                        sock.close()
                        server_sockets.remove(sock)
                except Exception as e:
                    print(f"Erro ao lidar com servidor {sock.getpeername()}: {str(e)}")
                    sock.close()
                    server_sockets.remove(sock)


def handle_client(client_socket, client_sockets):
    
    """
        Esta função é chamada em uma nova thread para cada cliente, permitindo que o servidor atenda múltiplos clientes de forma simultânea. (GPT 3.5)

        Não é necessário criar um handler para os servidores, pois, neste caso, cada servidor conectado é tratado de forma similar.
    """

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f"Cliente {client_socket.getpeername()} desconectado")
                client_socket.close()
                client_sockets.remove(client_socket)
                break

            message = data.decode()
            print(f"Mensagem recebida do cliente {client_socket.getpeername()}: {message}")

            # Verifica se o cliente quer encerrar a conexão
            if message.strip().lower() == "encerrar a conexão":
                print(f"Cliente {client_socket.getpeername()} solicitou encerramento da conexão.")
                client_socket.sendall("Fechando a conexão. \nAdeus!")
                client_socket.close()
                client_sockets.remove(client_socket)
                break

            # Verifica se o cliente quer encerrar o servidor
            if message.strip().lower() == "encerrar o servidor":
                print("Solicitado encerramento do servidor.")
                # Adiciona uma mensagem de encerramento para todos os clientes
                for sock in client_sockets:
                    sock.sendall(b"Servidor sendo encerrado. Adeus!")
                    sock.close()
                client_sockets.clear()
                server_socket.close()
                break

            # Aqui você pode processar a mensagem ou encaminhá-la para outros clientes, etc.
            # Vamos apenas responder para o exemplo
            response = b"Recebido pelo servidor: " + data.encode("utf-8")
            client_socket.sendall(response)
        except Exception as e:
            print(f"Erro ao lidar com cliente {client_socket.getpeername()}: {str(e)}")
            client_socket.close()
            client_sockets.remove(client_socket)


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

        # Servidores
        if not fila_solicitacoes_servidores.empty():
            solicitacao = fila_solicitacoes_servidores.get()
            # Realizar tratamento da solicitação dos servidores, processar, etc.
            
            # Simulando resposta aos clientes
            responder_clientes(solicitacao)
            
            fila_solicitacoes_servidores.task_done()

        time.sleep(1)


#-------------Início-do-Programa----------------------

# 1. Estabelecer a conexão em rede para clientes e servidores via socket;

# 1.1. Criando os sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(max_connections)

# 1.2. Listas de sockets de clientes e servidores
client_sockets = []
server_sockets = [server_socket]

# 2. Lidar com a solicitação de n-clientes e n-servidores
# 2.1. Iniciando a thread para lidar com clientes e servidores
thread_clients_and_servers = threading.Thread(target=handle_clients_and_servers, args=(client_sockets, server_sockets))
thread_clients_and_servers.daemon = True
thread_clients_and_servers.start()

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


"""
    #-----------------Referências---------------------------------

    (GPT 3.5): https://chat.openai.com/
    (iMasters): https://imasters.com.br/back-end/threads-em-python
"""