import queue

# Classe para o componente ShardA
class ShardA:
    
    # Construtor do objeto
    def __init__(self):
        self.queue = queue.Queue()

    # Operação de Crédito
    def Credito(self, data_operacao, conta_cliente, valor_operacao):
        # Simulação de persistência em banco de dados
        try:
            # Lógica de crédito no banco de dados de Shard A
            print("Executando transação de crédito em Shard A")
            # Simula persistência
            # Aqui você pode adicionar código para interagir com o banco de dados de Shard A
            response = "OK"  # Simulação de sucesso
            self.queue.put(response)
        except Exception as e:
            print(f"Erro ao processar crédito em Shard A: {str(e)}")

# Exemplo de uso do Shard A
shard_a = ShardA()
