# Use uma imagem base Python
FROM python:3.9-slim

# Diretório de trabalho
WORKDIR /app

# Copie o código do Transaction Coordinator para o contêiner
COPY coord.py .

# Instale as dependências necessárias
RUN pip install --upgrade pip

# Comando a ser executado quando o contêiner for iniciado
CMD ["python", "./coord.py"]
