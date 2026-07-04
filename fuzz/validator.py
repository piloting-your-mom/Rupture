import jsonschema
from jsonschema import validate

def validate_response_schema(response_json: dict, schema: dict) -> tuple[bool, str | None]:
    """
    Validates a JSON response against a user-provided JSON Schema.
    Returns (True, None) if valid, or (False, "error message") if invalid.
    """
    try:
        validate(instance=response_json, schema=schema)
        return True, None
    except jsonschema.exceptions.ValidationError as err:
        # Captures structural corruptions on successful HTTP responses
        return False, f"Schema Violation: {err.message}"
    except jsonschema.exceptions.SchemaError as err:
        return False, f"Invalid Template Schema: {err.message}"