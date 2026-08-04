#!/usr/bin/env python3
"""자동 갱신 전에 리디자인된 정적 화면 구조가 유지되는지 확인한다."""

from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
required_markers = (
    'id="currentTemp"',
    'id="forecast"',
    'id="keyList"',
    'id="conditionResult"',
    'src="app.js"',
    'href="styles.css"',
)
missing = [marker for marker in required_markers if marker not in text]
if missing:
    raise SystemExit("index.html 필수 구조 누락: " + ", ".join(missing))

print("리디자인된 index.html 구조 확인 완료")
