const stationData = {
  suncheon: { name: "순천역" },
  gokseong: { name: "곡성역" },
  gurye: { name: "구례구역" },
  beolgyo: { name: "벌교역" },
  boseong: { name: "보성역" }
};

const levels = [
  { min: 38, key: "extreme", name: "매우 위험", color: "#7f1d1d", dark: "#571313", soft: "#fcecec", symbol: "!", rank: 4 },
  { min: 35, key: "danger", name: "위험", color: "#c72c2c", dark: "#8f1e1e", soft: "#fff0f0", symbol: "!", rank: 3 },
  { min: 33, key: "warning", name: "경고", color: "#c45600", dark: "#8f3e00", soft: "#fff1e5", symbol: "!", rank: 2 },
  { min: 31, key: "caution", name: "주의", color: "#9a6500", dark: "#6f4900", soft: "#fff7df", symbol: "!", rank: 1 },
  { min: -99, key: "normal", name: "안전", color: "#17834b", dark: "#0d6538", soft: "#e9f6ef", symbol: "✓", rank: 0 }
];

const guides = {
  normal: {
    summary: "기본 예방수칙을 지키며 업무를 수행하세요.",
    yard: [
      "쿨토시, 넥쿨러 등 온열질환 예방용품 준비",
      "입환 시작 전 불필요한 옥외 대기시간 최소화",
      "작업 종료 후 실내 또는 그늘로 이동"
    ],
    platform: [
      "적절한 시간에 승강장으로 이동",
      "안내 및 대기 중 그늘 이용",
      "안내와 안내 사이 실내 복귀"
    ]
  },
  caution: {
    summary: "옥외 체류시간을 줄이고 작업 사이에 몸을 식히세요.",
    yard: [
      "작업 동선·역할 사전 확인 및 옥외 체류시간 단축",
      "작업 사이 대기 및 불필요한 이동 최소화",
      "작업 사이 실내 또는 냉방장소에서 냉각·휴식"
    ],
    platform: [
      "안내 및 대기 중 그늘 이용",
      "안내 종료 후 실내 또는 냉방장소 복귀",
      "장시간 연속 홈안내 시 교대 또는 냉방휴식 확보"
    ]
  },
  warning: {
    summary: "작업 순서와 휴식계획을 확인하고 냉방휴식을 확보하세요.",
    yard: [
      "작업 전 작업 순서·휴식계획 관리자 확인",
      "2인 이상 작업 및 상호 말투·걸음·반응 확인",
      "작업 단위 단축 및 선로 주변 대기시간 최소화",
      "작업 종료 후 즉시 냉방장소에서 냉각·휴식"
    ],
    platform: [
      "안내 위치·대기 위치·실내 복귀 동선 사전 확인",
      "안내 전 차양·그늘 대기 및 안내 종료 후 실내 복귀",
      "연속 홈안내 예정 시 교대자·냉방휴식 시간 사전 지정",
      "인턴사원 안내 구간·복귀 동선 확인 및 장시간 단독 옥외체류 방지"
    ]
  },
  danger: {
    summary: "현재 시행하려는 업무가 즉시 필요한지, 연기 가능한지 관리자와 먼저 확인하세요.",
    yard: [
      "연기 가능한 업무 조정 및 반드시 필요한 업무만 시행",
      "역할·동선 실내 사전 정리 및 옥외 체류시간 단축",
      "2인 이상 상호 상태 확인 및 최소 인원·최단시간 작업",
      "작업 종료 후 즉시 냉방장소 이동 및 충분한 냉각·휴식"
    ],
    platform: [
      "안내 동선·대기 위치·실내 복귀 경로 사전 확인",
      "안내 전 대기시간 및 안내 종료 후 홈 체류시간 최소화",
      "연속 안내 예정 시 교대자·냉방휴식 시간 사전 지정",
      "인턴사원 안내 동선·옥외 체류시간 확인 및 무리한 연속 안내 방지",
      "어지럼·메스꺼움·반응 저하 발생 시 즉시 교대"
    ]
  },
  extreme: {
    summary: "업무가 긴급하거나 반드시 필요한지 관리자와 확인하세요. 연기 가능한 업무는 시행하지 않습니다.",
    yard: [
      "반드시 필요한 업무만 최소 인원·최단시간 수행",
      "2인 이상 상호 상태 지속 확인 및 단독 행동 금지",
      "보냉장구·연락수단 준비 및 옥외 대기시간 제거",
      "말투·걸음·반응 이상 시 즉시 작업 중지",
      "작업 종료 후 즉시 냉방장소 이동"
    ],
    platform: [
      "이동·대기·복귀 동선 사전 확인 및 옥외 체류시간 최소화",
      "연속 홈안내 방지를 위한 교대자·업무 조정",
      "인턴사원 단독 장시간 안내 방지 및 담당 직원 상태 확인",
      "평소와 다른 몸 상태 발생 시 즉시 교대",
      "의식·말투·걸음 이상 시 즉시 냉방장소 이동 및 응급조치"
    ]
  }
};

