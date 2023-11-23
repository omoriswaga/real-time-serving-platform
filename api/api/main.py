from flask import Flask, jsonify, request
from SQLiteDatabase import SQLLiteDatabase
from AggregatedRepository import AggregatedRepository
import time


app = Flask(__name__)

FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

SQLITE_DB_PATH = "/data/db.sqlite"


@app.route("/aggregated", methods=["GET", "POST"])
def aggregated():
    db = SQLLiteDatabase(SQLITE_DB_PATH)
    repository = AggregatedRepository(db)

    status_code = 200
    rows = repository.get_all()

    return jsonify(rows), status_code


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
