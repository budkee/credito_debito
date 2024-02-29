import socket
import json
import time
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
    host = 'coordenador'
    port = 7777
    
    # Declara os dados (dá pra adaptar pra input)
    data_operacao = "22-22-2222"
    conta_cliente = "001"
    tipo_operacao = "D"
    valor_operacao = 1000
    
    # Envio e recebimento de dados
    request = OpClient(data_operacao, conta_cliente, tipo_operacao, valor_operacao)
    response = enviar_request(host, port, request)

    # Resposta do coordenador
    print(response)
    time.sleep(3)
    
    # Obtém o diretório de execução do script
    diretorio_execucao = os.path.dirname(os.path.abspath(__file__))

    # Define o nome do arquivo
    nome_arquivo = "saldo.txt"

    # Cria o caminho completo para o arquivo
    caminho_arquivo = os.path.join(diretorio_execucao, "data", nome_arquivo)

    # Verifica se o arquivo saldo.txt existe
    if os.path.exists(caminho_arquivo):
        # Se a resposta do coord for "Transação c"
        if response == 'Transação concluída com sucesso!':
            # Lê o valor do arquivo usando o caminho completo
            with open(caminho_arquivo, "r") as saldo_file:
                saldo_atualizado = saldo_file.read()
                print("Saldo atualizado:", saldo_atualizado)
    else:
        print("Arquivo 'saldo.txt' não encontrado.")


if __name__ == "__main__":
    main()