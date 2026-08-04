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
index = re.sub(r'href="styles\.css(?:\?v=[^"]+)?"', 'href="styles.css?v=20260805-0830"', index, count=1)
index = re.sub(r'src="app\.js(?:\?v=[^"]+)?"', 'src="app.js?v=20260805-0830"', index, count=1)

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

color_patch = r'''/* semantic-color-patch:start */
/* 시간별 전망은 글자색보다 행 전체의 연한 상태면으로 흐름을 전달한다. */
.forecast-grid {
  display: grid;
  gap: 3px;
  border-top: 0;
}
.forecast-item {
  border-bottom: 0;
  border-radius: 9px;
  background: var(--item-risk-soft);
}
.forecast-item[data-current="true"] {
  background: color-mix(in srgb, var(--item-risk-soft) 76%, var(--brand-100));
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--item-risk) 30%, transparent);
}
.forecast-time {
  color: var(--text-strong);
}
.forecast-level {
  color: var(--text);
}
.forecast-track::after {
  background: color-mix(in srgb, var(--item-risk) 18%, var(--line));
}
.forecast-temp {
  background: rgb(255 255 255 / 66%);
  color: var(--text-strong);
}

/* 건강정보는 목적별 의미색을 사용하되 내용보다 강하지 않게 표현한다. */
.info-list {
  display: grid;
  gap: 8px;
}
.info-block {
  border-top: 0;
  border-radius: 13px;
  overflow: clip;
  background: var(--info-soft, #f5f7f8);
}
.info-block:nth-child(1) { --info-color: var(--brand-800); --info-soft: #edf5fb; }
.info-block:nth-child(2) { --info-color: #087b78; --info-soft: #eaf7f5; }
.info-block:nth-child(3) { --info-color: #a75b00; --info-soft: #fff4e5; }
.info-block:nth-child(4) { --info-color: #b52a2a; --info-soft: #fff0f0; }
.info-block summary {
  min-height: 54px;
  padding-inline: 14px 44px;
  color: var(--text-strong);
}
.info-block summary::before {
  content: "";
  flex: 0 0 auto;
  width: 9px;
  height: 9px;
  margin-right: 10px;
  border-radius: 50%;
  background: var(--info-color);
}
.info-block summary::after {
  right: 14px;
  color: var(--info-color);
}
.details-content {
  padding: 0 14px 16px;
}
.info-block[open] summary {
  color: var(--info-color);
}
.emergency-banner {
  background: #fff0f0;
  color: #7b2020;
}
.condition-result {
  background: color-mix(in srgb, var(--condition-color) 8%, #fff);
}
/* semantic-color-patch:end */'''

styles = re.sub(
    r'/\* semantic-color-patch:start \*/.*?/\* semantic-color-patch:end \*/',
    '',
    styles,
    flags=re.S,
).rstrip() + "\n\n" + color_patch + "\n"

required_markers = {
    "index.html": (
        'data-station="suncheon"',
        '18:00~익일 08:00',
        'styles.css?v=20260805-0830',
        'app.js?v=20260805-0830',
        'id="forecast"',
    ),
    "app.js": (
        'start.setHours(18, 0, 0, 0)',
        'end.setHours(8, 0, 0, 0)',
        'return "24시"',
        'function renderForecast',
    ),
    "styles.css": (
        "/* hourly-list-patch:start */",
        "/* compact-density-patch:start */",
        "/* semantic-color-patch:start */",
        ".info-block:nth-child(4)",
        "background: var(--item-risk-soft)",
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
print("시간별 전망 상태면과 건강정보 의미색을 반영했습니다.")
