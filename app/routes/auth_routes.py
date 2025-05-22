from flask import Blueprint, request, jsonify
from flasgger import swag_from
from flask_jwt_extended import create_access_token
from app import db
from app.models.user_model import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'description': 'Criação de novo usuário',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Usuário criado com sucesso',
            'examples': {'application/json': {'message': 'User created successfully'}}
        },
        400: {
            'description': 'Dados ausentes ou inválidos'
        },
        409: {
            'description': 'Usuário já existe'
        }
    }
})
def signup():
    data = request.get_json() or {}

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 409

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'description': 'Autentica usuário e retorna token JWT',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login bem-sucedido com token JWT',
            'examples': {
                'application/json': {
                    'access_token': 'jwt-token-aqui'
                }
            }
        },
        401: {
            'description': 'Credenciais inválidas'
        }
    }
})
def login():
    data = request.get_json() or {}

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "Credenciais inválidas"}), 401

    # usa o método do modelo que faz bcrypt.check_password_hash corretamente
    if not user.check_password(password):
        return jsonify({"msg": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200
