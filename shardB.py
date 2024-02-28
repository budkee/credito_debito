import socket
import json
import queue

class ShardB:
    def __init__(self):
        self.queue = queue.Queue()
        self.saldo = 5000 

    def debito(self, data_operacao, conta_cliente, valor_operacao):
        resposta_data = {}
        
        try:
            if valor_operacao > self.saldo:
                resposta_data["status"] = "Saldo insuficiente"
            else:
                self.saldo -= valor_operacao
                valores_debito = self.saldo

                resposta_data = {
                    "status": "OK",
                    "novo_valor_debito": valores_debito
                }

                self.queue.put(resposta_data)
        
        except Exception as e:
            resposta_data["status"] = f"Erro ao processar débito: {str(e)}"

        return json.dumps(resposta_data) # Retornando valor atualizado da conta

def shard_b():
    # lendo ip do coordenator
    shard_b_host = '192.168.0.42'  
    shard_b_port = 8889  

    shard_b_instancia = ShardB()

    shard_b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    shard_b_socket.connect((shard_b_host, shard_b_port))

    print(f"[*] Shard B comunicando-se em: {shard_b_host}:{shard_b_port}")

    while True:
        # Recebendo conexão do Coordenador
        coordenador_socket, addr = shard_b_socket.accept()
        print(f"[*] Conexão aceita {addr[0]}:{addr[1]}")

        request = coordenador_socket.recv(1024).decode('utf-8')

        try:
            data = json.loads(request)
            if "operacao" in data and data["operacao"] == "D":
                data_operacao = data["data"]
                conta_cliente = data["conta_cliente"]
                valor_operacao = data["value"]

                # enviando resposta para coordenador
                resposta = shard_b_instancia.debito(data_operacao, conta_cliente, valor_operacao)
                coordenador_socket.send(resposta.encode('utf-8'))
            else:
                # Operação Inválida
                coordenador_socket.send("Operação Inválida".encode('utf-8'))
        except json.JSONDecodeError as e:
            # Erro de decodificação JSON
            coordenador_socket.send(f"Possível erro de comunicação com Server: {str(e)}")
        
        finally:
            coordenador_socket.close()

if __name__ == "__main__":
    shard_b()
