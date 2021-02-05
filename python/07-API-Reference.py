app = Flask(__name__)
db = SQLAlchemy(app)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

class User(db.Model):
    username = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.String(80))