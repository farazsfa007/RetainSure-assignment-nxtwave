# CHANGES.md

## 🔍 Major Issues Identified

1. SQL Injection: Direct use of f-strings with SQL statements.
2. Plain Text Passwords: Storing passwords without encryption.
3. No Input Validation: Open to bad or malicious inputs.
4. Missing Proper HTTP Status Codes.
5. No Code Separation: Everything was in `app.py`.

---

## 🔧 Changes Made

- Used parameterized queries to prevent SQL injection.
- Separated concerns: `routes`, `utils`, `models`, and `db`.
- Added SHA256 password hashing.
- Included validation utilities for request data.
- Used `jsonify` and proper status codes.
- Removed insecure debug prints.

---

## 🧠 Assumptions & Trade-offs

- Used SHA256 for hashing instead of `bcrypt` for simplicity, but bcrypt is better for real-world use.
- SQLite retained for quick setup; would recommend PostgreSQL for production.
- Didn’t add token-based authentication (like JWT) due to scope constraints.

---

## 🕒 If I Had More Time

- Add token-based authentication (JWT).
- Write more unit tests using `pytest` or `unittest`.
- Add Docker and deployment scripts.
- Integrate SQLAlchemy ORM instead of raw SQL.

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python init_db.py
python app.py
