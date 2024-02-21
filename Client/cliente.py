import queue

# Classe para o componente Cliente
class Client:

    # Construtor de inicialização do objeto
    def __init__(self):
        self.queue = queue.Queue()

    # Operação de solicitação
    def OpClient(self, data_operacao, conta_cliente, tipo, valor_operacao):
        
        # Organização dos dados de interesse
        request_transacao = {
            "data_operacao": data_operacao,
            "conta_cliente": conta_cliente,
            "tipo": tipo,
            "valor_operacao": valor_operacao
        }

        self.queue.put(request_transacao)

        # Tente esperar a resposta da fila
        try:
            # Espere a resposta em até 5 segundos
            response = self.queue.get(timeout=5) 

            # Retorno da resposta ao Cliente
            if response == "OK":
                print("Transação concluída com sucesso")
            else:
                print("Transação falhou")
        # Caso a fila esteja vazia 
        except queue.Empty:
            print("Timeout: Servidor não respondeu a tempo")

# Exemplo de uso do Client
client = Client()
client.OpClient("21/02/2024", "123456", "C", 100)
