const stationData = {
  suncheon: { name: "순천역" },
  gokseong: { name: "곡성역" },
  gurye: { name: "구례구역" },
  beolgyo: { name: "벌교역" },
  boseong: { name: "보성역" }
};

const levels = [
  { min: 38, key: "extreme", name: "매우 위험", color: "#7f1d1d", dark: "#571313", soft: "#fcecec", symbol: "!" },
  { min: 35, key: "danger", name: "위험", color: "#c72c2c", dark: "#8f1e1e", soft: "#fff0f0", symbol: "!" },
  { min: 33, key: "warning", name: "경고", color: "#c45600", dark: "#8f3e00", soft: "#fff1e5", symbol: "!" },
  { min: 31, key: "caution", name: "주의", color: "#9a6500", dark: "#6f4900", soft: "#fff7df", symbol: "!" },
  { min: -99, key: "normal", name: "안전", color: "#17834b", dark: "#0d6538", soft: "#e9f6ef", symbol: "✓" }
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

const state = {
  station: "suncheon",
  shift: "day",
  source: "auto",
  job: "yard",
  autoValue: null,
  fieldValue: null,
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

function applyRiskTheme(level) {
  document.documentElement.style.setProperty("--risk", level.color);
  document.documentElement.style.setProperty("--risk-dark", level.dark);
  document.documentElement.style.setProperty("--risk-soft", level.soft);
}

function setSegment(groupSelector, dataName, value) {
  $$(groupSelector).forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset[dataName] === value));
  });
}

