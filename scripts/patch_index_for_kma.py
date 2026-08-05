#!/usr/bin/env python3
"""기상 갱신 전 공식 체감온도 구간과 모바일 UI 구조를 유지한다."""

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

levels_block = '''const levels = [
  { min: 38, key: "danger", name: "위험 수준", color: "#662633", dark: "#401820", soft: "#c17b86", symbol: "!", rank: 4 },
  { min: 35, key: "warning", name: "경고 수준", color: "#a65332", dark: "#66321e", soft: "#d89b72", symbol: "!", rank: 3 },
  { min: 33, key: "caution", name: "주의 수준", color: "#956b24", dark: "#5e4216", soft: "#dec787", symbol: "!", rank: 2 },
  { min: 31, key: "interest", name: "관심 수준", color: "#4f6f5e", dark: "#30483b", soft: "#cbd8d0", symbol: "!", rank: 1 },
  { min: -99, key: "normal", name: "관심 미만", color: "#587080", dark: "#344955", soft: "#d5dfe4", symbol: "✓", rank: 0 }
];'''
app, level_count = re.subn(r'const levels = \[.*?\n\];', levels_block, app, count=1, flags=re.S)
if level_count != 1:
    raise SystemExit("app.js의 체감온도 단계 배열을 찾지 못했습니다.")

guides_block = '''const guides = {
  normal: {
    summary: "기본 예방수칙을 준비하고 체감온도 변화를 확인하세요.",
    yard: ["작업 전 물·온열질환 예방용품 준비", "불필요한 옥외 대기와 이동 최소화", "작업 후 실내 또는 그늘에서 몸 상태 확인"],
    platform: ["안내 전 물·온열질환 예방용품 준비", "승강장 대기 시 차양·그늘 우선 이용", "안내 사이 실내 복귀 및 몸 상태 확인"]
  },
  interest: {
    summary: "폭염안전 5대 기본수칙을 적용하고 적절한 냉방휴식을 확보하세요.",
    yard: ["시원한 물과 냉방·그늘 휴식공간 확보", "폭염 집중 시간대 작업 최소화 및 작업시간 조정 검토", "냉각조끼·넥쿨러 등 개인 보냉장구 준비", "작업 전후 본인과 동료의 온열질환 증상 확인"],
    platform: ["시원한 물과 실내·그늘 휴식공간 확보", "안내 전 대기시간과 안내 후 승강장 체류 최소화", "냉각조끼·넥쿨러 등 개인 보냉장구 준비", "연속 안내 시 교대 또는 적절한 냉방휴식 확보"]
  },
  caution: {
    summary: "매 2시간 이내 20분 이상 휴식하고 작업시간을 조정하세요.",
    yard: ["매 2시간 이내 20분 이상 냉방·그늘 휴식", "작업시간대 조정 또는 옥외작업 단축", "온열질환 민감군·고강도 작업자는 휴식 추가", "2인 이상 상호 말투·걸음·반응 확인"],
    platform: ["매 2시간 이내 20분 이상 냉방·그늘 휴식", "승강장 안내시간 단축 및 실내 복귀 동선 확보", "연속 안내 전 교대자와 휴식시간 지정", "온열질환 민감군·고강도 업무 담당자는 휴식 추가"]
  },
  warning: {
    summary: "매시간 15분 휴식하고 무더위 시간대 옥외작업을 조정·중지하세요.",
    yard: ["매시간 15분씩 냉방·그늘 휴식", "무더위 시간대에는 불가피한 경우 외 옥외작업 중지", "불가피한 작업은 최소 인원·최단시간 수행하고 휴식 충분히 부여", "담당자를 지정해 작업자의 건강상태 확인"],
    platform: ["매시간 15분씩 냉방·그늘 휴식", "무더위 시간대 안내 인원·시간 조정 및 옥외 대기 제거", "연속 안내를 피하고 교대자·실내 복귀시간 지정", "담당자가 안내 직원과 인턴사원의 건강상태 확인"]
  },
  danger: {
    summary: "재난·안전관리에 필요한 긴급조치 외 옥외작업을 중지하세요.",
    yard: ["재난·안전관리에 필요한 긴급조치 외 옥외작업 중지", "긴급작업도 최소 인원·최단시간 수행하고 휴식 충분히 부여", "온열질환 민감군의 옥외작업 제한", "보냉장구·연락수단 확보 및 담당자의 건강상태 지속 확인", "말투·걸음·의식 이상 시 즉시 작업 중지 및 119 신고"],
    platform: ["재난·안전관리에 필요한 긴급 안내 외 옥외업무 최소화", "긴급 안내 시 교대 운영하고 냉방휴식 충분히 부여", "온열질환 민감군의 장시간 승강장 업무 제한", "담당자가 직원·인턴사원의 건강상태 지속 확인", "말투·걸음·의식 이상 시 즉시 교대·냉각 및 119 신고"]
  }
};'''
app, guide_count = re.subn(
    r'const guides = \{.*?\n\};\n\nconst forecastAdvice',
    guides_block + '\n\nconst forecastAdvice',
    app,
    count=1,
    flags=re.S,
)
if guide_count != 1:
    raise SystemExit("app.js의 현장 지침 영역을 찾지 못했습니다.")

