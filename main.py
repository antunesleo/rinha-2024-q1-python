from flask import Flask
from psycopg_pool import ConnectionPool

app = Flask(__name__)
# pool = ConnectionPool(min_size=2)
# pool.wait()

@app.route("/")
def hello_world():
    # with pool.connection() as conn:
    #     pass
    return "<p>Hello, World!</p>"
