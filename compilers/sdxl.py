"""SDXL: concise, comma-separated descriptive phrases."""

from utils.language import hair_phrase, join_words, subject_phrase


def compile_sdxl(ir):
    subject = ir["subject"]
    appearance = ir.get("appearance", {})
    wardrobe = ir.get("wardrobe", {})
    composition = ir.get("composition", {})
    environment = ir.get("environment", {})
    lighting = ir.get("lighting", {})
    camera = ir.get("camera", {})
    aesthetic = ir.get("aesthetic", {})

    parts = [
        subject_phrase(subject),
        composition.get("shot"), composition.get("subject_position"),
        composition.get("pose"), composition.get("orientation"),
        composition.get("layout"), composition.get("negative_space"),
        appearance.get("face"), appearance.get("skin"),
        appearance.get("body"), hair_phrase(appearance.get("hair", {})),
        appearance.get("expression"),
        join_words(wardrobe.get("style"), wardrobe.get("garment")),
    ]
    for key in ("materials", "colors", "details", "accessories"):
        parts.extend(wardrobe.get(key, []))
    parts.extend(environment.get("props", []))
    parts.extend([
        environment.get("location"), environment.get("background"),
        environment.get("atmosphere"), lighting.get("type"),
        lighting.get("direction"), lighting.get("contrast"),
        lighting.get("temperature"),
    ])
    parts.extend(lighting.get("effects", []))
    parts.extend([
        camera.get("angle"),
        join_words(camera.get("lens"), "lens") if camera.get("lens") else None,
        join_words(camera.get("depth_of_field"), "depth of field")
        if camera.get("depth_of_field") else None,
    ])
    for key in ("genre", "mood", "style", "details"):
        value = aesthetic.get(key, [])
        parts.extend(value if isinstance(value, list) else [value])
    return ", ".join(part for part in parts if part)
