from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", methods=["GET"])
def index():
    response = {"message": "Workout Application API is running", "status": "success"}

    return make_response(jsonify(response), 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
