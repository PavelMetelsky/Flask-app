from flask import Flask, jsonify, request
import redis
import jwt
import datetime
from functools import wraps
from flasgger import Swagger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Use environment variables
r = redis.Redis(host='redis', port=6379)

# Swagger setup
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

swagger = Swagger(app, config=swagger_config)

# Decorator for protecting routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
            
        try:
            token = token.split("Bearer ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(*args, **kwargs)
    return decorated

@app.route('/ping')
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

@app.route('/count')
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
    visits = r.incr('visits')
    return jsonify({"visits": visits})

@app.route('/login', methods=['POST'])
def login():
    """
    Get JWT token
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: password
    responses:
      200:
        description: Successful authorization
        schema:
          type: object
          properties:
            token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      401:
        description: Authorization error
        schema:
          type: object
          properties:
            message:
              type: string
              example: Invalid credentials!
    """
    auth = request.json
    
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Authentication failed'}), 401
        
    # Use password verification through secure storage
    if auth.get('username') == 'admin' and auth.get('password') == 'password':
        token = jwt.encode({
            'user': auth.get('username'),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({'token': token})
    
    return jsonify({'message': 'Invalid credentials!'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
