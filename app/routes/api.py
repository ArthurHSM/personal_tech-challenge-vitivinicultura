from flask import Blueprint, jsonify
from flasgger import swag_from

api_bp = Blueprint('api', __name__)

@api_bp.route("/health", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'API está funcionando',
            'examples': {
                'application/json': {'status': 'ok'}
            }
        }
    }
})
def health_check():
    return jsonify({"status": "ok"})
