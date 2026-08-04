#!/usr/bin/env python3
"""기상 갱신 전 화면 구조와 모바일 현장용 정보 위계를 일관되게 유지한다."""

from pathlib import Path
import re

index_path = Path("index.html")
app_path = Path("app.js")
styles_path = Path("styles.css")

index = index_path.read_text(encoding="utf-8")
app = app_path.read_text(encoding="utf-8")
styles = styles_path.read_text(encoding="utf-8")

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

index = index.replace("18:10~익일 09:00", "18:00~익일 08:00")
index = re.sub(r'href="styles\.css(?:\?v=[^"]+)?"', 'href="styles.css?v=20260805-0900"', index, count=1)
index = re.sub(r'src="app\.js(?:\?v=[^"]+)?"', 'src="app.js?v=20260805-0900"', index, count=1)

# 공통 안전정보는 첫 항목만 기본 펼침으로 시작한다.
index = index.replace('<details class="info-block" open>', '<details class="info-block">')
index, open_count = re.subn(
    r'<details class="info-block">\s*<summary>오늘 컨디션 확인</summary>',
    '<details class="info-block" open>\n          <summary>오늘 컨디션 확인</summary>',
    index,
    count=1,
)
if open_count != 1:
    raise SystemExit("오늘 컨디션 확인 아코디언을 찾지 못했습니다.")

# 아무 항목도 선택하지 않은 상태에서는 큰 결과상자를 표시하지 않는다.
index, result_count = re.subn(
    r'<div class="condition-result" id="conditionResult" aria-live="polite">.*?</div>',
    '<div class="condition-result" id="conditionResult" aria-live="polite" hidden></div>',
    index,
    count=1,
    flags=re.S,
)
if result_count != 1:
    raise SystemExit("컨디션 확인 결과 영역을 찾지 못했습니다.")

shift_functions = '''function getShiftWindow(now = new Date()) {
  const start = new Date(now);
  const end = new Date(now);

  if (state.shift === "day") {
    start.setHours(9, 0, 0, 0);
    end.setHours(18, 0, 0, 0);
    if (now > end) {
      start.setDate(start.getDate() + 1);
      end.setDate(end.getDate() + 1);
    }
  } else {
    start.setHours(18, 0, 0, 0);
    end.setDate(end.getDate() + 1);
    end.setHours(8, 0, 0, 0);
  }

  return { start, end };
}

function getForecastRows() {
  const { start, end } = getShiftWindow(new Date());

  return state.hourly
    .filter((item) => {
      const date = new Date(item.time);
      return date >= start && date <= end;
    })
    .sort((a, b) => new Date(a.time) - new Date(b.time));
}

function formatForecastHour(date) {
  const hour = date.getHours();
  if (state.shift === "night" && hour === 0) return "24시";
  return `${hour}시`;
}

function getHotWindow'''
app, shift_count = re.subn(
    r'function getShiftWindow\(now = new Date\(\)\) \{.*?\n\}\n\nfunction getForecastRows\(\) \{.*?\n\}\n\nfunction formatForecastHour\(date(?:, firstDate)?\) \{.*?\n\}\n\nfunction getHotWindow',
    shift_functions,
    app,
    count=1,
    flags=re.S,
)
if shift_count != 1:
    raise SystemExit("app.js의 근무시간 예보 함수를 찾지 못했습니다.")

app = app.replace('  const firstDate = new Date(rows[0].time);\n', '')
app = app.replace('const timeLabel = formatForecastHour(date, firstDate);', 'const timeLabel = formatForecastHour(date);')

# 최고 예상 시간은 온도 굵기와 배경 명도만 한 단계 높인다.
app = app.replace(
    '    const current = date.getHours() === now.getHours() && date.toDateString() === now.toDateString();\n    const timeLabel = formatForecastHour(date);',
    '    const current = date.getHours() === now.getHours() && date.toDateString() === now.toDateString();\n    const peak = item.time === highest.time;\n    const timeLabel = formatForecastHour(date);',
)
app = app.replace(
    'return `<article class="forecast-item" data-current="${current}" style=',
    'return `<article class="forecast-item" data-current="${current}" data-peak="${peak}" style=',
)

