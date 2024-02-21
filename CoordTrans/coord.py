import queue

# Classe para o componente TransactionCoordinator
class CoordTrans:

    # Construtor do objeto
    def __init__(self, shard_a, shard_b):
        self.shard_a = shard_a
        self.shard_b = shard_b

    # Operação de processamento
    def process_transacao(self, request_transacao):
        
        data_operacao = request_transacao["data_operacao"]
        conta_cliente = request_transacao["conta_cliente"]
        tipo = request_transacao["tipo"]
        valor_operacao = request_transacao["valor_operacao"]

        # Tratamento de erros
        try:            
            
            # Verifique o tipo da transação
            if tipo == "C":
                self.shard_a.Credito(data_operacao, conta_cliente, valor_operacao)
            elif tipo == "D":
                self.shard_b.Debito(data_operacao, conta_cliente, valor_operacao)
            else:
                print("Tipo de transação inválido")
        
        except Exception as e:
            print(f"Erro ao processar transação: {str(e)}")

# Exemplo de uso do Transaction Coordinator
shard_a = ShardA()
shard_b = ShardB()
coordenador = CoordTrans(shard_a, shard_b)
