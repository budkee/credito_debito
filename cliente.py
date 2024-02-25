import queue
import socket
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

    def atualizar_saldo(self, tipo, valor_operacao):
        if tipo == 'C':
            self.saldo += valor_operacao
        elif tipo == 'D':
            self.saldo -= valor_operacao

    def get_saldo(self):
        return self.saldo

def main():
    host = 'localhost'
    port = 5000

    client = Client()

    # Loop para processar transações na fila continuamente
    while True:

        print(f"Saldo atual: {client.get_saldo()}")
        # Chama o método OpClient do Cliente
        data_operacao = input("Data operação: ")  # Input fornecido pelo usuário para exemplo, você pode obter esses dados de outra forma
        conta_cliente = input("Conta cliente: ")
        tipo = input("Tipo (C ou D): ")
        valor_operacao = float(input("Valor operação: "))

        client.OpClient(data_operacao, conta_cliente, tipo, valor_operacao)

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            client_socket.connect((host, port))

            next_transaction = client.queue.get()

            request = json.dumps({
                'operation': 'OpClient',
                'data': next_transaction['data_operacao'],
                'conta_cliente': next_transaction['conta_cliente'],
                'type': next_transaction['tipo'],
                'value': next_transaction['valor_operacao']
            })
            client_socket.send(request.encode())

            #--------------------------resposta
            response = client_socket.recv(1024).decode()
            print(response)


            # se a respota do coordenador for ok então atualiza o saldo de acordo com a operação
            if response == "OK":   
                client.atualizar_saldo(next_transaction['tipo'], next_transaction['valor_operacao'])
                print(f"Saldo atualizado: {client.get_saldo()}")

        except socket.error as e:
            print(f"Erro de comunicação com o servidor: {e}")

        finally:
            client_socket.close()

if __name__ == "__main__":
    main()