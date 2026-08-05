const stationData = {
  suncheon: { name: "순천역" },
  gokseong: { name: "곡성역" },
  gurye: { name: "구례구역" },
  beolgyo: { name: "벌교역" },
  boseong: { name: "보성역" }
};

const levels = [
  { min: 38, key: "danger", name: "위험 수준", color: "#662633", dark: "#401820", soft: "#c17b86", symbol: "!", rank: 4 },
  { min: 35, key: "warning", name: "경고 수준", color: "#a65332", dark: "#66321e", soft: "#d89b72", symbol: "!", rank: 3 },
  { min: 33, key: "caution", name: "주의 수준", color: "#956b24", dark: "#5e4216", soft: "#dec787", symbol: "!", rank: 2 },
  { min: 31, key: "interest", name: "관심 수준", color: "#4f6f5e", dark: "#30483b", soft: "#cbd8d0", symbol: "!", rank: 1 },
  { min: -99, key: "normal", name: "관심 미만", color: "#587080", dark: "#344955", soft: "#d5dfe4", symbol: "✓", rank: 0 }
];

const guides = {
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
};

const forecastAdvice = {
  normal: "기본 예방수칙을 준비하고 이후 체감온도 변화를 확인하세요.",
  interest: "물·냉방휴식 장소·보냉장구를 준비하고 폭염 집중 시간대 노출을 줄이세요.",
  caution: "매 2시간 이내 20분 이상 휴식하고 작업시간 조정·교대계획을 확인하세요.",
  warning: "매시간 15분 휴식하고 무더위 시간대 옥외작업 조정·중지를 준비하세요.",
  danger: "긴급조치 외 옥외작업을 중지하고 보냉·교대·응급연락체계를 확인하세요."
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
    $("#weatherMeta").textContent = "시간별 체감온도 수치가 어느 구간에 해당하는지 보여주는 참고 표시입니다. 기상청 공식 폭염 영향예보는 일 최고 체감온도·지속일수·분야별 영향을 종합해 별도로 발표합니다. 실제 작업 판단은 현장 측정값과 회사 지침을 우선합니다.";
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

function getShiftWindow(now = new Date()) {
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
    const peak = item.time === highest.time;
    const timeLabel = formatForecastHour(date);
    return `<article class="forecast-item" data-current="${current}" data-peak="${peak}" style="--item-risk:${level.color};--item-risk-dark:${level.dark};--item-risk-soft:${level.soft}" aria-label="${timeLabel}, 체감온도 ${item.hi.toFixed(1)}도, ${level.name}">
      <time class="forecast-time" datetime="${item.time}">${timeLabel}</time>
      <div class="forecast-track"><span class="forecast-level">${level.name}</span></div>
      <div class="forecast-temp">${item.hi.toFixed(1)}℃</div>
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

// accordion-single-open:start
// 공통 안전정보는 현장에서 한 번에 하나만 펼쳐지도록 한다.
const infoBlocks = $$(".info-block");
infoBlocks.forEach((block) => block.addEventListener("toggle", () => {
  if (!block.open) return;
  infoBlocks.forEach((other) => {
    if (other !== block) other.open = false;
  });
}));
if (infoBlocks[0] && !infoBlocks.some((block) => block.open)) infoBlocks[0].open = true;

// accordion-single-open:end

$$(".condition-check").forEach((checkbox) => checkbox.addEventListener("change", updateConditionCheck));

updateConditionCheck();
renderHero();
renderGuide();
loadWeather();
