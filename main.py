import json
import os
from datetime import datetime, timezone
from flask import Flask, request
from psycopg_pool import ConnectionPool

database_host = os.environ.get("DATABASE_HOST")
database_port = int(os.environ.get("DATABASE_PORT"))
database_name = os.environ.get("DATABASE_NAME")
database_password = os.environ.get("DATABASE_PASSWORD")
database_user = os.environ.get("DATABASE_USER")

app = Flask(__name__)
pool = ConnectionPool(
    f"host={database_host} port={database_port} dbname={database_name} user={database_user} password={database_password}",
    min_size=14,
    max_size=50,
)
pool.wait()


@app.route("/clientes/<cliente_id>/transacoes", methods=["POST"])
def cria_transacao(cliente_id):
    payload = json.loads(request.data)

    for campo in ("tipo", "valor", "descricao"):
        if campo not in payload:
            return "", 422

    if payload["tipo"] not in ("c", "d"):
         return "", 422

    if not isinstance(payload["valor"], int):
        return "", 422

    if not isinstance(payload["descricao"], str):
        return "", 422

    descricao_len = len(payload["descricao"])
    if descricao_len > 10 or descricao_len < 1:
        return "", 422

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
        conn.execute(f"UPDATE clientes SET saldo = {saldo_futuro} WHERE id={cliente_id}")
        return {"limite": limite, "saldo": saldo_futuro}, 200


@app.route("/clientes/<cliente_id>/extrato", methods=["GET"])
def extrato(cliente_id):
    with pool.connection() as conn:
        result = conn.execute(
            f"SELECT saldo, limite FROM clientes WHERE id = {cliente_id}"
        ).fetchone()
        if result is None:
            return "", 404
        saldo, limite = result
        
        resposta = {
            "saldo": {
                "total": saldo,
                "data_extrato": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "limite": limite,
            },
            "ultimas_transacoes": []
        }

        result = conn.execute(
            f"SELECT valor, tipo, descricao, realizada_em FROM transacoes WHERE cliente_id = {cliente_id} ORDER BY realizada_em DESC LIMIT 10"
        ).fetchall()
        for transacao_db in result:
            resposta["ultimas_transacoes"].append({
                "valor": transacao_db[0],
                "tipo": transacao_db[1],
                "descricao": transacao_db[2],
                "realizada_em": transacao_db[3].isoformat().replace("+00:00", "Z"),
            })

        return resposta, 200