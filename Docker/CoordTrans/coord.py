import socket
import threading
import queue
import json


class Client:
    def __init__(self):
        self.queue = queue.Queue()
        self.saldo = 0.0 

    def OpClient(self, data_operacao, conta_cliente, tipo, valor_operacao):
        
        request_transacao = {
            "data_operacao": data_operacao,
            "conta_cliente": conta_cliente,
            "tipo": tipo,
            "valor_operacao": valor_operacao
        }

        # Coloca a requisição na fila
        self.queue.put(request_transacao)

    def atualizar_saldo(self, tipo, valor_operacao):
        if tipo == 'C':
            self.saldo += valor_operacao
        elif tipo == 'D':
            self.saldo -= valor_operacao

    def get_saldo(self):
        return self.saldo


def start_server():
    # Endereço e porta em que o servidor vai ouvir
    host = '0.0.0.0'
    port = 9999
    port_shardA = 8888

    # Cria um socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket com o endereço e porta
    server_socket.bind((host, port))

    # Escuta
    server_socket.listen()

    print(f"[*] Servidor escutando em {host}:{port}")

    while True:
        
        # Aceita a conexão
        client_socket, addr = server_socket.accept()
        print(f"[*] Conexão aceita de {addr[0]}:{addr[1]}")

        # Cria uma thread para lidar com o cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()




def handle_client(client_socket):
    
    # Recebe dados do cliente
    request = client_socket.recv(1024).decode('utf-8')

    # Fila de clientes e identificação por ordem de chegada
    print(f"Dados recebidos do cliente[i]: {request}")

    # Trata a mensagem 
    try:
        data = json.loads(request)
        
        if "operation" in data and data["operation"] == "OpClient":
            
            # Extrai os dados relevantes
            client_data = {
                "data": data["data"],
                "conta_cliente": data["conta_cliente"],
                "tipo": data["tipo"],
                "value": data["value"]
            }

            # Armazena os dados em um arquivo JSON
            with open("client_data.json", "a") as json_file:
                json.dump(client_data, json_file)
                json_file.write("\n")

            if response == "OK":   
                client.atualizar_saldo(next_transaction['tipo'], next_transaction['valor_operacao'])
                print(f"Saldo atualizado: {client.get_saldo()}")

            # Após receber os dados do shard correspondente
            #response = "OK"
        else:
            response = "Operação não suportada."
    except json.JSONDecodeError:
        response = "Erro ao decodificar JSON."

    # Envia resposta de volta para o cliente
    client_socket.send(response.encode('utf-8'))

    # Fecha a conexão com o cliente
    client_socket.close()


if __name__ == "__main__":
    start_server()
