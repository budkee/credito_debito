import socket
import json

def OpClient(data_operacao, conta_cliente, tipo_operacao, valor_operacao):
    
    return {
        "data_operacao": data_operacao,
        "conta_cliente": conta_cliente,
        "tipo_operacao": tipo_operacao,
        "valor_operacao": valor_operacao
    }

def enviar_request(host, port, request):
    
    # Comunicação por streamming
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps(request).encode())
        response = s.recv(1024)

    return response.decode()


def main(host, port):
    
    # Declara os dados (dá pra adaptar pra input)
    data_operacao = "22-22-2222"
    conta_cliente = "001"
    tipo_operacao = "D"
    valor_operacao = 1000
    
    request = OpClient(data_operacao, conta_cliente, tipo_operacao, valor_operacao)
    
    response = enviar_request(host, port, request)
    print("Resposta do coordenador:", response)


if __name__ == "__main__":
    main('coordenador', 7777)
