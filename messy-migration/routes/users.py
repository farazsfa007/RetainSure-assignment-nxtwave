from flask import Blueprint, request, jsonify
from db import get_db_connection
from models import hash_password
from utils.validators import validate_user_data

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    return jsonify([dict(row) for row in users]), 200

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user)), 200
    return jsonify({"error": "User not found"}), 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    error = validate_user_data(data)
    if error:
        return jsonify({"error": error}), 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (data['name'], data['email'], hash_password(data['password']))
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User created successfully"}), 201

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email required"}), 400

    conn = get_db_connection()
    conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (data['name'], data['email'], user_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "User updated successfully"}), 200

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted"}), 200

@user_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name', '')
    if not name:
        return jsonify({"error": "Missing name parameter"}), 400

    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f'%{name}%',)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in users]), 200

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400

    hashed_pw = hash_password(data['password'])

    conn = get_db_connection()
    user = conn.execute("SELECT id FROM users WHERE email = ? AND password = ?", (data['email'], hashed_pw)).fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success", "user_id": user['id']}), 200
    return jsonify({"status": "failed"}), 401
