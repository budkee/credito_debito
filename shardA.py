# shard_a.py
import socket
import json

def credito(data_operacao, conta_cliente, valor_operacao):
    resposta_data = {
        "status": "OK"
    }
    return json.dumps(resposta_data)

def shard_a():
    # configurando shard A
    shard_a_host = '192.168.0.41'  
    shard_a_port = 8888  

    #criando socket TCP para o shard A
    shard_a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ver isso aqui!

    # vinculando socket com host e porta do server
    shard_a_socket.bind((shard_a_host, shard_a_port))

    #conexões recebidas
    shard_a_socket.listen(5)

    print(f"[*] Shard A comunicando-se em {shard_a_host}:{shard_a_port}")

    while True:
        # Recebendo coordenador
        coordenador_socket, addr = shard_a_socket.accept()
        print(f"[*] Conexão aceita {addr[0]}:{addr[1]}")

        ###
        solicitacao = coordenador_socket.recv(1024).decode('utf-8')

        try:
            data = json.loads(solicitacao)
            if "operacao" in data and data["operacao"] == "Credito":
        
                data_operacao = data["data"]
                conta_cliente = data["conta_cliente"]
                valor_operacao = data["value"]

                # enviando resposta para coordenador
                resposta = credito(data_operacao, conta_cliente, valor_operacao)
                coordenador_socket.send(resposta.encode('utf-8'))
            else:
                coordenador_socket.send("Operação Inválida".encode('utf-8'))
        
        except json.JSONDecodeError:
            # Erro cod JSON
            coordenador_socket.send("Possível erro de comunicação com Server")

        
        coordenador_socket.close()

if __name__ == "__main__":
    shard_a()
