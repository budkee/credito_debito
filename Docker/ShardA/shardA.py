import queue
import threading
import time

fila_respostas = queue.Queue()

def processar_shard(solicitacao, shard):
    # Simulação do processamento
    time.sleep(2)
    
    # Simulação do retorno
    retorno = "Tudo certo por aqui!"
    
    # Enviar retorno para fila de respostas
    fila_respostas.put((solicitacao, shard, retorno))
