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

    #def atualizar_saldo(self, tipo, valor_operacao):
     #   if tipo == 'C':
      #      self.saldo += valor_operacao
       # elif tipo == 'D':
        #    self.saldo -= valor_operacao

    #def get_saldo(self):
     #   return self.saldo


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


def solicitando_shard_a(client_data):
    try:
        shard_a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        shard_a_host = '0.0.0.0'  # Substituir pelo endereço do Shard A
        shard_a_port = 8888  # Substituir pela porta do Shard A

        shard_a_socket.connect((shard_a_host, shard_a_port))

        # solicitação para o Shard A
        request_shard_a = json.dumps({
            'data': client_data['data'],
            'conta_cliente': client_data['conta_cliente'],
            'value': client_data['value']
        })

        shard_a_socket.send(request_shard_a.encode('utf-8'))

        # Recebendo a resposta do Shard A
        resposta_shard_a = shard_a_socket.recv(1024).decode('utf-8')

        shard_a_socket.close()

        return resposta_shard_a
    except socket.error as e:
        return f"Erro na comunicação com o Shard A: {str(e)}"


def solicitando_shard_b(client_data):
    try:
        shard_b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        shard_b_host = '0.0.0.0'  # Substitir pelo endereço do Shard B
        shard_b_port = 8889  # Substituir pela porta do Shard B

        shard_b_socket.connect((shard_b_host, shard_b_port))

        # solicitação shard B
        request_shard_b = json.dumps({
            'data': client_data['data'],
            'conta_cliente': client_data['conta_cliente'],
            'value': client_data['value']
        })

        shard_b_socket.send(request_shard_b.encode('utf-8'))

        # Recebe a resposta do Shard B
        resposta_shard_b = shard_b_socket.recv(1024).decode('utf-8')

        shard_b_socket.close()

        return resposta_shard_b
    except socket.error as e:
        return f"Erro na comunicação com o Shard B: {str(e)}"


def handle_client(client_socket):
    # Recebe dados do cliente
    request = client_socket.recv(1024).decode('utf-8')

    # Trata a mensagem
    try:
        data = json.loads(request)

        if "operation" in data and data["operation"] == "OpClient":
            # Extraindo dados do cliente
            client_data = {
                "data": data["data"],
                "conta_cliente": data["conta_cliente"],
                "tipo": data["tipo"],
                "value": data["value"]
            }

            # Armazenando os dados em um arquivo JSON
            with open("client_data.json", "a") as json_file:
                json.dump(client_data, json_file)
                json_file.write("\n")

            if client_data['tipo'] == 'C':
                # enviando solicitação para o Shard A
                resposta_shard_a = solicitando_shard_a(client_data)
                response = resposta_shard_a  
            elif client_data['tipo'] == 'D':
                # enviando solicitação para o Shard B
                resposta_shard_b = solicitando_shard_b(client_data)
                response = resposta_shard_b 
            else:
                response = "Tipo de operação não suportado."

        else:
            response = "Operação não suportada."
    except json.JSONDecodeError:
        response = "Erro ao decodificar JSON."

    # Enviando resposta de volta para o cliente
    client_socket.send(response.encode('utf-8'))

    # Fechando a conexão com o cliente
    client_socket.close()


if __name__ == "__main__":
    start_server()
