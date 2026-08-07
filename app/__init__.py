from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///olympus.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from app.routes.gods import gods_bp
    from app.routes.creatures import creatures_bp
    from app.routes.myths import myths_bp
    app.register_blueprint(gods_bp)
    app.register_blueprint(creatures_bp)
    app.register_blueprint(myths_bp)

    with app.app_context():
        db.create_all()

    return app