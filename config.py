import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configurações do Swagger
    SWAGGER = {
        'title': 'API Vitivinicultura',
        'uiversion': 3
    }

    # Configurações de segurança e banco de dados
    SECRET_KEY = 'sua-chave-secreta-aqui'  # Use algo mais forte em produção
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🔐 Configuração do JWT
    JWT_SECRET_KEY = 'sua-jwt-secret-key-aqui'  # Chave usada para assinar tokens
