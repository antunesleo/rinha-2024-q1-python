# rinha-2024-q1-python

Implementação da rinha de backend 2024 q1 em python

## Stack

* Framework Web: [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* Biblioteca de banco de dados e pool de conexões: [psycopg3](https://www.psycopg.org/psycopg3/)
* Banco de dados: [Postgres](https://www.postgresql.org/)
* WSGI Server: [Gunicorn](https://gunicorn.org/) async worker com [gevent](https://www.gevent.org/)
* Load balancer: [nginx](https://www.nginx.com/)

## Resultados

A ser definido

## Estratégia

Rodando a api com async workers temos concorrencia com corotinas e não precisamos de diversos forks de processos (workers). Isso é interessante devido ao limite de CPU e memória. Ter diversos processos com menos de 1 CPU não é interessante devido a sobrecarga de troca de contexto, além de que cada processo duplica o uso base de memória. Tal estratégia permitiu alocar mais memória e CPU para o banco de dados, que somado a algumas configurações de buffers melhorou o desempenho das consultas

## Rodando

```sh
docker-compose up
```

## Rodando e buildando localmente

```sh
docker-compose up -f docker-compose.local.yml
```