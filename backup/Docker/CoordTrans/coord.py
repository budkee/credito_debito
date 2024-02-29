import socket
import threading
from queue import Queue
import json

class Client:
    
    def __init__(self):
        self.queue = Queue()
        self.saldo = 0.0 

    def OpClient(self, data_operacao, conta_cliente, tipo_operacao, valor_operacao):
        request_transacao = {
            "data_operacao": data_operacao,
            "conta_cliente": conta_cliente,
            "tipo_operacao": tipo_operacao,
            "valor_operacao": valor_operacao
        }
        self.queue.put(request_transacao)


#-------Função-Principal--------
def start_server(host, port):

    # Cria a fila de requisições
    request_queue = Queue()

    # Conexão por streamming
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        
        server_socket.bind((host, port))
        server_socket.listen()
        print("Servidor principal escutando em", (host, port))

        # Execução em multithread das requisições
        process_thread = threading.Thread(target=handle_request, args=(request_queue,))
        process_thread.start()
    
        # Enquanto o servidor estiver ativo
        while True:

            # Aceita a conexão
            client_socket, address = server_socket.accept()
            print(f"[*] Conexão estabelecida com {address[0]}:{address[1]}")
            
            # Execução em multithread dos dados dos clientes
            client_thread = threading.Thread(target=handle_client_data, args=(client_socket, address, request_queue))
            client_thread.start()

#-------Função-para-Lidar-com-Shards--------
def handle_shards(host, port, tipo_operacao, valor_operacao):
    
    # Comunicação por streamming
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        request = {
            "tipo_operacao": tipo_operacao,
            "valor_operacao": valor_operacao
        }
        s.sendall(json.dumps(request).encode())
        response = s.recv(1024)
    return response.decode()

#-------Função-para-Lidar-com-os-dados-do-Clientes--------
def handle_client_data(client_socket, address, request_queue):

    # Recebe dados do cliente
    dados = client_socket.recv(1024).decode('utf-8')
    request = json.loads(dados)

    # Trata a mensagem
    try:
        
        # Puxa os dados de interesse
        data_operacao = request['data_operacao']
        conta_cliente = request['conta_cliente']
        tipo_operacao = request['tipo_operacao']
        valor_operacao = request['valor_operacao']

        # Verifica qual é o tipo de operação de interesse ao usuário
        if tipo_operacao == 'C':
            request_queue.put(("shardA", tipo_operacao, valor_operacao))
        
        elif tipo_operacao == "D":
            request_queue.put(("shardB", tipo_operacao, valor_operacao))
        
        else:
            client_socket.send("Tipo de operação inválido".encode())
            client_socket.close()
            return
        
        response = "OK"

        # Enviando resposta de volta para o cliente
        client_socket.send(response.encode('utf-8'))

        # Fechando a conexão com o cliente
        client_socket.close()

    except json.JSONDecodeError:
        response = "Erro ao decodificar JSON."

#-------Função-para-Lidar-com-as-Requisições--------
def handle_request(request_queue):

    while True:
        
        if not request_queue.empty():

            shard, tipo_operacao, valor_operacao = request_queue.get()
            
            if shard == "shardA":
                
                response = handle_shards('localhost', 8888, tipo_operacao, valor_operacao)

            elif shard == "shardB":

                response = handle_shards('localhost', 9999, tipo_operacao, valor_operacao)
            else:
                response = "Shard inválido"
            print("Resposta do", shard, ":", response)


#-------Módulo-Principal--------
if __name__ == "__main__":

    # Configurações do servidor
    host = '0.0.0.0'
    port = 7777

    #-------Início-do-Programa----- 
    start_server(host, port)