function formatObservationTime(value) {
  const date = value ? new Date(value) : null;
  if (!date || Number.isNaN(date.getTime())) return "최근 관측";
  return date.toLocaleString("ko-KR", { month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

async function loadWeather() {
  const currentTemp = $("#currentTemp");
  const currentBadge = $("#currentBadge");
  const weatherMeta = $("#weatherMeta");
  const headerStatus = $("#headerStatus");

  currentTemp.textContent = "--℃";
  currentBadge.innerHTML = '<span class="risk-symbol" aria-hidden="true">·</span><span>확인 중</span>';
  weatherMeta.textContent = "기상청 초단기실황을 확인하고 있습니다.";
  headerStatus.textContent = "기상 연동 중";

  try {
    const response = await fetch(`weather.json?v=${Date.now()}`, { cache: "no-store" });
    if (!response.ok) throw new Error(`weather.json ${response.status}`);
    const data = await response.json();
    const station = data.stations?.[state.station];
    if (!station?.current || !Array.isArray(station.hourly) || station.hourly.length === 0) {
      throw new Error("역별 기상자료 없음");
    }

    const row = station.current;
    const temp = Number(row.temp);
    const humidity = Number(row.rh);
    const apparent = Number(row.hi);
    if (![temp, humidity, apparent].every(Number.isFinite)) throw new Error("잘못된 실황값");

    state.autoValue = apparent;
    state.hourly = station.hourly.map((item) => ({
      time: item.time,
      temp: Number(item.temp),
      rh: Number(item.rh),
      hi: Number(item.hi)
    }));

    const level = getLevel(apparent);
    applyRiskTheme(level);
    currentTemp.textContent = `${apparent.toFixed(1)}℃`;
    currentBadge.innerHTML = `<span class="risk-symbol" aria-hidden="true">${level.symbol}</span><span>${level.name}</span>`;
    weatherMeta.textContent = `기온 ${temp.toFixed(1)}℃ · 습도 ${Math.round(humidity)}% · ${formatObservationTime(row.time)} 관측`;
    $("#currentAction").textContent = guides[level.key].summary;
    $("#updated").textContent = `${new Date(data.generatedAt || Date.now()).toLocaleString("ko-KR")} 갱신`;
    headerStatus.textContent = "기상 연동 정상";
    renderForecast();
    renderGuide();
  } catch (error) {
    console.error(error);
    state.autoValue = null;
    state.hourly = [];
    currentTemp.textContent = "확인 실패";
    currentBadge.innerHTML = '<span class="risk-symbol" aria-hidden="true">!</span><span>현장값 우선</span>';
    weatherMeta.textContent = "기상청 자료를 불러오지 못했습니다. 현장 측정값을 입력하세요.";
    $("#currentAction").textContent = "현장 온·습도계 측정값과 회사 지침을 우선 적용하세요.";
    $("#updated").textContent = "기상정보 불러오기 실패";
    headerStatus.textContent = "기상 연동 확인 필요";
    renderForecast();
    renderGuide();
  }
}

function isInShift(date) {
  const hour = date.getHours() + date.getMinutes() / 60;
  if (state.shift === "day") return hour >= 9 && hour <= 18.67;
  return hour >= 18.17 || hour <= 9;
}

function renderForecast() {
  const forecast = $("#forecast");
  const summary = $("#forecastSummary");
  const now = new Date();
  const rows = state.hourly
    .filter((item) => {
      const date = new Date(item.time);
      return date >= new Date(now.getTime() - 3600000) && isInShift(date);
    })
    .slice(0, 12);

  if (rows.length === 0) {
    summary.textContent = state.hourly.length ? "선택한 근무시간의 남은 예보가 없습니다." : "시간별 예보를 불러오지 못했습니다.";
    forecast.innerHTML = '<div class="empty-state">표시할 시간별 예보가 없습니다.</div>';
    return;
  }

  const highest = rows.reduce((max, item) => item.hi > max.hi ? item : max, rows[0]);
  const highestLevel = getLevel(highest.hi);
  const highestTime = new Date(highest.time).toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });
  summary.innerHTML = `근무시간 중 최고 <strong>${highest.hi.toFixed(1)}℃ · ${highestLevel.name}</strong> <span class="microcopy">(${highestTime} 예상)</span>`;

  forecast.innerHTML = rows.map((item) => {
    const date = new Date(item.time);
    const level = getLevel(item.hi);
    const label = date.toLocaleString("ko-KR", { month: "numeric", day: "numeric", hour: "2-digit" });
    return `<article class="forecast-item" style="--item-risk:${level.color};--item-risk-dark:${level.dark}" aria-label="${label}, 체감온도 ${item.hi.toFixed(1)}도, ${level.name}">
      <div class="forecast-time">${label}</div>
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
  $("#guideSource").textContent = state.source === "field" ? "현장 입력값" : "기상 자동값";

  if (value === null) {
    $("#guideStatus").textContent = state.source === "field" ? "현장값 입력 필요" : "기상정보 확인 중";
    $("#guideSummary").textContent = state.source === "field"
      ? "현장 온도와 습도를 입력한 뒤 행동지침에 적용하세요."
      : "값이 준비되면 현재 단계 지침이 표시됩니다.";
    $("#keyList").innerHTML = "";
    renderHomeSupport();
    return;
  }

  const level = getLevel(value);
  const guide = guides[level.key];
  const items = guide[state.job];
  applyRiskTheme(level);
  $("#guideStatus").textContent = `체감 ${value.toFixed(1)}℃ · ${level.name}`;
  $("#guideSummary").textContent = guide.summary;
  $("#keyList").innerHTML = items.map((item, index) => `<li class="guide-item">
    <span class="guide-number">${String(index + 1).padStart(2, "0")}</span>
    <span class="guide-text">${item}</span>
  </li>`).join("");
  renderHomeSupport();
}

function updateField() {
  const temp = Number.parseFloat($("#tempInput").value);
  const humidity = Number.parseFloat($("#rhInput").value);
  const apparent = heatIndex(temp, humidity);
  const result = $("#fieldResult");
  const button = $("#useField");

  if (apparent === null) {
    state.fieldValue = null;
    result.textContent = "값을 입력하세요";
    button.disabled = true;
    if (state.source === "field") renderGuide();
    return;
  }

  state.fieldValue = apparent;
  const level = getLevel(apparent);
  result.textContent = `${apparent.toFixed(1)}℃ · ${level.name}`;
  result.style.color = level.dark;
  button.disabled = false;
  if (state.source === "field") renderGuide();
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

$("#stationSelect").addEventListener("change", (event) => {
  state.station = event.target.value;
  loadWeather();
});

$$('[data-shift]').forEach((button) => button.addEventListener("click", () => {
  state.shift = button.dataset.shift;
  setSegment('[data-shift]', "shift", state.shift);
  renderForecast();
}));

$$('[data-source]').forEach((button) => button.addEventListener("click", () => {
  state.source = button.dataset.source;
  setSegment('[data-source]', "source", state.source);
  renderGuide();
}));

$$('[data-job]').forEach((button) => button.addEventListener("click", () => {
  state.job = button.dataset.job;
  setSegment('[data-job]', "job", state.job);
  renderGuide();
}));

$("#tempInput").addEventListener("input", updateField);
$("#rhInput").addEventListener("input", updateField);
$("#useField").addEventListener("click", () => {
  state.source = "field";
  setSegment('[data-source]', "source", state.source);
  renderGuide();
  $("#action-title").scrollIntoView({ behavior: "smooth", block: "start" });
});
$$(".condition-check").forEach((checkbox) => checkbox.addEventListener("change", updateConditionCheck));

updateConditionCheck();
renderGuide();
loadWeather();
