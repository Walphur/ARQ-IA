"""Ensure banner client contract: status only, never /ready."""

from pathlib import Path


def _strip_comments_and_strings_noise(source: str) -> str:
    """Keep import/call surface; ignore prose comments that mention /ready."""
    lines = []
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("/*") or stripped.startswith("*") or stripped.startswith("//"):
            continue
        lines.append(line)
    return "\n".join(lines)


def test_platform_status_js_does_not_call_ready():
    root = Path(__file__).resolve().parents[2]
    status_js = _strip_comments_and_strings_noise(
        (root / "frontend/src/infrastructure/platformStatus.js").read_text(encoding="utf-8")
    )
    banner_js = _strip_comments_and_strings_noise(
        (root / "frontend/src/components/DegradationBanner.js").read_text(encoding="utf-8")
    )
    assert "/v1/platform/status" in status_js
    assert "`${base}/ready`" not in status_js
    assert '"/ready"' not in status_js
    assert "'/ready'" not in status_js
    assert "fetchPlatformStatus" in banner_js
    assert "`${base}/ready`" not in banner_js
    assert '"/ready"' not in banner_js
    assert "'/health'" not in banner_js
    assert '"/health"' not in banner_js
