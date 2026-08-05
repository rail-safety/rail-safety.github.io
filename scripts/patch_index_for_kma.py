#!/usr/bin/env python3
"""기상 갱신 전 최신 모바일 UI와 PWA 기능이 유지되는지 검증한다."""

from pathlib import Path
import re

index_path = Path("index.html")
app_path = Path("app.js")
styles_path = Path("styles.css")
refresh_path = Path("refresh.css")
typography_path = Path("typography-fix.css")
pwa_style_path = Path("pwa.css")
pwa_script_path = Path("pwa.js")
manifest_path = Path("manifest.webmanifest")
service_worker_path = Path("service-worker.js")

index = index_path.read_text(encoding="utf-8")
app = app_path.read_text(encoding="utf-8")
styles = styles_path.read_text(encoding="utf-8")
refresh = refresh_path.read_text(encoding="utf-8")
typography = typography_path.read_text(encoding="utf-8")
pwa_style = pwa_style_path.read_text(encoding="utf-8")
pwa_script = pwa_script_path.read_text(encoding="utf-8")
manifest = manifest_path.read_text(encoding="utf-8")
service_worker = service_worker_path.read_text(encoding="utf-8")

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
index = re.sub(r'href="refresh\.css(?:\?v=[^"]+)?"', 'href="refresh.css?v=20260805-0910"', index, count=1)
index = re.sub(r'src="app\.js(?:\?v=[^"]+)?"', 'src="app.js?v=20260805-0900"', index, count=1)
index = re.sub(r'src="refresh\.js(?:\?v=[^"]+)?"', 'src="refresh.js?v=20260805-0850"', index, count=1)

# 홈 화면 설치용 메타데이터와 아이콘을 유지한다.
index = re.sub(r'<meta name="theme-color" content="[^"]+"\s*/>', '<meta name="theme-color" content="#073b66" />', index, count=1)
pwa_head = '''  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="default" />
  <meta name="apple-mobile-web-app-title" content="폭염 안전 가이드" />
  <link rel="manifest" href="manifest.webmanifest?v=20260805-0950" />
  <link rel="icon" href="app-icon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="apple-touch-icon.png" />'''
if 'rel="manifest"' not in index:
    index = index.replace('  <title>순천관리역 폭염 안전 가이드</title>', '  <title>순천관리역 폭염 안전 가이드</title>\n' + pwa_head, 1)
else:
    index = re.sub(r'href="manifest\.webmanifest(?:\?v=[^"]+)?"', 'href="manifest.webmanifest?v=20260805-0950"', index, count=1)
    if 'apple-mobile-web-app-capable' not in index:
        index = index.replace('  <title>순천관리역 폭염 안전 가이드</title>', '  <title>순천관리역 폭염 안전 가이드</title>\n' + pwa_head, 1)

# 공유·홈 화면 추가 UI와 중간톤 위험단계 스타일을 연결한다.
if 'href="pwa.css' not in index:
    index = re.sub(
        r'(  <link rel="stylesheet" href="refresh\.css\?v=[^"]+"\s*/>)',
        r'\1\n  <link rel="stylesheet" href="pwa.css?v=20260805-1125" />',
        index,
        count=1,
    )
else:
    index = re.sub(r'href="pwa\.css(?:\?v=[^"]+)?"', 'href="pwa.css?v=20260805-1125"', index, count=1)

if 'src="pwa.js' not in index:
    index = re.sub(
        r'(  <script src="refresh\.js\?v=[^"]+"></script>)',
        r'\1\n  <script src="pwa.js?v=20260805-1125"></script>',
        index,
        count=1,
    )
else:
    index = re.sub(r'src="pwa\.js(?:\?v=[^"]+)?"', 'src="pwa.js?v=20260805-1125"', index, count=1)

# 주요 섹션 제목은 한 문장으로 정리하고 동일한 제목 위계를 사용한다.
index, contacts_count = re.subn(
    r'<p class="section-kicker">순천관리역 비상연락망</p>\s*<h2 id="contacts-title">원터치 연락</h2>',
    '<h2 id="contacts-title">비상연락망</h2>',
    index,
    count=1,
)
if contacts_count == 0 and '<h2 id="contacts-title">비상연락망</h2>' not in index:
    raise SystemExit("비상연락망 제목을 찾지 못했습니다.")

index, standards_count = re.subn(
    r'<p class="section-kicker">2026 공식 기준</p>\s*<h2 id="standards-title">단계별 기준</h2>',
    '<h2 id="standards-title">2026년 폭염 단계별 기준</h2>',
    index,
    count=1,
)
if standards_count == 0 and '<h2 id="standards-title">2026년 폭염 단계별 기준</h2>' not in index:
    raise SystemExit("폭염 단계별 기준 제목을 찾지 못했습니다.")

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
        'refresh.css?v=20260805-0910',
        'pwa.css?v=20260805-1125',
        'app.js?v=20260805-0900',
        'refresh.js?v=20260805-0850',
        'pwa.js?v=20260805-1125',
        'manifest.webmanifest?v=20260805-0950',
        'apple-touch-icon.png',
        '<h2 id="forecast-title">오늘의 체감온도</h2>',
        '<h2 id="action-title">현장 업무 지침</h2>',
        '<h2 id="health-title">공통 안전정보</h2>',
        '<h2 id="contacts-title">비상연락망</h2>',
        '<h2 id="standards-title">2026년 폭염 단계별 기준</h2>',
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
        '.forecast-item[data-peak="true"]',
        '.condition-result[hidden]',
        '.info-block:nth-child(4)[open]',
        '/* precision-density-patch:end */',
    ),
    "refresh.css": (
        '@import url("typography-fix.css?v=20260805-0910")',
        '.hero__refresh',
    ),
    "typography-fix.css": (
        'word-break: keep-all',
        'line-break: strict',
        '.support-panel li',
        '.details-content li',
        '#forecast-title',
        '#contacts-title',
        '#standards-title',
    ),
    "pwa.css": (
        '.page-quick-actions',
        '#dec787',
        '#d89b72',
        '#c97973',
        '#c17b86',
        '.install-dialog',
    ),
    "pwa.js": (
        'navigator.share',
        'beforeinstallprompt',
        'serviceWorker.register',
        'dataRiskLevel',
        'panel: "#e8d9b2"',
        'lockHeroToAutomaticWeather',
    ),
    "manifest.webmanifest": (
        '"display": "standalone"',
        '"/icon-192.png"',
        '"/icon-512.png"',
    ),
    "service-worker.js": (
        'weather.json',
        'cache: "no-store"',
    ),
}

sources = {
    "index.html": index,
    "app.js": app,
    "styles.css": styles,
    "refresh.css": refresh,
    "typography-fix.css": typography,
    "pwa.css": pwa_style,
    "pwa.js": pwa_script,
    "manifest.webmanifest": manifest,
    "service-worker.js": service_worker,
}

for filename, markers in required_markers.items():
    source = sources[filename]
    missing = [marker for marker in markers if marker not in source]
    if missing:
        raise SystemExit(f"{filename} UI 구조 검증 실패: " + ", ".join(missing))

for icon_path in ("icon-192.png", "icon-512.png", "apple-touch-icon.png", "app-icon.svg"):
    if not Path(icon_path).exists():
        raise SystemExit(f"홈 화면 아이콘 누락: {icon_path}")

index_path.write_text(index, encoding="utf-8")
print("중간톤 위험단계 팔레트와 공유·설치 기능, 기존 모바일 UI를 확인했습니다.")
