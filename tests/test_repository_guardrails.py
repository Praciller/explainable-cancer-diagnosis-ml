from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_local_markdown_links_and_images_exist() -> None:
    missing: list[str] = []
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for markdown in ROOT.rglob("*.md"):
        if any(part in {".venv", "node_modules"} for part in markdown.parts):
            continue
        for target in pattern.findall(markdown.read_text(encoding="utf-8")):
            clean = target.split("#", 1)[0].strip()
            if not clean or "://" in clean or clean.startswith("mailto:"):
                continue
            if not (markdown.parent / clean).resolve().exists():
                missing.append(f"{markdown.relative_to(ROOT)} -> {target}")
    assert not missing, "\n".join(missing)


def test_tracked_text_avoids_machine_paths_and_secret_files() -> None:
    forbidden_paths = ("C:" + "\\Users\\", "/" + "Users/", "/" + "home/")
    violations: list[str] = []
    tracked = (
        subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        .stdout.decode("utf-8")
        .split("\0")
    )
    for relative_path in filter(None, tracked):
        path = ROOT / relative_path
        if not path.is_file() or path.suffix.lower() in {".png", ".joblib", ".pt", ".pyc"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(value in text for value in forbidden_paths):
            violations.append(str(path.relative_to(ROOT)))
    assert not violations


def test_safety_boundary_is_present_on_primary_surfaces() -> None:
    required_phrases = ("diagnosis", "screening", "treatment", "medical advice")
    surfaces = [
        ROOT / "README.md",
        ROOT / "src" / "contracts.py",
        ROOT / "frontend" / "src" / "components" / "DisclaimerBanner.tsx",
    ]
    for surface in surfaces:
        text = surface.read_text(encoding="utf-8").lower()
        assert all(phrase in text for phrase in required_phrases), surface
