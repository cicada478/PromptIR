"""Public compiler interface; suitable for a future ComfyUI wrapper."""

from .flux import compile_flux
from .sdxl import compile_sdxl
from utils.normalizer import normalize_ir
from utils.validation import validate_ir


COMPILERS = {"sdxl": compile_sdxl, "flux": compile_flux}


def _prepare(ir, target):
    if not isinstance(target, str) or target.lower() not in COMPILERS:
        raise ValueError(f"Unsupported target: {target!r}. Choose sdxl or flux.")
    validate_ir(ir)
    return normalize_ir(ir), target.lower()


def compile_prompt(ir, target):
    """Return positive prompt text from an IR mapping and model target."""
    normalized, target = _prepare(ir, target)
    return COMPILERS[target](normalized)


def compile_negative(ir, target):
    """Return the separate negative prompt text, if supplied."""
    normalized, _ = _prepare(ir, target)
    return ", ".join(normalized.get("negative", []))


__all__ = ["compile_prompt", "compile_negative"]
