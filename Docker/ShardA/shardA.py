import threading
import socket
import json
import os


def handle_request(coord_socket, address):
    # Recebe os dados do coordenador
    data = coord_socket.recv(1024).decode()
    request = json.loads(data)
    
    # Puxa os dados de interesse
    tipo_operacao = request["tipo_operacao"]
    valor_operacao = request["valor_operacao"]


    # Obtém o diretório de execução do script
    diretorio_execucao = os.path.dirname(os.path.abspath(__file__))
    
    # Define o nome do arquivo
    nome_arquivo = "saldo.txt"
    
    # Cria o caminho completo para o arquivo
    saldo_file_path = os.path.join(diretorio_execucao, "data", nome_arquivo)


    try:
        # Leitura do arquivo
        with open(saldo_file_path, "r") as saldo_file:
            saldo_atual = int(saldo_file.read())
            novo_saldo = saldo_atual + valor_operacao
        # Escrita no arquivo
        with open(saldo_file_path, "w") as saldo_file:
            saldo_file.write(str(novo_saldo))
    
        # Simulação de operação de crédito
        saldo_atualizado = saldo_atual + valor_operacao
    
        # Retorna para o coordenador
        response = f"Ok! Saldo atualizado: {saldo_atualizado}"
        coord_socket.send(json.dumps(response).encode())
    
    except Exception as e:
        print(f"Erro ao manipular o arquivo {saldo_file_path}: {e}")
        response = f"Erro ao atualizar saldo: {e}"
        coord_socket.send(json.dumps(response).encode())

    coord_socket.close()


def shard_a(host, port):
    
    # Conexão por streamming
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print("Servidor shardA escutando em", (host, port))
        
        while True:
            coord_socket, address = server_socket.accept()
            print(f"[*] Conexão estabelecida com {address[0]}:{address[1]}")
            coord_thread = threading.Thread(target=handle_request, args=(coord_socket, address))
            coord_thread.start()


if __name__ == "__main__":

    shard_a('0.0.0.0', 8888)