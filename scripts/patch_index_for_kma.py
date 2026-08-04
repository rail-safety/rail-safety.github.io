#!/usr/bin/env python3
"""기상 갱신 전 최신 모바일 UI 구조가 유지되는지 검증한다."""

from pathlib import Path
import re

index_path = Path("index.html")
app_path = Path("app.js")
styles_path = Path("styles.css")
refresh_path = Path("refresh.css")
typography_path = Path("typography-fix.css")

index = index_path.read_text(encoding="utf-8")
app = app_path.read_text(encoding="utf-8")
styles = styles_path.read_text(encoding="utf-8")
refresh = refresh_path.read_text(encoding="utf-8")
typography = typography_path.read_text(encoding="utf-8")

# 근무역 버튼은 한 줄에 들어가는 짧은 명칭과 고정 순서를 유지한다.
station_buttons = '''<div class="station-grid" id="stationButtons" aria-label="근무역 선택">
        <button type="button" data-station="suncheon" aria-pressed="true">순천</button>
        <button type="button" data-station="gokseong" aria-pressed="false">곡성</button>
        <button type="button" data-station="gurye" aria-pressed="false">구례구</button>
        <button type="button" data-station="beolgyo" aria-pressed="false">벌교</button>
        <button type="button" data-station="boseong" aria-pressed="false">보성</button>
      </div>'''
index, station_count = re.subn(
    r'<div class="station-grid" id="stationButtons" aria-label="근무역 선택">.*?</div>',
    station_buttons,
    index,
    count=1,
    flags=re.S,
)
if station_count != 1:
    raise SystemExit("index.html의 근무역 버튼 영역을 찾지 못했습니다.")

# 정시 예보 기준 근무시간과 최신 정적 파일 버전을 유지한다.
index = index.replace("18:10~익일 09:00", "18:00~익일 08:00")
index = re.sub(r'href="styles\.css(?:\?v=[^"]+)?"', 'href="styles.css?v=20260805-0900"', index, count=1)
index = re.sub(r'href="refresh\.css(?:\?v=[^"]+)?"', 'href="refresh.css?v=20260805-0905"', index, count=1)
index = re.sub(r'src="app\.js(?:\?v=[^"]+)?"', 'src="app.js?v=20260805-0900"', index, count=1)

# 공통 안전정보는 오늘 컨디션 확인만 기본 펼침으로 시작한다.
index = index.replace('<details class="info-block" open>', '<details class="info-block">')
index, open_count = re.subn(
    r'<details class="info-block">\s*<summary>오늘 컨디션 확인</summary>',
    '<details class="info-block" open>\n          <summary>오늘 컨디션 확인</summary>',
    index,
    count=1,
)
if open_count != 1:
    raise SystemExit("오늘 컨디션 확인 아코디언을 찾지 못했습니다.")

# 미선택 상태에서는 결과 상자를 숨긴다. 반복 실행해도 동일한 결과가 되도록 처리한다.
index, result_count = re.subn(
    r'<div class="condition-result" id="conditionResult" aria-live="polite"(?: hidden)?>.*?</div>',
    '<div class="condition-result" id="conditionResult" aria-live="polite" hidden></div>',
    index,
    count=1,
    flags=re.S,
)
if result_count != 1:
    raise SystemExit("컨디션 확인 결과 영역을 찾지 못했습니다.")

required_markers = {
    "index.html": (
        'data-station="suncheon"',
        'data-station="boseong"',
        '18:00~익일 08:00',
        'styles.css?v=20260805-0900',
        'refresh.css?v=20260805-0905',
        'app.js?v=20260805-0900',
        '<details class="info-block" open>',
        'id="conditionResult" aria-live="polite" hidden',
    ),
    "app.js": (
        'start.setHours(18, 0, 0, 0)',
        'end.setHours(8, 0, 0, 0)',
        'return "24시"',
        'data-peak="${peak}"',
        'target.hidden = true',
        '// accordion-single-open:start',
    ),
    "styles.css": (
        '/* precision-density-patch:start */',
        'background: color-mix(in srgb, var(--item-risk) 14%, #fff)',
        '.forecast-item[data-peak="true"]',
        '.condition-result[hidden]',
        '.info-block:nth-child(4)[open]',
        '/* precision-density-patch:end */',
    ),
    "refresh.css": (
        '@import url("typography-fix.css?v=20260805-0905")',
        '.hero__refresh',
    ),
    "typography-fix.css": (
        'word-break: keep-all',
        'line-break: strict',
        '.support-panel li',
        '.details-content li',
    ),
}

sources = {
    "index.html": index,
    "app.js": app,
    "styles.css": styles,
    "refresh.css": refresh,
    "typography-fix.css": typography,
}

for filename, markers in required_markers.items():
    source = sources[filename]
    missing = [marker for marker in markers if marker not in source]
    if missing:
        raise SystemExit(f"{filename} UI 구조 검증 실패: " + ", ".join(missing))

index_path.write_text(index, encoding="utf-8")
print("최신 모바일 UI 구조와 한글 줄바꿈, 기상 갱신 호환성을 확인했습니다.")
