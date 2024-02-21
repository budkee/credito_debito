import queue

# Classe do componente ShardB
class ShardB:

    # Construtor do objeto
    def __init__(self):
        self.queue = queue.Queue()


    # Operação em Débito
    def Debito(self, data_operacao, conta_cliente, valor_operacao):

        # Simulação de persistência em banco de dados
        try:
            # Lógica de débito no banco de dados de Shard B
            print("Executando transação de débito em Shard B")
            
            response = "OK"  # Simulação de sucesso
            self.queue.put(response)

        except Exception as e:
            print(f"Erro ao processar débito em Shard B: {str(e)}")

# Exemplo de uso do Shard B
shard_b = ShardB()
