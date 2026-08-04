#!/usr/bin/env python3
"""기상 갱신 전에 폭염 안전 가이드의 필수 화면 구조를 검증한다."""

from pathlib import Path

files = {
    "index.html": Path("index.html").read_text(encoding="utf-8"),
    "app.js": Path("app.js").read_text(encoding="utf-8"),
    "styles.css": Path("styles.css").read_text(encoding="utf-8"),
}

required_markers = {
    "index.html": (
        'id="currentTemp"',
        'id="forecast"',
        'id="keyList"',
        'id="conditionResult"',
        'id="homeSupport"',
        'src="app.js"',
        'href="styles.css"',
    ),
    "app.js": (
        "const guides",
        "function renderForecast",
        "function renderHomeSupport",
        "function renderGuide",
        "weather.json",
    ),
    "styles.css": (
        ":root",
        ".forecast-grid",
        ".guide-list",
        ".info-block",
    ),
}

for filename, markers in required_markers.items():
    missing = [marker for marker in markers if marker not in files[filename]]
    if missing:
        raise SystemExit(f"{filename} 필수 구조 누락: " + ", ".join(missing))

print("리디자인 화면과 기상 연동 필수 구조 확인 완료")
