"""Build a standalone Windows GUI executable with PyInstaller."""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VERSION = (ROOT / "GUI_VERSION").read_text(encoding="utf-8").strip()


def main():
    if sys.platform != "win32":
        raise SystemExit("Build the Windows executable on Windows.")
    command = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
        "--onefile", "--windowed", "--name", f"PromptIR-v{VERSION}",
        "--add-data", f"{ROOT / 'GUI_VERSION'}:.",
        "--add-data", f"{ROOT / 'prompts' / 'dunhuang_single.json'}:prompts",
        "--distpath", str(ROOT / "dist"),
        "--workpath", str(ROOT / "build"),
        "--specpath", str(ROOT / "build"),
        str(ROOT / "gui.py"),
    ]
    subprocess.run(command, cwd=ROOT, check=True)
    print(ROOT / "dist" / f"PromptIR-v{VERSION}.exe")


if __name__ == "__main__":
    main()
