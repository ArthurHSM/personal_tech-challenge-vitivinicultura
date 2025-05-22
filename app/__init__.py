from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_jwt_extended import JWTManager  # 🔐 Importa JWT
from config import Config

db = SQLAlchemy()
jwt = JWTManager()  # 🔐 Instância JWT

def create_app():
    app = Flask(__name__)

    # Configurações
    app.config.from_object(Config)

    # Banco de dados
    db.init_app(app)

    # JWT
    jwt.init_app(app)  # 🔐 Inicializa JWT com o app

    # Swagger
    Swagger(app)

    # Rotas
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
