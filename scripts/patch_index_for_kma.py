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

# 근무역 버튼은 모바일 한 줄에 들어가는 짧은 명칭과 업무 순서로 유지한다.
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

# 시간별 예보는 정시 단위이므로 야간 표시는 18:00~익일 08:00으로 맞춘다.
index = index.replace("18:10~익일 09:00", "18:00~익일 08:00")

# 새 자바스크립트와 스타일을 브라우저 캐시가 아닌 최신 파일로 강제 로드한다.
index = re.sub(r'href="styles\.css(?:\?v=[^"]+)?"', 'href="styles.css?v=20260805-0750"', index, count=1)
index = re.sub(r'src="app\.js(?:\?v=[^"]+)?"', 'src="app.js?v=20260805-0750"', index, count=1)

# 주간은 09~18시, 야간은 당일 18시부터 익일 08시까지 하나의 연속 구간으로 표시한다.
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

required_markers = {
    "index.html": (
        'data-station="suncheon"',
        'data-station="gurye"',
        '18:00~익일 08:00',
        'styles.css?v=20260805-0750',
        'app.js?v=20260805-0750',
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
print("야간근무 예보와 정적 파일 캐시 무효화를 반영했습니다.")
