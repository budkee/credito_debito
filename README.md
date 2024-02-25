# Trabalho Prático | Computação Distribuída

## Objetivo

- Implementar os códigos para o processamento de transações em crédito e débito aos seguintes componentes do sistema de transação bancária:

    - Client
    - Transaction Coordinator
    - ShardA
    - ShardB

## Estratégia de Implementação

1. Escreva o código a ser executado por cada componente utilizando a política First In First Out (FIFO).

    - [Código | Cliente](./Client/cliente.py)
    - [Código | Coordenador da Transação](./CoordTrans/coord.py)
    - [Código | ShardA](./ShardA/shardA.py)
    - [Código | ShardB](./ShardB/shardB.py)

2. Para implementação do sistema em questão, serão criados um container para cada componente pela plataforma Docker.

    - [Dockerfile | Cliente](./Client/Dockerfile)
    - [Dockerfile | Coordenador da Transação](./CoordTrans/Dockerfile)
    - [Dockerfile | ShardA](./ShardA/Dockerfile)
    - [Dockerfile | ShardB](./ShardB/Dockerfile)

2.1 Dentro do diretório de cada componente, construa as imagens criadas no Dockerfile.

    docker build -t nome-image -f Dockerfile.nome .


