#!/usr/bin/env python3
"""Packages the reader skins under src/<id>/ for the store.

Each src/<id>/ holds a skin.json (its "id" equal to the folder's name, "preview" a picture inside
it) and the assets it names. Writes <id>.zip (the folder's contents, skin.json at the top),
previews/<id>.<ext>, and catalog.json — the list the app reads from app_reader_skin_url.

    python3 skins/build.py
"""
import json
import pathlib
import shutil
import sys
import zipfile

BASE_URL = "https://raw.githubusercontent.com/Darkrai9x/vbook-settings/main/skins/"
ROOT = pathlib.Path(__file__).resolve().parent
SKIP = {".DS_Store", "Thumbs.db"}


def package(src: pathlib.Path) -> dict:
    skin = json.loads((src / "skin.json").read_text("utf-8"))
    skin_id = skin.get("id")
    if skin_id != src.name:
        sys.exit(f"{src}: id {skin_id!r} isn't the folder's name")
    preview = src / skin.get("preview", "")
    if not skin.get("preview") or not preview.is_file():
        sys.exit(f"{src}: no preview picture")
    target = ROOT / f"{skin_id}.zip"
    # Fixed dates and order: an unchanged skin packs to the same bytes, so git sees no change.
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in src.rglob("*") if p.is_file() and p.name not in SKIP):
            info = zipfile.ZipInfo(path.relative_to(src).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())
    previews = ROOT / "previews"
    previews.mkdir(exist_ok=True)
    preview_name = f"{skin_id}{preview.suffix}"
    shutil.copyfile(preview, previews / preview_name)
    return {
        "id": skin_id,
        "name": skin.get("name", {}),
        "description": skin.get("description", {}),
        "author": skin.get("author", ""),
        "version": skin.get("version", 1),
        "minApp": skin.get("minApp", 1),
        "preview": BASE_URL + "previews/" + preview_name + f"?v={skin.get('version', 1)}",
        "url": BASE_URL + f"{skin_id}.zip?v={skin.get('version', 1)}",
        "size": target.stat().st_size,
    }


def main() -> None:
    sources = sorted(p for p in (ROOT / "src").iterdir() if (p / "skin.json").is_file())
    items = [package(src) for src in sources]
    (ROOT / "catalog.json").write_text(json.dumps({"skins": items}, indent=2, ensure_ascii=False) + "\n", "utf-8")
    for item in items:
        print(f"{item['id']}: v{item['version']}, {item['size'] // 1024} KB")


if __name__ == "__main__":
    main()
