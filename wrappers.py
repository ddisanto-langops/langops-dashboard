import os
import logging
from functools import wraps
from flask import request, jsonify

logger = logging.getLogger(__name__)

def require_x_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. Grab the key from the 'X-Auth' header
        provided_key = request.headers.get('X-Auth')
        secret_key = os.environ.get('X_AUTH')

        # 2. Validate
        if provided_key and provided_key == secret_key:
            logger.info(f"X-Auth validated for path: {request.path}")
            return f(*args, **kwargs)
        
        # 3. Handle Failure
        logger.warning(f"Invalid or missing X-Auth key for path: {request.path}")
        return jsonify({"error": "Unauthorized Access"}), 401
        
    return decorated_function