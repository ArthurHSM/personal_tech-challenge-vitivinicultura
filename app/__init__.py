from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    # Configurações
    app.config.from_object('app.config.Config')

    # Swagger
    Swagger(app)

    # Rotas
    from app.routes.api import api_bp
    app.register_blueprint(api_bp)

    return app