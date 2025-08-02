from flask import Flask
from routes.users import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)

@app.route('/')
def health_check():
    return {"status": "API is running"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)
