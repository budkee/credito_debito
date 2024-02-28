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
        self.queue.put(request_transacao)

    def atualizar_saldo(self, tipo, valor_operacao):
        if tipo == 'C':
            self.saldo += valor_operacao
        elif tipo == 'D':
            self.saldo -= valor_operacao

    def get_saldo(self):
        return self.saldo

def handle_client(client_socket, client):
    request = client_socket.recv(1024).decode('utf-8')
    response = "Operação não suportada."

    try:
        data = json.loads(request)
        if "operation" in data and data["operation"] == "OpClient":
            client_data = {
                "data_operacao": data["data_operacao"],
                "conta_cliente": data["conta_cliente"],
                "tipo": data["tipo"],
                "valor_operacao": data["valor_operacao"]
            }
            with open("client_data.json", "a") as json_file:
                json.dump(client_data, json_file)
                json_file.write("\n")

            client.atualizar_saldo(client_data['tipo'], client_data['valor_operacao'])
            response = "OK"
            print(f"Saldo atualizado: {client.get_saldo()}")
    except json.JSONDecodeError:
        response = "Erro ao decodificar JSON."
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

def start_server():
    host = '0.0.0.0'
    port = 9999
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[*] Servidor escutando em {host}:{port}")

    client_instance = Client()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Conexão aceita de {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_instance))
        client_handler.start()

if __name__ == "__main__":
    start_server()
