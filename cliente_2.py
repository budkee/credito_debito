import socket

# Configurações do cliente
SERVER_HOST = '192.168.0.40'  # Endereço IP do servidor
SERVER_PORT = 8888             # Porta do servidor

# Criando o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectando ao servidor
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"Conectado ao servidor em {SERVER_HOST}:{SERVER_PORT}")

    while True:
        # Aguardando a entrada do usuário
        message = input("Digite sua mensagem (ou 'encerrar' para sair): ")

        # Verificando se o usuário quer encerrar
        if message.lower() == 'encerrar':
            client_socket.sendall(message.encode())
            break

        # Enviando a mensagem ao servidor
        client_socket.sendall(message.encode())

        # Recebendo a resposta do servidor
        response = client_socket.recv(1024)
        print("Resposta do servidor:", response.decode())

except Exception as e:
    print(f"Erro ao conectar ao servidor: {str(e)}")

finally:
    # Fechando o socket do cliente
    client_socket.close()
    print("Conexão com o servidor encerrada.")
