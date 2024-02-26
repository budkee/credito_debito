import socket
import threading
import json

def handle_client(client_socket):
    
    # Recebe dados do cliente
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Recebido do cliente: {request}")

    # Trata a mensagem
    try:
        data = json.loads(request)
        if "operation" in data and data["operation"] == "OpClient":
            
            # Extrai os dados relevantes
            client_data = {
                "data": data["data"],
                "conta_cliente": data["conta_cliente"],
                "type": data["type"],
                "value": data["value"]
            }

            # Armazena os dados em um arquivo JSON
            with open("client_data.json", "a") as json_file:
                json.dump(client_data, json_file)
                json_file.write("\n")

            response = "OK"
        else:
            response = "Operação não suportada."
    except json.JSONDecodeError:
        response = "Erro ao decodificar JSON."

    # Envia resposta de volta para o cliente
    client_socket.send(response.encode('utf-8'))

    # Fecha a conexão com o cliente
    client_socket.close()

def start_server():
    # Endereço e porta em que o servidor vai ouvir
    host = 'localhost'
    port = 9999

    # Cria um socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket com o endereço e porta
    server_socket.bind((host, port))

    # Define o limite máximo de conexões pendentes
    server_socket.listen(5)

    print(f"[*] Servidor escutando em {host}:{port}")

    while True:
        
        # Aceita a conexão
        client_socket, addr = server_socket.accept()
        print(f"[*] Conexão aceita de {addr[0]}:{addr[1]}")

        # Cria uma thread para lidar com o cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