const forecastAdvice = {
  normal: "물과 온열질환 예방용품을 준비하고 기본 예방수칙을 유지하세요.",
  caution: "그늘·냉방 휴식장소를 미리 확인하고 옥외 체류시간을 줄이세요.",
  warning: "휴식계획과 교대계획을 미리 확인하고 냉방휴식을 확보하세요.",
  danger: "연기 가능한 업무를 조정하고 물·휴식장소·교대계획을 미리 확인하세요.",
  extreme: "필수업무 여부를 관리자와 확인하고 보냉조치·교대·응급연락을 준비하세요."
};

const state = {
  station: "suncheon",
  shift: "day",
  source: "auto",
  appliedSource: "auto",
  job: "yard",
  autoValue: null,
  autoTemp: null,
  autoRh: null,
  autoObserved: null,
  generatedAt: null,
  fieldValue: null,
  fieldTemp: null,
  fieldRh: null,
  fieldAppliedAt: null,
  hourly: []
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

function heatIndex(t, rh) {
  if (!Number.isFinite(t) || !Number.isFinite(rh) || rh < 0 || rh > 100) return null;
  const tw = t * Math.atan(0.151977 * Math.sqrt(rh + 8.313659))
    + Math.atan(t + rh)
    - Math.atan(rh - 1.67633)
    + 0.00391838 * Math.pow(rh, 1.5) * Math.atan(0.023101 * rh)
    - 4.686035;
  const apparent = -0.2442 + 0.55399 * tw + 0.45535 * t - 0.0022 * tw * tw + 0.00278 * tw * t + 3.0;
  return Math.round(apparent * 10) / 10;
}

function getLevel(value) {
  return levels.find((level) => value >= level.min);
}

function formatTime(value, includeDate = false) {
  const date = value ? new Date(value) : null;
  if (!date || Number.isNaN(date.getTime())) return "확인 중";
  return date.toLocaleString("ko-KR", includeDate
    ? { month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit" }
    : { hour: "2-digit", minute: "2-digit" });
}

function setPressed(selector, dataName, value) {
  $$(selector).forEach((button) => button.setAttribute("aria-pressed", String(button.dataset[dataName] === value)));
}

function applyGuideTheme(level) {
  document.documentElement.style.setProperty("--risk", level.color);
  document.documentElement.style.setProperty("--risk-dark", level.dark);
  document.documentElement.style.setProperty("--risk-soft", level.soft);
  $("#guideLevelDot").style.background = level.color;
  $("#guideLevelDot").style.boxShadow = `0 0 0 7px ${level.soft}`;
}

function renderHero() {
  const usingField = state.appliedSource === "field" && state.fieldValue !== null;
  const value = usingField ? state.fieldValue : state.autoValue;
  const temp = usingField ? state.fieldTemp : state.autoTemp;
  const humidity = usingField ? state.fieldRh : state.autoRh;
  const observed = usingField ? state.fieldAppliedAt : state.autoObserved;
  const sourceName = usingField ? "현장 입력값" : "기상청 실황";
  const locationText = usingField
    ? `${stationData[state.station].name} 현장 측정값`
    : `${stationData[state.station].name} 인근 자동값`;

  $("#heroLocation").textContent = locationText;
  $("#heroSource").textContent = sourceName;

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
  $("#heroObserved").textContent = usingField ? `${formatTime(observed)} 적용` : `${formatTime(observed)} 관측`;
  $("#updated").textContent = usingField
    ? `현장값 ${formatTime(state.fieldAppliedAt, true)} 적용`
    : `${formatTime(state.generatedAt, true)} 기상자료 갱신`;
}

async function loadWeather() {
  $("#headerStatus").textContent = "기상 연동 중";
  try {
    const response = await fetch(`weather.json?v=${Date.now()}`, { cache: "no-store" });
    if (!response.ok) throw new Error(`weather.json ${response.status}`);
    const data = await response.json();
    const station = data.stations?.[state.station];
    if (!station?.current || !Array.isArray(station.hourly) || station.hourly.length === 0) throw new Error("역별 기상자료 없음");

    const row = station.current;
    const temp = Number(row.temp);
    const humidity = Number(row.rh);
    const apparent = Number(row.hi);
    if (![temp, humidity, apparent].every(Number.isFinite)) throw new Error("잘못된 실황값");

    state.autoValue = apparent;
    state.autoTemp = temp;
    state.autoRh = humidity;
    state.autoObserved = row.time;
    state.generatedAt = data.generatedAt || Date.now();
    state.hourly = station.hourly.map((item) => ({ time: item.time, temp: Number(item.temp), rh: Number(item.rh), hi: Number(item.hi) }));
    $("#weatherMeta").textContent = `${stationData[state.station].name} 인근 기상청 초단기실황과 여름철 체감온도 산식을 적용한 참고값입니다. 실제 작업 판단은 현장 측정값과 회사 지침을 우선합니다.`;
    $("#headerStatus").textContent = "기상 연동 정상";
    renderHero();
    renderForecast();
    renderGuide();
  } catch (error) {
    console.error(error);
    state.autoValue = null;
    state.autoTemp = null;
    state.autoRh = null;
    state.autoObserved = null;
    state.hourly = [];
    $("#headerStatus").textContent = "기상 연동 확인 필요";
    $("#weatherMeta").textContent = "기상청 자료를 불러오지 못했습니다. 현장 온·습도계 측정값과 회사 지침을 우선 적용하세요.";
    renderHero();
    renderForecast();
    renderGuide();
  }
}

function isInShift(date) {
  const hour = date.getHours() + date.getMinutes() / 60;
  if (state.shift === "day") return hour >= 9 && hour <= 18.67;
  return hour >= 18.17 || hour <= 9;
}

function getForecastRows() {
  const now = new Date();
  return state.hourly
    .filter((item) => {
      const date = new Date(item.time);
      return date >= new Date(now.getTime() - 3600000) && isInShift(date);
    })
    .slice(0, 12);
}

function getHotWindow(rows, highest) {
  const hotRows = rows.filter((item) => item.hi >= highest.hi - 1.0);
  if (hotRows.length === 0) return "--";
  const first = new Date(hotRows[0].time);
  const last = new Date(hotRows[hotRows.length - 1].time);
  const firstText = `${first.getHours()}시`;
  const lastText = `${last.getHours()}시`;
  return firstText === lastText ? firstText : `${firstText}~${lastText}`;
}

function renderForecast() {
  const rows = getForecastRows();
  const forecast = $("#forecast");
  if (rows.length === 0) {
    $("#forecastMax").textContent = "--℃";
    $("#forecastLevel").textContent = "확인 중";
    $("#forecastPeakTime").textContent = "--";
    $("#forecastHotWindow").textContent = "--";
    $("#forecastTrend").textContent = "--";
    $("#forecastAdvice").textContent = state.hourly.length ? "선택한 근무시간의 남은 예보가 없습니다." : "시간별 예보를 불러오지 못했습니다.";
    forecast.innerHTML = '<div class="empty-state">표시할 시간별 예보가 없습니다.</div>';
    return;
  }

  const highest = rows.reduce((max, item) => item.hi > max.hi ? item : max, rows[0]);
  const highestLevel = getLevel(highest.hi);
  const currentLevel = state.autoValue === null ? null : getLevel(state.autoValue);
  const peakTime = new Date(highest.time);
  const trend = currentLevel && highestLevel.rank > currentLevel.rank
    ? `${currentLevel.name} → ${highestLevel.name} 상승 예상`
    : `${highestLevel.name} 단계 · 추가 상승 없음`;

  const highlight = $("#forecastHighlight");
  highlight.style.setProperty("--forecast-color", highestLevel.color);
  highlight.style.setProperty("--forecast-dark", highestLevel.dark);
  highlight.style.setProperty("--forecast-soft", highestLevel.soft);
  $("#forecastMax").textContent = `${highest.hi.toFixed(1)}℃`;
  $("#forecastLevel").textContent = highestLevel.name;
  $("#forecastPeakTime").textContent = `${peakTime.getHours()}시경`;
  $("#forecastHotWindow").textContent = getHotWindow(rows, highest);
  $("#forecastTrend").textContent = trend;
  $("#forecastAdvice").textContent = forecastAdvice[highestLevel.key];
  $("#forecastSummary").textContent = `${rows.length}개 시간대 · 기상청 단기예보`;

  const now = new Date();
  forecast.innerHTML = rows.map((item) => {
    const date = new Date(item.time);
    const level = getLevel(item.hi);
    const current = date.getHours() === now.getHours() && date.toDateString() === now.toDateString();
    return `<article class="forecast-item" data-current="${current}" style="--item-risk:${level.color};--item-risk-dark:${level.dark}" aria-label="${date.getHours()}시, 체감온도 ${item.hi.toFixed(1)}도, ${level.name}">
      <div class="forecast-time">${date.getHours()}시</div>
      <div class="forecast-temp">${item.hi.toFixed(1)}℃</div>
      <div class="forecast-level">${level.name}</div>
    </article>`;
  }).join("");
}

function renderHomeSupport() {
  const target = $("#homeSupport");
  if (state.job !== "platform") {
    target.innerHTML = "";
    return;
  }
  target.innerHTML = `<div class="support-panel">
    <h3>폭염 시 취약고객 안내</h3>
    <ul>
      <li>고령자·어린이·임산부·거동 불편 고객의 장시간 더위 노출 확인</li>
      <li>어지럼·기력저하·비틀거림 발생 시 그늘 또는 냉방장소 안내</li>
      <li>혼자 이동하기 어려운 고객의 안전한 이동 지원 및 주변 직원 지원 요청</li>
      <li>의식·말투·걸음 이상 또는 상태 미회복 시 119 신고</li>
      <li>고객 지원으로 직원의 옥외 노출 장기화 시 즉시 추가 지원 요청</li>
    </ul>
  </div>`;
}

function renderGuide() {
  const value = state.source === "field" ? state.fieldValue : state.autoValue;
  const sourceLabel = state.source === "field" ? "현장 입력값" : "기상 자동값";
  const jobLabel = state.job === "yard" ? "수송" : "홈안내";
  $("#guideContext").textContent = `${jobLabel} · ${sourceLabel}`;
  $("#fieldPanel").hidden = state.source !== "field";

  if (value === null) {
    applyGuideTheme({ color: "#70808b", dark: "#46555f", soft: "#eef1f3" });
    $("#guideStatus").textContent = state.source === "field" ? "현장값 입력 필요" : "기상정보 확인 중";
    $("#guideSummary").textContent = state.source === "field"
      ? "현장 온도와 습도를 입력한 뒤 계산값을 적용하세요."
      : "값이 준비되면 현재 단계의 핵심 지침이 표시됩니다.";
    $("#keyList").innerHTML = "";
    renderHomeSupport();
    return;
  }

  const level = getLevel(value);
  const guide = guides[level.key];
  applyGuideTheme(level);
  $("#guideStatus").textContent = `체감 ${value.toFixed(1)}℃ · ${level.name}`;
  $("#guideSummary").textContent = guide.summary;
  $("#keyList").innerHTML = guide[state.job].map((item, index) => `<li class="guide-item">
    <span class="guide-number">${String(index + 1).padStart(2, "0")}</span>
    <span class="guide-text">${item}</span>
  </li>`).join("");
  renderHomeSupport();
}

function updateField() {
  const temp = Number.parseFloat($("#tempInput").value);
  const humidity = Number.parseFloat($("#rhInput").value);
  const apparent = heatIndex(temp, humidity);
  if (apparent === null) {
    state.fieldValue = null;
    state.fieldTemp = null;
    state.fieldRh = null;
    $("#fieldResult").textContent = "값을 입력하세요";
    $("#fieldResult").style.color = "";
    $("#useField").disabled = true;
    renderGuide();
    return;
  }
  const level = getLevel(apparent);
  state.fieldValue = apparent;
  state.fieldTemp = temp;
  state.fieldRh = humidity;
  $("#fieldResult").textContent = `${apparent.toFixed(1)}℃ · ${level.name}`;
  $("#fieldResult").style.color = level.dark;
  $("#useField").disabled = false;
  renderGuide();
}

function updateConditionCheck() {
  const selected = $$(".condition-check:checked").map((item) => item.value);
  let title = "선택한 증상 없음";
  let body = "근무 중 상태 변화 시 다시 확인";
  let color = "#17834b";
  if (selected.includes("heat")) {
    title = "즉시 작업 중지 및 냉방장소 이동";
    body = "상태 공유 · 신속한 냉각 · 빠른 회복이 없으면 119 또는 의료기관 도움 요청";
    color = "#c72c2c";
  } else if (selected.includes("illness")) {
    title = "옥외작업 전 관리자 확인 필요";
    body = "탈수·체온 상승 위험 증가 · 시원한 장소에서 수분 보충 · 증상 지속 시 의료기관 안내";
    color = "#c45600";
  } else if (selected.length >= 2 || selected.includes("fatigue")) {
    title = "업무 강도·더위 노출 축소";
    body = "동료·관리자에게 상태 공유 · 악화 시 즉시 작업 중지";
    color = "#9a6500";
  } else if (selected.includes("sleep")) {
    title = "수면 상태 공유 및 무리한 작업 방지";
    body = "동료·관리자에게 사전 공유 · 휴식계획 확인";
    color = "#9a6500";
  }
  const target = $("#conditionResult");
  target.style.setProperty("--condition-color", color);
  target.innerHTML = `<strong>${title}</strong><p>${body}</p>`;
}

$$('[data-station]').forEach((button) => button.addEventListener("click", () => {
  state.station = button.dataset.station;
  setPressed('[data-station]', "station", state.station);
  loadWeather();
}));

$$('[data-shift]').forEach((button) => button.addEventListener("click", () => {
  state.shift = button.dataset.shift;
  setPressed('[data-shift]', "shift", state.shift);
  renderForecast();
}));

$$('[data-source]').forEach((button) => button.addEventListener("click", () => {
  state.source = button.dataset.source;
  if (state.source === "auto") state.appliedSource = "auto";
  setPressed('[data-source]', "source", state.source);
  renderHero();
  renderGuide();
}));

$$('[data-job]').forEach((button) => button.addEventListener("click", () => {
  state.job = button.dataset.job;
  setPressed('[data-job]', "job", state.job);
  renderGuide();
}));

$("#tempInput").addEventListener("input", updateField);
$("#rhInput").addEventListener("input", updateField);
$("#useField").addEventListener("click", () => {
  if (state.fieldValue === null) return;
  state.source = "field";
  state.appliedSource = "field";
  state.fieldAppliedAt = new Date();
  setPressed('[data-source]', "source", state.source);
  renderHero();
  renderGuide();
  $("#action-title").scrollIntoView({ behavior: "smooth", block: "start" });
});

$$(".condition-check").forEach((checkbox) => checkbox.addEventListener("change", updateConditionCheck));

updateConditionCheck();
renderHero();
renderGuide();
loadWeather();
