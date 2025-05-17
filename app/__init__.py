from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configurações
    app.config.from_object('config.Config')

    # Banco de dados
    db.init_app(app)

    # Swagger
    Swagger(app)  # ou com config customizado (opcional, posso te mostrar)

    # Importa e registra as rotas
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Se tiver outras rotas, registre aqui no futuro
    # from app.routes.scraping_routes import scraping_bp
    # app.register_blueprint(scraping_bp, url_prefix="/scraping")

    return app
