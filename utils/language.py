"""Small phrase helpers shared by model compilers."""


def join_words(*items):
    return " ".join(item for item in items if item)


def join_list(items):
    items = [item for item in items if item]
    if len(items) < 2:
        return items[0] if items else ""
    if len(items) == 2:
        return " and ".join(items)
    return ", ".join(items[:-1]) + ", and " + items[-1]


def with_article(phrase):
    if not phrase or phrase.lower().startswith(("a ", "an ", "the ")):
        return phrase
    article = "an" if phrase[0].lower() in "aeiou" else "a"
    return f"{article} {phrase}"


def hair_phrase(hair):
    if not hair:
        return ""
    parts = [hair.get(key) for key in ("length", "texture", "color")]
    if hair.get("style"):
        parts.append("hair")
        return join_words(*parts) + ", " + hair["style"]
    return join_words(*parts, "hair") if any(parts) else ""


def subject_phrase(subject):
    count = subject.get("count", 1)
    identity = subject.get("identity")
    if identity:
        base = identity
    else:
        person = subject.get("gender") or subject.get("type") or "subject"
        if person == "female":
            person = "woman" if count == 1 else "women"
        elif person == "male":
            person = "man" if count == 1 else "men"
        base = join_words(subject.get("age"), subject.get("ethnicity"), person)
    return join_words(str(count) if count > 1 else None, base)
