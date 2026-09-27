"""Command line entry point for the standalone Prompt IR compiler."""

import argparse
import json
import sys
from pathlib import Path

from compilers import compile_negative, compile_prompt

VERSION = Path(__file__).with_name("VERSION").read_text(encoding="utf-8").strip()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compile a Prompt IR JSON file.")
    parser.add_argument("input", type=Path, nargs="?", help="Path to a UTF-8 Prompt IR JSON file")
    parser.add_argument("--target", choices=("sdxl", "flux"))
    parser.add_argument("--version", action="version", version=f"Prompt IR {VERSION}")
    args = parser.parse_args(argv)
    if args.input is None or args.target is None:
        parser.error("input and --target are required unless --version is used")

    try:
        with args.input.open("r", encoding="utf-8") as stream:
            ir = json.load(stream)
        positive = compile_prompt(ir, args.target)
        negative = compile_negative(ir, args.target)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        parser.exit(2, f"Error: {exc}\n")

    print("Positive prompt:\n" + positive)
    print("\nNegative prompt:\n" + negative)
    return 0


if __name__ == "__main__":
    sys.exit(main())
