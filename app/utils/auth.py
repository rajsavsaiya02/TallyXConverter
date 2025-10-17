# app/utils/auth.py
from functools import wraps
from flask import request, jsonify, current_app


def password_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401

        try:
            auth_type, provided_password = auth_header.split(None, 1)
            if auth_type.lower() != 'bearer' or provided_password != current_app.config['ADMIN_PASSWORD']:
                raise ValueError()
        except ValueError:
            return jsonify({"error": "Invalid authorization"}), 403

        return f(*args, **kwargs)

    return decorated_function