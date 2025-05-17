from flask import Blueprint, request, jsonify
from app.models.user_model import User  # Importa apenas o User
from app import db  # Importa db do __init__.py
from flasgger import swag_from

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
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password are required"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 409

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201