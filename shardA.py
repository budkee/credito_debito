# shard_a.py
import socket
import json
import queue

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

def shard_a():
    # lendo ip do coordenator
    shard_a_host = '192.168.0.41'  
    shard_a_port = 8888  

    shard_a_instancia = ShardA()

    shard_a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ver isso aqui!
    shard_a_socket.connect((shard_a_host, shard_a_port))
    #shard_a_socket.listen(5)

    print(f"[*] Shard A comunicando-se em {shard_a_host}:{shard_a_port}")

    while True:
        # Recebendo conexão do Coordenador
        coordenador_socket, addr = shard_a_socket.accept()
        print(f"[*] Conexão aceita {addr[0]}:{addr[1]}")

        request = coordenador_socket.recv(1024).decode('utf-8')

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
