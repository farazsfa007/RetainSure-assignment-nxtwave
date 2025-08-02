def validate_user_data(data):
    if not data.get("name"):
        return "Name is required"
    if not data.get("email"):
        return "Email is required"
    if not data.get("password") or len(data['password']) < 6:
        return "Password must be at least 6 characters long"
    return None
