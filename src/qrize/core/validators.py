from jsonschema import Draft7Validator, validate, ValidationError
from typing import Dict, Optional

from jsonschema.exceptions import SchemaError


from qrize.core.types import Result


def validate_against_schema(entry: object, schema: Dict) -> Result[bool]:
    """
    Validate an entry against a five jsonschema
    """
    try:
        validate(entry, schema)
        return (None, True)

    except ValidationError:
        return ("Failed to validate entry against schema, skipping.", False)


def validate_schema(schema: Dict) -> Result[bool]:
    """
    Validate schema
    """

    try:
        Draft7Validator.check_schema(schema)
        return (None, True)

    except SchemaError:
        return ("Invalid schema", False)


def has_property(schema: Dict, property: Optional[str]) -> bool:
    """
    Check wether the schema has a given prop
    """
    return "required" in schema and property in schema["required"]
