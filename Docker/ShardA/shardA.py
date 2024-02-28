# shard_a.py
import threading
import socket
import queue
import json

class ShardA:
    def __init__(self):
        self.queue = queue.Queue()
        self.saldo = 5000

    def credito(self,data_operacao, conta_cliente, valor_operacao):
        
        self.saldo+=valor_operacao 
        valores_credito=self.saldo

        resposta_data = {   
            "status": "OK",
            "novo_valor_credito": valores_credito
        }

        self.queue.put(resposta_data)
        return json.dumps(resposta_data) #retorna valor atualizado da conta


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
                "type": data["type"],
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


def shard_a():
    # lendo ip do coordenator
    host = '0.0.0.0'#'coordenador'
    shard_a_host = '0.0.0.0'  
    shard_a_port = 8888  

    shard_a_instancia = ShardA()

    shard_a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ver isso aqui!

    shard_a_socket.bind((host, shard_a_port))
    shard_a_socket.listen()

    print(f"[*] Shard A comunicando-se em {shard_a_host}:{shard_a_port}")

    while True:
        
        # Recebendo conexão do Coordenador
        coordenador_socket, addr = shard_a_socket.accept()
        print(f"[*] Conexão aceita {addr}")

        # Cria a thread para lidar com as requisições do coordenador
        
        # Cria uma thread para lidar com o cliente
        client_handler = threading.Thread(target=handle_client, args=(coordenador_socket,))
        client_handler.start()
        
        #request = coordenador_socket.recv(1024).decode('utf-8')

        try:
            data = json.loads(request)
            data_operacao = data["data"]
            conta_cliente = data["conta_cliente"]
            valor_operacao = data["value"]

            resposta = shard_a_instancia.credito(data_operacao, conta_cliente, valor_operacao)
            coordenador_socket.send(resposta.encode('utf-8'))
        except json.JSONDecodeError as e:
            # Erro de decodificação JSON
            coordenador_socket.send(f"Possível erro de comunicação com Server: {str(e)}")
        finally:
            coordenador_socket.close()



if __name__ == "__main__":
    shard_a()
