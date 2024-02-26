import socket
import json

def debito(data_operacao, conta_cliente, valor_operacao):
    resposta_data = {
        "status": "OK"
    }
    return json.dumps(resposta_data)

def start_shard_b():
    # Shard B configuration
    shard_b_host = '192.168.0.42'  
    shard_b_port = 8889  

    # Criando socket
    shard_b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # vinculando socket com host e porta do server
    shard_b_socket.bind((shard_b_host, shard_b_port))

    # Conexões recebidas
    shard_b_socket.listen(5)

    print(f"[*] Shard B comunicando-se em: {shard_b_host}:{shard_b_port}")

    while True:
        # Recebendo conexão do Coordenador
        coordenador_socket, addr = shard_b_socket.accept()
        print(f"[*] Conexão aceita {addr[0]}:{addr[1]}")

        request = coordenador_socket.recv(1024).decode('utf-8')

        try:
            data = json.loads(request)
            if "operacao" in data and data["operacao"] == "Debito":
                data_operacao = data["data"]
                conta_cliente = data["conta_cliente"]
                valor_operacao = data["value"]

                # enviando resposta para coordenador
                resposta = debito(data_operacao, conta_cliente, valor_operacao)
                coordenador_socket.send(resposta.encode('utf-8'))
            else:
                # Operação Inválida
                coordenador_socket.send("Operação Inválida".encode('utf-8'))
        except json.JSONDecodeError:
            coordenador_socket.send("Possível erro de comunicação com Server")

        coordenador_socket.close()

if __name__ == "__main__":
    start_shard_b()
