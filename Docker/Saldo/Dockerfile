# Use uma imagem base Python
FROM python:3.9-slim

WORKDIR /app

# Copie o arquivo de texto para o contêiner
COPY saldo.txt /app/data/saldo.txt

# Defina as permissões de leitura e escrita para o arquivo
RUN chmod 644 /app/data/saldo.txt

# Comando a ser executado quando o contêiner for iniciado
CMD ["tail", "-f", "/dev/null"]
