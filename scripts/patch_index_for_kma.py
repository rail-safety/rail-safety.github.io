#!/usr/bin/env python3
"""기상 갱신 전 화면 구조와 현장용 표시 밀도를 일관되게 유지한다."""

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
index = re.sub(r'href="styles\.css(?:\?v=[^"]+)?"', 'href="styles.css?v=20260805-0845"', index, count=1)
index = re.sub(r'src="app\.js(?:\?v=[^"]+)?"', 'src="app.js?v=20260805-0845"', index, count=1)

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

semantic_patch = r'''/* semantic-color-patch:start */
/* 시간별 전망: 한 시간당 한 행, 행 전체 단계색, 온도 pill 제거 */
.forecast-grid {
  display: grid !important;
  grid-template-columns: 1fr !important;
  gap: 4px;
  border-top: 0;
}
.forecast-item {
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr) 64px;
  align-items: center;
  gap: 8px;
  width: 100%;
  min-height: 40px;
  padding: 5px 10px;
  border: 0;
  border-radius: 9px;
  background: var(--item-risk-soft);
  text-align: left;
}
.forecast-item[data-current="true"] {
  background: color-mix(in srgb, var(--item-risk-soft) 82%, var(--brand-100));
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--item-risk) 35%, transparent);
}
.forecast-time {
  color: var(--text-strong);
  font-size: 14px;
  font-weight: 680;
  white-space: nowrap;
}
.forecast-track {
  display: flex;
  align-items: center;
  gap: 7px;
  min-width: 0;
}
.forecast-track::after {
  content: "";
  flex: 1 1 auto;
  min-width: 12px;
  height: 1px;
  background: color-mix(in srgb, var(--item-risk) 22%, var(--line));
}
.forecast-level {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  margin: 0;
  color: var(--text);
  font-size: 12px;
  font-weight: 650;
  white-space: nowrap;
}
.forecast-level::before {
  content: "";
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--item-risk);
}
.forecast-temp {
  min-width: 0;
  margin: 0;
  padding: 0;
  border-radius: 0;
  background: transparent;
  color: var(--text-strong);
  font-size: 15px;
  font-weight: 720;
  text-align: right;
  font-variant-numeric: tabular-nums;
}

/* 공통 안전정보: 중립 리스트, 위험정보만 강조 */
.info-list {
  display: block;
  margin-top: 14px;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}
.info-block {
  border-top: 1px solid var(--line);
  border-radius: 0;
  overflow: visible;
  background: #fff;
}
.info-block:first-child { border-top: 0; }
.info-block summary {
  min-height: 56px;
  padding: 12px 44px 12px 2px;
  color: var(--text-strong);
  background: transparent;
}
.info-block summary::before {
  content: "";
  flex: 0 0 auto;
  width: 8px;
  height: 8px;
  margin-right: 10px;
  border-radius: 50%;
  background: var(--brand-800);
}
.info-block:nth-child(2) summary::before { background: #27766f; }
.info-block:nth-child(3) summary::before { background: #a56512; }
.info-block:nth-child(4) summary::before { background: #b52a2a; }
.info-block summary::after {
  right: 4px;
  color: var(--brand-800);
}
.info-block:nth-child(4) summary::after { color: #b52a2a; }
.details-content {
  padding: 0 2px 18px;
}
.info-block[open] summary {
  color: var(--text-strong);
}

/* 최상단 긴급 경고만 연한 적색으로 분명하게 구분 */
.emergency-banner {
  border-left: 0;
  border-radius: 13px;
  background: #fff0ef;
  color: #7b2020;
}

/* 응급조치 펼침 시에만 강한 위험 패널 */
.info-block:nth-child(4)[open] {
  margin: 12px 0;
  padding: 0 16px 16px;
  border: 0;
  border-radius: 18px;
  background: #962b24;
  color: #fff;
}
.info-block:nth-child(4)[open] summary {
  padding-left: 0;
  color: #fff;
}
.info-block:nth-child(4)[open] summary::before {
  background: #fff;
}
.info-block:nth-child(4)[open] summary::after {
  right: 0;
  color: #fff;
}
.info-block:nth-child(4)[open] .details-content {
  padding: 4px 0 0;
  color: #fff;
}
.info-block:nth-child(4)[open] .details-content,
.info-block:nth-child(4)[open] .details-content li,
.info-block:nth-child(4)[open] .subhead,
.info-block:nth-child(4)[open] .subhead--danger {
  color: #fff;
}
.info-block:nth-child(4)[open] .call-button {
  width: 100%;
  background: #fff;
  color: #962b24;
}

@media (max-width: 380px) {
  .forecast-item {
    grid-template-columns: 42px minmax(0, 1fr) 58px;
    gap: 6px;
    min-height: 38px;
    padding-inline: 8px;
  }
  .forecast-time { font-size: 13px; }
  .forecast-level { font-size: 11px; }
  .forecast-temp { font-size: 14px; }
}
/* semantic-color-patch:end */'''

styles = re.sub(
    r'/\* semantic-color-patch:start \*/.*?/\* semantic-color-patch:end \*/',
    '',
    styles,
    flags=re.S,
).rstrip() + "\n\n" + semantic_patch + "\n"

required_markers = {
    "index.html": (
        'data-station="suncheon"',
        '18:00~익일 08:00',
        'styles.css?v=20260805-0845',
        'app.js?v=20260805-0845',
        'id="forecast"',
    ),
    "app.js": (
        'start.setHours(18, 0, 0, 0)',
        'end.setHours(8, 0, 0, 0)',
        'return "24시"',
        'function renderForecast',
    ),
    "styles.css": (
        "/* semantic-color-patch:start */",
        "grid-template-columns: 1fr !important",
        "background: var(--item-risk-soft)",
        ".info-block:nth-child(4)[open]",
        "background: #962b24",
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
print("세로형 시간별 전망과 절제된 공통 안전정보 UI를 반영했습니다.")
