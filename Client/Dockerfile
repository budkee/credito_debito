# Use a imagem base Python
FROM python:3.9-slim

# Copie o código do Client para o contêiner
COPY cliente.py .

# Instale as dependências necessárias
RUN pip install queue

# Comando a ser executado quando o contêiner for iniciado
CMD ["python", "./client.py"]