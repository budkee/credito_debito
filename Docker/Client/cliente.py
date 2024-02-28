import socket
import json

def OpClient(data_operacao, conta_cliente, tipo, valor_operacao):
        
    request_transacao = {
        "data_operacao": data_operacao,
        "conta_cliente": conta_cliente,
        "tipo": tipo,
        "valor_operacao": valor_operacao
    }

def main():
    
    host = 'coordenador'
    port = 9999

    # Loop para processar transações na fila continuamente
    while True:
        
        #print(f"Saldo atual: {}")

        data_operacao = "22-22-2222"
        
        conta_cliente = "001"
        
        tipo = "C"
        
        valor_operacao = 1000


        operacao = OpClient(data_operacao, conta_cliente, tipo, valor_operacao)
        
        try:
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            client_socket.connect((host, port))

            request = json.dumps({
                'data': operacao['data_operacao'],
                'conta_cliente': operacao['conta_cliente'],
                'tipo': operacao['tipo'],
                'valor_operacao': operacao['valor_operacao']
            })

            client_socket.send(request.encode())

            #--------------------------resposta
            response = client_socket.recv(1024).decode()
            
            print(response)

        except socket.error as e:
            print(f"Erro de comunicação com o servidor: {e}")

        finally:
            client_socket.close()

if __name__ == "__main__":
    main()