condition_function = '''function updateConditionCheck() {
  const selected = $$(".condition-check:checked").map((item) => item.value);
  const target = $("#conditionResult");

  if (selected.length === 0) {
    target.hidden = true;
    target.innerHTML = "";
    target.removeAttribute("data-severity");
    return;
  }

  let title = "업무 강도·더위 노출 축소";
  let body = "동료·관리자에게 상태 공유 · 악화 시 즉시 작업 중지";
  let color = "#9a6500";
  let severity = "caution";

  if (selected.includes("heat")) {
    title = "즉시 작업 중지 및 냉방장소 이동";
    body = "상태 공유 · 신속한 냉각 · 빠른 회복이 없으면 119 또는 의료기관 도움 요청";
    color = "#c72c2c";
    severity = "critical";
  } else if (selected.includes("illness")) {
    title = "옥외작업 전 관리자 확인 필요";
    body = "탈수·체온 상승 위험 증가 · 시원한 장소에서 수분 보충 · 증상 지속 시 의료기관 안내";
    color = "#c45600";
    severity = "warning";
  } else if (selected.includes("sleep") && selected.length === 1) {
    title = "수면 상태 공유 및 무리한 작업 방지";
    body = "동료·관리자에게 사전 공유 · 휴식계획 확인";
  }

  target.hidden = false;
  target.dataset.severity = severity;
  target.style.setProperty("--condition-color", color);
  target.innerHTML = `<strong>${title}</strong><p>${body}</p>`;
}'''
app, condition_count = re.subn(
    r'function updateConditionCheck\(\) \{.*?\n\}',
    condition_function,
    app,
    count=1,
    flags=re.S,
)
if condition_count != 1:
    raise SystemExit("app.js의 컨디션 확인 함수를 찾지 못했습니다.")

accordion_block = '''// 공통 안전정보는 현장에서 한 번에 하나만 펼쳐지도록 한다.
const infoBlocks = $$(".info-block");
infoBlocks.forEach((block) => block.addEventListener("toggle", () => {
  if (!block.open) return;
  infoBlocks.forEach((other) => {
    if (other !== block) other.open = false;
  });
}));
if (infoBlocks[0] && !infoBlocks.some((block) => block.open)) infoBlocks[0].open = true;

'''
app = re.sub(
    r'// accordion-single-open:start.*?// accordion-single-open:end\n\n',
    '',
    app,
    flags=re.S,
)
accordion_block = '// accordion-single-open:start\n' + accordion_block + '// accordion-single-open:end\n\n'
app = app.replace(
    '$$(".condition-check").forEach((checkbox) => checkbox.addEventListener("change", updateConditionCheck));',
    accordion_block + '$$(".condition-check").forEach((checkbox) => checkbox.addEventListener("change", updateConditionCheck));',
    1,
)

