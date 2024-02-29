import socket
import json
import os

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


def main():
    
    # Configuração de comunicação com o coordenador
    host = 'localhost' #'coordenador'
    port = 7777
    
    # Declara os dados (dá pra adaptar pra input)
    data_operacao = "22-22-2222"
    conta_cliente = "001"
    tipo_operacao = "C"
    valor_operacao = 1000
    
    request = OpClient(data_operacao, conta_cliente, tipo_operacao, valor_operacao)
    
    response = enviar_request(host, port, request)
    print("Resposta do servidor principal:", response)
   
    caminho_arquivo = "C:\\Users\\kelvi\\OneDrive\\Documentos\\trabaiCompDist\\credito_debito\\backup\\Docker\\saldo.txt"

    
    # Verifica se o arquivo saldo.txt existe
    if os.path.exists(caminho_arquivo):
        # Lê o valor do arquivo usando o caminho completo
        with open(caminho_arquivo, "r") as saldo_file:
            saldo_atualizado = saldo_file.read()
        print("Saldo atualizado:", saldo_atualizado)
    else:
        print("Arquivo 'saldo.txt' não encontrado.")


if __name__ == "__main__":
    main()