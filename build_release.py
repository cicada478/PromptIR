"""Build a clean, portable CLI ZIP in dist/."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
BASE_FILES = [
    "VERSION", "CHANGELOG.md", "README.md", "main.py",
    "compilers/__init__.py", "compilers/sdxl.py", "compilers/flux.py",
    "utils/__init__.py", "utils/language.py", "utils/normalizer.py",
    "utils/validation.py", "schema/prompt.schema.json",
    "prompts/dunhuang_single.json",
]
GUI_FILES = ["GUI_VERSION", "gui.py", "GUI_README.md"]


def main():
    parser = argparse.ArgumentParser(description="Build a clean Prompt IR release ZIP")
    parser.add_argument("--edition", choices=("cli", "gui"), default="cli")
    args = parser.parse_args()
    edition_version = (ROOT / "GUI_VERSION").read_text(encoding="utf-8").strip() if args.edition == "gui" else VERSION
    output = ROOT / "dist" / f"prompt-ir-v{edition_version}-{args.edition}.zip"
    output.parent.mkdir(exist_ok=True)
    files = BASE_FILES + (GUI_FILES if args.edition == "gui" else [])
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name in files:
            source = ROOT / name
            archive.write(source, arcname=f"prompt_ir/{name}")
    print(output)


if __name__ == "__main__":
    main()
