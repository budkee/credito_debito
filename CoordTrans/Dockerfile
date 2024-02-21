# Use uma imagem base Python
FROM python:3.9-slim

# Copie o código do Transaction Coordinator para o contêiner
COPY coord.py .

# Instale as dependências necessárias
RUN pip install queue

# Comando a ser executado quando o contêiner for iniciado
CMD ["python", "./coord.py"]
