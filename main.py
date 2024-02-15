from flask import Flask
from psycopg_pool import ConnectionPool

app = Flask(__name__)
pool = ConnectionPool("host=localhost port=5432 dbname=rinhapython user=postgres password=postgres", min_size=2)
pool.wait()

@app.route("/")
def hello_world():
    with pool.connection() as conn:
        result = conn.execute("SELECT 1+1").fetchone()
        return f"<p>1 + 1 = {result[0]}</p>"
