# Use uma imagem base Python
FROM python:3.9-slim

WORKDIR /app

# Copie o código do Shard A para o contêiner
COPY shardA.py .

# Instale as dependências necessárias
RUN pip install --upgrade pip

# Comando a ser executado quando o contêiner for iniciado
CMD ["python", "./shardA.py"]
