"""Dependency-free validation of the supported JSON Schema fields."""

from collections.abc import Mapping


FIELDS = {
    "subject": {"count": int, "type": str, "gender": str, "age": str,
                "ethnicity": str, "identity": str},
    "appearance": {"face": str, "skin": str, "body": str,
                   "hair": {"color": str, "length": str, "texture": str,
                            "style": str}, "expression": str},
    "wardrobe": {"style": str, "garment": str, "materials": list,
                 "colors": list, "details": list, "accessories": list},
    "composition": {"shot": str, "subject_position": str, "pose": str,
                    "orientation": str, "layout": str, "negative_space": str},
    "environment": {"location": str, "background": str, "props": list,
                    "atmosphere": str},
    "lighting": {"type": str, "direction": str, "contrast": str,
                 "temperature": str, "effects": list},
    "camera": {"lens": str, "angle": str, "depth_of_field": str},
    "aesthetic": {"genre": list, "mood": list, "style": (str, list),
                  "details": list},
}


def _check_object(value, spec, path):
    if not isinstance(value, Mapping):
        raise ValueError(f"{path} must be an object")
    for key, item in value.items():
        if key not in spec:
            raise ValueError(f"Unknown field: {path}.{key}")
        expected = spec[key]
        name = f"{path}.{key}"
        if isinstance(expected, dict):
            _check_object(item, expected, name)
        elif expected is list or expected == (str, list):
            if expected == (str, list) and isinstance(item, str):
                continue
            if not isinstance(item, list) or any(not isinstance(x, str) for x in item):
                raise ValueError(f"{name} must be a string or an array of strings" if expected != list
                                 else f"{name} must be an array of strings")
        elif expected is int:
            if type(item) is not int or item < 1:
                raise ValueError(f"{name} must be an integer of at least 1")
        elif item is not None and not isinstance(item, expected):
            raise ValueError(f"{name} must be a string")


def validate_ir(ir):
    """Validate the supported schema subset; raise ValueError with a field path."""
    if not isinstance(ir, Mapping):
        raise ValueError("Prompt IR must be a JSON object")
    if "subject" not in ir:
        raise ValueError("Missing required field: subject")
    for key, value in ir.items():
        if key == "negative":
            if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
                raise ValueError("negative must be an array of strings")
        elif key in FIELDS:
            _check_object(value, FIELDS[key], key)
        else:
            raise ValueError(f"Unknown field: {key}")
