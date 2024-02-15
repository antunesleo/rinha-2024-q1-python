import json
from flask import Flask, request
from psycopg_pool import ConnectionPool

app = Flask(__name__)
pool = ConnectionPool(
    "host=localhost port=5432 dbname=rinhapython user=postgres password=postgres",
    min_size=2,
)
pool.wait()


@app.route("/")
def hello_world():
    print(request.data)
    with pool.connection() as conn:
        result = conn.execute("SELECT 1+1").fetchone()
        return f"<p>1 + 1 = {result[0]}</p>"


@app.route("/clientes/<cliente_id>/transacoes", methods=["POST"])
def cria_transacao(cliente_id):
    payload = json.loads(request.data)

    with pool.connection() as conn:
        result = conn.execute(
            f"SELECT saldo, limite FROM clientes WHERE id = {cliente_id} FOR UPDATE"
        ).fetchone()
        if result is None:
            return "", 404
        saldo, limite = result
        
        if payload["tipo"] == "c":
            saldo_futuro = saldo + payload["valor"]
        else:
            saldo_futuro = saldo - payload["valor"]

        if saldo_futuro < 0 and abs(saldo_futuro) > limite:
            return "", 422

        conn.execute(
            f"INSERT INTO transacoes (cliente_id, tipo, descricao, valor) VALUES ({cliente_id}, '{payload['tipo']}', '{payload['descricao']}', {payload['valor']})"
        )
        return "", 200
