#!/usr/bin/env python3
"""기상 갱신 전 화면 구조를 검증하고 근무시간 예보 표시를 일관되게 유지한다."""

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
index = re.sub(r'href="styles\.css(?:\?v=[^"]+)?"', 'href="styles.css?v=20260805-0815"', index, count=1)
index = re.sub(r'src="app\.js(?:\?v=[^"]+)?"', 'src="app.js?v=20260805-0815"', index, count=1)

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

compact_css = '''/* compact-density-patch:start */
.hero__action {
  margin-top: 20px;
  padding-top: 16px;
}
.hero__action-label {
  margin-bottom: 2px;
  font-size: 13px;
}
.hero__action p:last-child {
  font-size: clamp(17px, 4.7vw, 19px);
  line-height: 1.42;
  font-weight: 620;
}
.hero__meta {
  margin-top: 14px;
}
.forecast-advice,
.emergency-banner,
.condition-result {
  border-left: 0;
}
.forecast-advice {
  padding: 12px 13px;
  background: rgb(255 255 255 / 72%);
}
.emergency-banner,
.condition-result {
  background: #f5f7f8;
}
.hourly-block {
  margin-top: 18px;
}
.hourly-block__title {
  margin-bottom: 6px;
}
.forecast-grid {
  border-top: 1px solid var(--line);
}
.forecast-item {
  grid-template-columns: 48px minmax(0, 1fr) auto;
  gap: 8px;
  min-height: 38px;
  padding: 3px 2px;
}
.forecast-time {
  font-size: 14px;
  font-weight: 620;
}
.forecast-track {
  gap: 7px;
}
.forecast-level {
  gap: 5px;
  font-size: 12px;
  font-weight: 650;
}
.forecast-level::before {
  width: 7px;
  height: 7px;
}
.forecast-temp {
  min-width: 60px;
  padding: 4px 8px;
  font-size: 15px;
  font-weight: 700;
}
@media (max-width: 380px) {
  .forecast-item {
    grid-template-columns: 44px minmax(0, 1fr) auto;
    gap: 6px;
    min-height: 36px;
  }
  .forecast-time { font-size: 13px; }
  .forecast-level { font-size: 11px; }
  .forecast-temp {
    min-width: 56px;
    padding-inline: 7px;
    font-size: 14px;
  }
}
/* compact-density-patch:end */'''
styles = re.sub(
    r'/\* compact-density-patch:start \*/.*?/\* compact-density-patch:end \*/',
    compact_css,
    styles,
    count=1,
    flags=re.S,
)
if "/* compact-density-patch:start */" not in styles:
    styles = styles.rstrip() + "\n\n" + compact_css + "\n"

required_markers = {
    "index.html": (
        'data-station="suncheon"',
        'data-station="gurye"',
        '18:00~익일 08:00',
        'styles.css?v=20260805-0815',
        'app.js?v=20260805-0815',
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
        ".forecast-track",
        "repeat(5",
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
print("히어로 행동문구와 시간별 전망 밀도를 개선했습니다.")
