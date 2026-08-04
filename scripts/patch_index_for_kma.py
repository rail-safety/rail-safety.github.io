#!/usr/bin/env python3
"""기상 갱신 전 화면 구조를 검증하고 소규모 UI 패치를 일관되게 유지한다."""

from pathlib import Path
import re

index_path = Path("index.html")
app_path = Path("app.js")
styles_path = Path("styles.css")

index = index_path.read_text(encoding="utf-8")
app = app_path.read_text(encoding="utf-8")
styles = styles_path.read_text(encoding="utf-8")

# 근무역 버튼을 모바일 한 줄에 들어가는 짧은 명칭과 업무 순서로 고정한다.
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

# 하나의 근무조만 선택해 시간순으로 표시한다. 근무 중이면 남은 시간만, 근무 전이면 해당 근무 전체를 표시한다.
shift_functions = '''function getShiftWindow(now = new Date()) {
  const start = new Date(now);
  const end = new Date(now);

  if (state.shift === "day") {
    start.setHours(9, 0, 0, 0);
    end.setHours(18, 40, 0, 0);
    if (now > end) {
      start.setDate(start.getDate() + 1);
      end.setDate(end.getDate() + 1);
    }
  } else {
    const minutes = now.getHours() * 60 + now.getMinutes();
    const nightEnd = 9 * 60;
    const nightStart = 18 * 60 + 10;

    if (minutes <= nightEnd) {
      start.setDate(start.getDate() - 1);
      start.setHours(18, 10, 0, 0);
      end.setHours(9, 0, 0, 0);
    } else {
      start.setHours(18, 10, 0, 0);
      end.setDate(end.getDate() + 1);
      end.setHours(9, 0, 0, 0);
      if (minutes > nightStart) {
        start.setHours(18, 10, 0, 0);
      }
    }
  }

  return { start, end };
}

function getForecastRows() {
  const now = new Date();
  const { start, end } = getShiftWindow(now);
  const lowerBound = now >= start && now <= end
    ? new Date(now.getTime() - 60 * 60 * 1000)
    : start;

  return state.hourly
    .filter((item) => {
      const date = new Date(item.time);
      return date >= lowerBound && date <= end;
    })
    .sort((a, b) => new Date(a.time) - new Date(b.time));
}

function formatForecastHour(date, firstDate) {
  const isNextDay = firstDate && date.toDateString() !== firstDate.toDateString();
  const hour = date.getHours();
  const period = hour < 12 ? "오전" : "오후";
  const displayHour = hour % 12 || 12;
  return `${isNextDay ? "익일 " : ""}${period} ${displayHour}시`;
}

function getHotWindow'''
app, shift_count = re.subn(
    r'function isInShift\(date\) \{.*?\n\}\n\nfunction getForecastRows\(\) \{.*?\n\}\n\nfunction getHotWindow',
    shift_functions,
    app,
    count=1,
    flags=re.S,
)
if shift_count != 1:
    raise SystemExit("app.js의 근무시간 필터 함수를 찾지 못했습니다.")

# 시간별 전망을 시간-단계-온도 순서의 세로 행 목록으로 변경한다.
forecast_markup = '''  const now = new Date();
  const firstDate = new Date(rows[0].time);
  forecast.innerHTML = rows.map((item) => {
    const date = new Date(item.time);
    const level = getLevel(item.hi);
    const current = date.getHours() === now.getHours() && date.toDateString() === now.toDateString();
    const timeLabel = formatForecastHour(date, firstDate);
    return `<article class="forecast-item" data-current="${current}" style="--item-risk:${level.color};--item-risk-dark:${level.dark};--item-risk-soft:${level.soft}" aria-label="${timeLabel}, 체감온도 ${item.hi.toFixed(1)}도, ${level.name}">
      <time class="forecast-time" datetime="${item.time}">${timeLabel}</time>
      <div class="forecast-track"><span class="forecast-level">${level.name}</span></div>
      <div class="forecast-temp">${item.hi.toFixed(1)}℃</div>
    </article>`;
  }).join("");'''