precision_patch = r'''/* precision-density-patch:start */
:root {
  --shadow-soft: 0 1px 2px rgb(18 42 60 / 4%), 0 6px 18px rgb(18 42 60 / 4%);
}
.page-header { padding: 22px 0 14px; }
.station-section { padding: 16px; }
.section-inline-heading { margin-bottom: 10px; }
.station-grid { gap: 5px; }
.station-grid button {
  min-height: 44px;
  border-radius: 12px;
  box-shadow: none;
}
.station-grid button[aria-pressed="true"] {
  box-shadow: 0 3px 9px rgb(0 79 143 / 14%);
}
.hero {
  margin-top: 16px;
  padding: 22px 20px 19px;
}
.hero__reading { margin-top: 22px; }
.hero__action { margin-top: 18px; padding-top: 14px; }
.hero__action p:last-child {
  font-size: clamp(18px, 5vw, 20px);
  line-height: 1.42;
  font-weight: 640;
}
.hero__meta { gap: 6px; margin-top: 13px; }
.hero__meta span {
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 13px;
}
.hero__updated { margin-top: 8px; font-size: 13px; }
.data-note { margin-top: 9px; font-size: 13px; }
.surface {
  margin-top: 24px;
  padding: 20px 18px;
}
.section-heading { margin-bottom: 14px; }
.section-description { margin-top: 4px; }
.segmented { gap: 4px; padding: 4px; border-radius: 14px; }
.segmented button { min-height: 44px; padding: 7px 9px; }
.segmented--soft button { min-height: 54px; }
.segmented--soft button[aria-pressed="true"] {
  background: #fff;
  color: var(--brand-900);
  box-shadow: 0 2px 6px rgb(31 54 69 / 10%);
}
.action-settings { gap: 10px; padding: 14px; border-radius: 16px; }
.action-settings .setting-group:first-child .segmented button[aria-pressed="true"] {
  background: #fff;
  color: var(--brand-900);
  box-shadow: inset 0 0 0 1px #b9d3e4;
}
.action-settings .setting-group:last-child .segmented button[aria-pressed="true"] {
  background: var(--brand-800);
  color: #fff;
  box-shadow: none;
}
.forecast-highlight { margin-top: 14px; padding: 18px; }
.forecast-facts { margin-top: 14px; padding-top: 12px; }
.forecast-facts div { margin-top: 7px; }
.forecast-advice { margin-top: 13px; padding: 11px 12px; }
.hourly-block { margin-top: 17px; }
.hourly-block__title { margin-bottom: 7px; }

/* 시간별 전망은 단계별 행 전체 색상으로 위험 흐름을 보여준다. */
.forecast-grid {
  display: grid !important;
  grid-template-columns: 1fr !important;
  gap: 3px;
}
.forecast-item {
  grid-template-columns: 48px minmax(0, 1fr) 64px;
  min-height: 39px;
  padding: 5px 10px;
  border: 0;
  border-radius: 8px;
  background: color-mix(in srgb, var(--item-risk) 14%, #fff);
}
.forecast-item[data-current="true"] {
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--item-risk) 42%, transparent);
}
.forecast-item[data-peak="true"] {
  background: color-mix(in srgb, var(--item-risk) 20%, #fff);
}
.forecast-item[data-peak="true"] .forecast-temp {
  color: var(--item-risk-dark);
  font-weight: 800;
}
.forecast-time,
.forecast-temp { color: var(--text-strong); }
.forecast-level { color: var(--item-risk-dark); }
.forecast-temp {
  min-width: 0;
  padding: 0;
  border-radius: 0;
  background: transparent;
  text-align: right;
}
.forecast-track::after {
  background: color-mix(in srgb, var(--item-risk) 26%, var(--line));
}
.guide-header { margin-top: 20px; padding-top: 18px; }
.guide-summary { margin-top: 8px; padding: 12px 13px; }
.guide-list { margin-top: 10px; }
.guide-item { gap: 10px; padding: 12px 2px; }
.guide-text { line-height: 1.48; }

/* 공통 안전정보는 흰색 기반으로 유지하고 위험도만 작은 포인트로 구분한다. */
.emergency-banner {
  padding: 13px 14px;
  border: 0;
  border-radius: 12px;
  background: #fff0ef;
}
.emergency-banner strong { font-size: 18px; }
.emergency-banner span { font-size: 15px; font-weight: 620; }
.info-list {
  display: block;
  margin-top: 12px;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}
.info-block {
  margin: 0;
  padding: 0;
  border: 0;
  border-top: 1px solid var(--line);
  border-radius: 0;
  background: #fff;
  color: var(--text);
}
.info-block:first-child { border-top: 0; }
.info-block summary {
  min-height: 50px;
  padding: 9px 40px 9px 2px;
  color: var(--text-strong);
  font-size: 18px;
  background: transparent;
}
.info-block summary::before {
  width: 8px;
  height: 8px;
  margin-right: 10px;
  background: var(--brand-800);
}
.info-block:nth-child(2) summary::before { background: var(--brand-800); }
.info-block:nth-child(3) summary::before { background: #a56512; }
.info-block:nth-child(4) summary::before { background: #b52a2a; }
.info-block summary::after { right: 2px; color: var(--brand-800); }
.info-block:nth-child(3) summary::after { color: #a56512; }
.info-block:nth-child(4) summary::after { color: #b52a2a; }
.details-content { padding: 0 2px 14px; }
.details-content ul,
.details-content ol { margin-top: 8px; }
.details-content li { margin: 6px 0; }
.check-intro { margin-bottom: 3px; font-size: 14px; }
.condition-row {
  min-height: 44px;
  gap: 10px;
  font-size: 16px;
}
.condition-row input {
  width: 18px;
  height: 18px;
}
.condition-result[hidden] { display: none; }
.condition-result {
  margin-top: 10px;
  padding: 11px 12px;
  border: 0;
  border-radius: 10px;
  background: #f2f5f7;
}
.condition-result[data-severity="warning"] { background: #fff5e8; }
.condition-result[data-severity="critical"] { background: #fff0ef; }
.condition-result strong { font-size: 16px; }
.condition-result p { font-size: 14px; }
.microcopy { margin-top: 8px; font-size: 13px; }

/* 응급조치는 펼친 경우에만 하나의 강한 위험 패널로 표시한다. */
.info-block:nth-child(4)[open] {
  margin: 10px 0;
  padding: 0 14px 14px;
  border: 0;
  border-radius: 16px;
  background: #8f2d27;
  color: #fff;
}
.info-block:nth-child(4)[open] summary {
  min-height: 52px;
  padding-left: 0;
  color: #fff;
}
.info-block:nth-child(4)[open] summary::before { background: #fff; }
.info-block:nth-child(4)[open] summary::after { right: 0; color: #fff; }
.info-block:nth-child(4)[open] .details-content,
.info-block:nth-child(4)[open] .details-content li,
.info-block:nth-child(4)[open] .subhead,
.info-block:nth-child(4)[open] .subhead--danger { color: #fff; }
.info-block:nth-child(4)[open] .details-content { padding: 0 0 2px; }
.info-block:nth-child(4)[open] .call-button {
  width: 100%;
  margin-top: 12px;
  background: #fff;
  color: #8f2d27;
}
.contact-link { min-height: 52px; padding-block: 10px; }
.utility-grid { gap: 24px; margin-top: 24px; }
.standard-row { min-height: 56px; padding-block: 9px; }
footer { padding-top: 24px; }

@media (max-width: 420px) {
  .station-section { padding: 14px; }
  .hero { padding: 20px 17px 18px; }
  .surface { padding: 18px 15px; }
  .forecast-item {
    grid-template-columns: 43px minmax(0, 1fr) 58px;
    gap: 6px;
    min-height: 38px;
    padding-inline: 8px;
  }
  .forecast-time { font-size: 13px; }
  .forecast-level { font-size: 11px; }
  .forecast-temp { font-size: 14px; }
}
/* precision-density-patch:end */'''

styles = re.sub(
    r'/\* precision-density-patch:start \*/.*?/\* precision-density-patch:end \*/',
    '',
    styles,
    flags=re.S,
).rstrip() + "\n\n" + precision_patch + "\n"

required_markers = {
    "index.html": (
        'data-station="suncheon"',
        '18:00~익일 08:00',
        'styles.css?v=20260805-0900',
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
        "/* precision-density-patch:start */",
        'background: color-mix(in srgb, var(--item-risk) 14%, #fff)',
        '.forecast-item[data-peak="true"]',
        '.condition-result[hidden]',
        '.info-block:nth-child(4)[open]',
    ),
}

for filename, markers in required_markers.items():
    source = {"index.html": index, "app.js": app, "styles.css": styles}[filename]
    missing = [marker for marker in markers if marker not in source]
    if missing:
        raise SystemExit(f"{filename} 패치 검증 실패: " + ", ".join(missing))

index_path.write_text(index, encoding="utf-8")
app_path.write_text(app, encoding="utf-8")
styles_path.write_text(styles, encoding="utf-8")
print("모바일 밀도, 시간별 위험색, 공통 안전정보 위계를 정밀 조정했습니다.")
