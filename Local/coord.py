import socket
import threading
from queue import Queue
import json


#-------Função-Principal--------
def start_server(host, port):

    # Cria a fila de requisições
    request_queue = Queue()

    # Conexão por streamming
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        
        server_socket.bind((host, port))
        server_socket.listen()
        print("Coordenador escutando em", (host, port))

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

#-------Função-para-Lidar-com-as-Requisições--------
def handle_request(request_queue):

    while True:
        
        if not request_queue.empty():

            shard, tipo_operacao, valor_operacao = request_queue.get()
            
            if shard == "shardA":
                
                response = handle_shards('0.0.0.0', 8888, tipo_operacao, valor_operacao)
                
            elif shard == "shardB":

                response = handle_shards('0.0.0.0', 9999, tipo_operacao, valor_operacao)

            else:
                response = "Shard inválido"
            
            print(response) # Resposta do shard correspondente


#-------Função-para-Lidar-com-Shards--------
def handle_shards(host, port, tipo_operacao, valor_operacao):
    
    # Comunicação por streamming
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        saldo_atual = 1000 

        request = {
            "tipo_operacao": tipo_operacao,
            "valor_operacao": valor_operacao,
            "saldo_atual": saldo_atual
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
            # Obter a resposta do shardA
        

        elif tipo_operacao == "D":
            request_queue.put(("shardB", tipo_operacao, valor_operacao))
            # Obter a resposta do shardB
            
        else:
            client_socket.send("Tipo de operação inválido".encode())
            client_socket.close()
            return
        
    
        # Atualizar o saldo
        #saldo_atualizado = json.loads(shard_response)['saldo_atualizado']

        response = "Transação concluída com sucesso!" # Resposta para o cliente

        # Enviando resposta de volta para o cliente
        client_socket.send(response.encode('utf-8'))

        # Fechando a conexão com o cliente
        client_socket.close()

    except json.JSONDecodeError:
        response = "Erro ao decodificar JSON."


            

#-------Módulo-Principal--------
if __name__ == "__main__":

    # Configurações do servidor
    host = '0.0.0.0'
    port = 7777

    #-------Início-do-Programa----- 
    start_server(host, port)