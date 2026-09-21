from flask import Flask

from config import SQLALCHEMY_DATABASE_URI
from models import db
from views import QRCodeView


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Register QR Code view
app.add_url_rule(
    "/",
    view_func=QRCodeView.as_view("generator")
)


@app.context_processor
def inject_global_vars():
    return {
        "title": "Generator QRCode"
    }


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)