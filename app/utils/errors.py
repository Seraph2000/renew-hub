def error_response(error_type, message, status):
    return {
        "error": {
            "type": error_type,
            "message": message,
            "status": status
        }
    }, status
