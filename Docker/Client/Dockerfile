# Use a imagem base Python
FROM python:3.9-slim

WORKDIR /app

# Copie o código do Cliente para o contêiner
COPY cliente.py .

# Instale as dependências necessárias
RUN pip install --upgrade pip

# Comando a ser executado quando o contêiner for iniciado
CMD ["python", "./cliente.py"]
