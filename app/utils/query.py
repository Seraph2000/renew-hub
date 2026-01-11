from app.utils.validation import ValidationError
from datetime import datetime

def parse_query_params(schema, args):
    parsed = {}

    for key, expected_type in schema.items():
        raw = args.get(key)

        if raw is None:
            continue

        if expected_type == int:
            try:
                parsed[key] = int(raw)
            except ValueError:
                raise ValidationError(f"{key} must be an integer")

        elif expected_type == float:
            try:
                parsed[key] = float(raw)
            except ValueError:
                raise ValidationError(f"{key} must be a float")

        elif expected_type == "date":
            try:
                parsed[key] = datetime.fromisoformat(raw).date()
            except Exception:
                raise ValidationError(f"Invalid date: {raw}")

        else:
            parsed[key] = raw

    return parsed