forecast_block = '''const forecastAdvice = {
  normal: "기본 예방수칙을 준비하고 이후 체감온도 변화를 확인하세요.",
  interest: "물·냉방휴식 장소·보냉장구를 준비하고 폭염 집중 시간대 노출을 줄이세요.",
  caution: "매 2시간 이내 20분 이상 휴식하고 작업시간 조정·교대계획을 확인하세요.",
  warning: "매시간 15분 휴식하고 무더위 시간대 옥외작업 조정·중지를 준비하세요.",
  danger: "긴급조치 외 옥외작업을 중지하고 보냉·교대·응급연락체계를 확인하세요."
};'''
app, forecast_count = re.subn(r'const forecastAdvice = \{.*?\n\};', forecast_block, app, count=1, flags=re.S)
if forecast_count != 1:
    raise SystemExit("app.js의 전망 안내문 영역을 찾지 못했습니다.")

hero_block = '''function renderHero() {
  const value = state.autoValue;
  const temp = state.autoTemp;
  const humidity = state.autoRh;
  const observed = state.autoObserved;

  $("#heroLocation").textContent = `${stationData[state.station].name} 인근 자동값`;
  $("#heroSource").textContent = "기상청 실황";

  if (value === null) {
    $("#currentTemp").innerHTML = '--<span>℃</span>';
    $("#currentBadge").innerHTML = '<span class="hero__level-icon" aria-hidden="true">·</span><strong>확인 중</strong>';
    $("#currentAction").textContent = "기상정보를 확인하고 있습니다.";
    $("#heroTemp").textContent = "기온 --℃";
    $("#heroHumidity").textContent = "습도 --%";
    $("#heroObserved").textContent = "관측시각 확인 중";
    $("#updated").textContent = "최근 갱신정보 확인 중";
    return;
  }

  const level = getLevel(value);
  $(".hero").style.setProperty("--hero-risk", level.color);
  $("#currentTemp").innerHTML = `${value.toFixed(1)}<span>℃</span>`;
  $("#currentBadge").innerHTML = `<span class="hero__level-icon" aria-hidden="true">${level.symbol}</span><strong>${level.name}</strong>`;
  $("#currentAction").textContent = guides[level.key].summary;
  $("#heroTemp").textContent = `기온 ${Number.isFinite(temp) ? temp.toFixed(1) : "--"}℃`;
  $("#heroHumidity").textContent = `습도 ${Number.isFinite(humidity) ? Math.round(humidity) : "--"}%`;
  $("#heroObserved").textContent = `${formatTime(observed)} 관측`;
  $("#updated").textContent = `${formatTime(state.generatedAt, true)} 기상자료 갱신`;
}'''
app, hero_count = re.subn(r'function renderHero\(\) \{.*?\n\}\n\nasync function loadWeather', hero_block + '\n\nasync function loadWeather', app, count=1, flags=re.S)
if hero_count != 1:
    raise SystemExit("app.js의 상단 자동값 카드 렌더링 함수를 찾지 못했습니다.")

official_note = "시간별 체감온도 수치가 어느 구간에 해당하는지 보여주는 참고 표시입니다. 기상청 공식 폭염 영향예보는 일 최고 체감온도·지속일수·분야별 영향을 종합해 별도로 발표합니다. 실제 작업 판단은 현장 측정값과 회사 지침을 우선합니다."
app = re.sub(r'\$\("#weatherMeta"\)\.textContent = `[^`]+`;', f'$("#weatherMeta").textContent = "{official_note}";', app, count=1)

