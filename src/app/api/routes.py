from flask import Blueprint, jsonify
from app.extensions import redis_client
from app.auth.decorators import token_required

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/ping')
def ping():
    """
    Check API availability
    ---
    responses:
      200:
        description: API is working
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
    """
    return jsonify({"status": "ok"})

@api_bp.route('/count')
@token_required
def count():
    """
    Visit counter (JWT authorization required)
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Format - Bearer {token}
        
    responses:
      200:
        description: Returns visit count
        schema:
          type: object
          properties:
            visits:
              type: integer
              example: 42
      401:
        description: Authorization error
        schema:
          type: object
          properties:
            message:
              type: string
              example: Token is missing!
    """
    visits = redis_client.incr('visits')
    return jsonify({"visits": visits})