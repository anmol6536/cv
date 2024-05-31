from pathlib import Path


CURRENT_FILE = Path(__file__).resolve()


class GlobalPaths:
    ROOT = CURRENT_FILE.parent.parent
    TEXT_YAML = ROOT / "static" / "open_text" / "generic_text.yaml"
    IMAGE_FOLDER = ROOT / "static" / "images"
    ICONS_FOLDER = ROOT / "static" / "icons"
