from flask import Flask, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

@app.route('/count')
def count():
    visits = r.incr('visits')
    return jsonify({"visits": visits})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)