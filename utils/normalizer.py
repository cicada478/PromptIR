"""Normalize a few common aliases without changing the caller's mapping."""

from copy import deepcopy


GENDER_ALIASES = {
    "woman": "female", "women": "female", "女性": "female",
    "man": "male", "men": "male", "男性": "male",
}


def normalize_ir(ir):
    normalized = deepcopy(ir)
    gender = normalized["subject"].get("gender")
    if gender:
        normalized["subject"]["gender"] = GENDER_ALIASES.get(
            gender.casefold(), gender.strip()
        )
    return normalized
