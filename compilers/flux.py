"""FLUX: connected natural-language scene description."""

from utils.language import hair_phrase, join_list, join_words, subject_phrase, with_article


def compile_flux(ir):
    subject = ir["subject"]
    appearance = ir.get("appearance", {})
    wardrobe = ir.get("wardrobe", {})
    composition = ir.get("composition", {})
    environment = ir.get("environment", {})
    lighting = ir.get("lighting", {})
    camera = ir.get("camera", {})
    aesthetic = ir.get("aesthetic", {})
    sentences = []

    who = subject_phrase(subject)
    shot = composition.get("shot")
    described_subject = who if subject.get("count", 1) > 1 else with_article(who)
    opening = f"The image depicts {described_subject}"
    if shot:
        opening += f" in {with_article(shot)}"
    placement = join_list([composition.get(key) for key in
                           ("subject_position", "pose", "orientation", "layout")])
    if placement:
        opening += f", {placement}"
    sentences.append(opening + ".")

    traits = [appearance.get(key) for key in ("face", "skin", "body")]
    traits += [hair_phrase(appearance.get("hair", {})), appearance.get("expression")]
    traits = [item for item in traits if item]
    if traits:
        sentences.append("The subject has " + join_list(traits) + ".")

    clothing = join_words(wardrobe.get("style"), wardrobe.get("garment"))
    materials = wardrobe.get("materials", [])
    colors = wardrobe.get("colors", [])
    details = wardrobe.get("details", []) + wardrobe.get("accessories", [])
    if clothing:
        sentence = f"The subject wears {with_article(clothing)}"
        if materials:
            sentence += " made of " + join_list(materials)
        if colors:
            sentence += " in " + join_list(colors)
        if details:
            sentence += ", with " + join_list(details)
        sentences.append(sentence + ".")
    elif materials or colors or details:
        sentences.append("The wardrobe includes " + join_list(materials + colors + details) + ".")

    setting = [environment.get(key) for key in ("location", "background", "atmosphere")]
    setting += environment.get("props", [])
    setting = [item for item in setting if item]
    if setting:
        sentences.append("The scene features " + join_list(setting) + ".")

    light = [lighting.get(key) for key in ("type", "direction", "contrast", "temperature")]
    light += lighting.get("effects", [])
    light = [item for item in light if item]
    if light:
        sentences.append("Lighting uses " + join_list(light) + ".")

    camera_items = [camera.get("angle")]
    if camera.get("lens"):
        camera_items.append(join_words(camera["lens"], "lens"))
    if camera.get("depth_of_field"):
        camera_items.append(join_words(camera["depth_of_field"], "depth of field"))
    camera_items = [item for item in camera_items if item]
    if camera_items:
        sentences.append("The camera uses " + join_list(camera_items) + ".")

    style = []
    for key in ("genre", "mood", "style", "details"):
        value = aesthetic.get(key, [])
        style.extend(value if isinstance(value, list) else [value])
    if style:
        sentences.append("The overall aesthetic is " + join_list(style) + ".")
    return " ".join(sentences)