app, markup_count = re.subn(
    r'  const now = new Date\(\);\n  forecast\.innerHTML = rows\.map\(\(item\) => \{.*?\n  \}\)\.join\(""\);',
    forecast_markup,
    app,
    count=1,
    flags=re.S,
)
if markup_count != 1:
    raise SystemExit("app.js의 시간별 예보 마크업을 찾지 못했습니다.")

# 이전 패치 블록이 있으면 교체하고, 없으면 파일 끝에 추가한다.
forecast_css = '''/* hourly-list-patch:start */
.station-grid {
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 6px;
}
.station-grid button {
  min-height: 46px;
  padding-inline: 2px;
  font-size: clamp(14px, 4vw, 16px);
  white-space: nowrap;
}
.forecast-grid {
  display: block;
  border-top: 1px solid var(--line);
}
.forecast-item {
  display: grid;
  grid-template-columns: minmax(82px, 104px) minmax(0, 1fr) auto;
  align-items: center;
  gap: 12px;
  min-height: 58px;
  padding: 9px 2px;
  border-bottom: 1px solid var(--line);
  border-radius: 0;
  background: transparent;
  text-align: left;
}
.forecast-item[data-current="true"] {
  background: var(--brand-050);
  box-shadow: none;
}
.forecast-time {
  color: var(--text-strong);
  font-size: 16px;
  font-weight: 620;
  white-space: nowrap;
}
.forecast-track {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}
.forecast-track::after {
  content: "";
  flex: 1 1 auto;
  min-width: 12px;
  height: 1px;
  background: var(--line);
}
.forecast-level {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  color: var(--item-risk-dark);
  font-size: 14px;
  font-weight: 680;
  white-space: nowrap;
}
.forecast-level::before {
  width: 9px;
  height: 9px;
  background: var(--item-risk);
}
.forecast-temp {
  min-width: 72px;
  margin: 0;
  padding: 7px 10px;
  border-radius: 999px;
  background: var(--item-risk-soft);
  color: var(--item-risk-dark);
  font-size: 18px;
  font-weight: 720;
  text-align: center;
}
@media (max-width: 380px) {
  .station-section { padding-inline: 14px; }
  .station-grid { gap: 4px; }
  .station-grid button { font-size: 14px; }
  .forecast-item { grid-template-columns: 78px minmax(0, 1fr) auto; gap: 8px; }
  .forecast-level { font-size: 13px; }
  .forecast-temp { min-width: 66px; padding-inline: 8px; font-size: 17px; }
}
/* hourly-list-patch:end */'''
styles = re.sub(
    r'/\* hourly-list-patch:start \*/.*?/\* hourly-list-patch:end \*/',
    forecast_css,
    styles,
    count=1,
    flags=re.S,
)
if "/* hourly-list-patch:start */" not in styles:
    styles = styles.rstrip() + "\n\n" + forecast_css + "\n"

required_markers = {
    "index.html": ('data-station="suncheon"', 'data-station="gurye"', 'id="forecast"'),
    "app.js": ("function getShiftWindow", "function formatForecastHour", 'class="forecast-track"'),
    "styles.css": ("/* hourly-list-patch:start */", ".forecast-track", "repeat(5"),
}
for filename, markers in required_markers.items():
    source = {"index.html": index, "app.js": app, "styles.css": styles}[filename]
    missing = [marker for marker in markers if marker not in source]
    if missing:
        raise SystemExit(f"{filename} 패치 검증 실패: " + ", ".join(missing))

index_path.write_text(index, encoding="utf-8")
app_path.write_text(app, encoding="utf-8")
styles_path.write_text(styles, encoding="utf-8")
print("근무역 한 줄 버튼과 시간순 시간별 전망 목록을 반영했습니다.")