# 최신 정적 파일 버전과 공식 단계 안내를 index.html에 유지한다.
index = re.sub(r'href="pwa\.css(?:\?v=[^"]+)?"', 'href="pwa.css?v=20260805-1305"', index, count=1)
index = re.sub(r'src="pwa\.js(?:\?v=[^"]+)?"', 'src="pwa.js?v=20260805-1305"', index, count=1)
index = re.sub(r'src="app\.js(?:\?v=[^"]+)?"', 'src="app.js?v=20260805-1305"', index, count=1)
index = index.replace('<h2 id="standards-title">2026년 폭염 단계별 기준</h2>', '<h2 id="standards-title">2026년 체감온도 구간별 대응 기준</h2>')

standards_html = '''<div class="standards-list">
          <div class="standard-row standard-row--interest"><strong>31℃</strong><span><b>관심 수준</b> · 폭염안전 5대 기본수칙 및 적절한 휴식</span></div>
          <div class="standard-row standard-row--caution"><strong>33℃</strong><span><b>주의 수준</b> · 매 2시간 이내 20분 이상 휴식, 작업시간 조정·옥외작업 단축</span></div>
          <div class="standard-row standard-row--warning"><strong>35℃</strong><span><b>경고 수준</b> · 매시간 15분 휴식, 무더위 시간대 불가피한 경우 외 옥외작업 중지</span></div>
          <div class="standard-row standard-row--danger"><strong>38℃</strong><span><b>위험 수준</b> · 재난·안전관리 긴급조치 외 옥외작업 중지</span></div>
        </div>'''
index, standards_count = re.subn(r'<div class="standards-list">.*?</div>\s*<p class="standards-note">', standards_html + '\n        <p class="standards-note">', index, count=1, flags=re.S)
if standards_count != 1:
    raise SystemExit("index.html의 체감온도 기준표를 찾지 못했습니다.")

standards_note = "위 단계명은 시간별 체감온도 수치의 구간 표시입니다. 기상청 공식 영향예보 단계는 일 최고 체감온도와 지속일수, 분야별 영향을 종합해 발표합니다. 작업장에서는 현장 체감온도와 고용노동부·안전보건공단 대응지침, 회사 폭염 대응계획을 함께 적용합니다."
index = re.sub(r'<p class="standards-note">.*?</p>', f'<p class="standards-note">{standards_note}</p>', index, count=1, flags=re.S)

required = {
    "index.html": ("pwa.css?v=20260805-1305", "app.js?v=20260805-1305", "pwa.js?v=20260805-1305", "관심 수준", "주의 수준", "경고 수준", "위험 수준"),
    "app.js": ('key: "interest"', 'name: "관심 수준"', 'name: "위험 수준"', "매 2시간 이내 20분 이상", "매시간 15분", "긴급조치 외 옥외작업 중지"),
    "pwa.css": ('[data-risk-level="interest"]', '.standard-row--interest', '.standard-row--danger'),
    "pwa.js": ("dataRiskLevel", "const palette", "applyRiskTheme", "initQuickActions"),
    "refresh.css": ('.hero__refresh',),
    "typography-fix.css": ('word-break: keep-all',),
    "manifest.webmanifest": ('"display": "standalone"',),
    "service-worker.js": ('weather.json', 'cache: "no-store"'),
}

sources = {
    "index.html": index,
    "app.js": app,
    "pwa.css": pwa_style,
    "pwa.js": pwa_script,
    "refresh.css": refresh,
    "typography-fix.css": typography,
    "manifest.webmanifest": manifest,
    "service-worker.js": service_worker,
}
for filename, markers in required.items():
    missing = [marker for marker in markers if marker not in sources[filename]]
    if missing:
        raise SystemExit(f"{filename} 공식 기준 검증 실패: " + ", ".join(missing))

if "매우 위험" in app or "매우 위험" in pwa_script:
    raise SystemExit("비공식 단계명 '매우 위험'이 남아 있습니다.")

for icon_path in ("icon-192.png", "icon-512.png", "apple-touch-icon.png", "app-icon.svg"):
    if not Path(icon_path).exists():
        raise SystemExit(f"홈 화면 아이콘 누락: {icon_path}")

index_path.write_text(index, encoding="utf-8")
app_path.write_text(app, encoding="utf-8")
print("관심·주의·경고·위험 구간과 작업장 대응지침을 확인했습니다.")
