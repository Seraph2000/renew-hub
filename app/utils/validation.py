from datetime import datetime

class ValidationError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


def validate_payload(data, required_fields):
    """
    Validate that required fields exist and have correct types.
    """
    if not isinstance(data, dict):
        raise ValidationError("Payload must be a JSON object")

    for field, field_type in required_fields.items():
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")

        value = data[field]

        # Type checking
        if field_type == int and not isinstance(value, int):
            raise ValidationError(f"Field '{field}' must be an integer")

        if field_type == float and not isinstance(value, (int, float)):
            raise ValidationError(f"Field '{field}' must be a number")

        if field_type == str and not isinstance(value, str):
            raise ValidationError(f"Field '{field}' must be a string")

        if field_type == "date":
            try:
                datetime.fromisoformat(value)
            except Exception:
                raise ValidationError(f"Field '{field}' must be an ISO date string")

    return True
