from pathlib import Path

ROOT = Path(__file__).resolve().parent


def asset(name):
    return str(ROOT / name)
