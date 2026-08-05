(() => {
  const MIN_SCALE_TEMP = 24;
  const MAX_SCALE_TEMP = 40;

  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const getBarPercent = (temperature) => {
    const ratio = (temperature - MIN_SCALE_TEMP) / (MAX_SCALE_TEMP - MIN_SCALE_TEMP);
    return clamp(ratio * 100, 8, 100);
  };

  const getStageLabel = (level) => level.name.replace(/\s*수준$/, "");

  if (typeof getForecastRows !== "function" || typeof getLevel !== "function") return;

  renderForecast = function renderForecastBars() {
    const rows = getForecastRows();
    const forecast = $("#forecast");

    if (rows.length === 0) {
      $("#forecastMax").textContent = "--℃";
      $("#forecastLevel").textContent = "확인 중";
      $("#forecastPeakTime").textContent = "--";
      $("#forecastHotWindow").textContent = "--";
      $("#forecastTrend").textContent = "--";
      $("#forecastAdvice").textContent = state.hourly.length
        ? "선택한 근무시간의 남은 예보가 없습니다."
        : "시간별 예보를 불러오지 못했습니다.";
      forecast.innerHTML = '<div class="empty-state">표시할 시간별 예보가 없습니다.</div>';
      return;
    }

    const highest = rows.reduce((max, item) => item.hi > max.hi ? item : max, rows[0]);
    const highestLevel = getLevel(highest.hi);
    const currentLevel = state.autoValue === null || state.autoStale ? null : getLevel(state.autoValue);
    const peakTime = new Date(highest.time);
    const trend = currentLevel && highestLevel.rank > currentLevel.rank
      ? `${currentLevel.name} → ${highestLevel.name} 상승 예상`
      : `${highestLevel.name} · 추가 상승 없음`;

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
    $("#forecastSummary").textContent = `${rows.length}개 시간대 · 막대 길이는 체감온도 기준`;

    const now = new Date();
    forecast.innerHTML = rows.map((item) => {
      const date = new Date(item.time);
      const level = getLevel(item.hi);
      const current = date.getHours() === now.getHours() && date.toDateString() === now.toDateString();
      const peak = item.time === highest.time;
      const timeLabel = formatForecastHour(date);
      const stageLabel = getStageLabel(level);
      const barPercent = getBarPercent(item.hi).toFixed(1);

      return `<article class="forecast-item forecast-item--bar" data-risk-level="${level.key}" data-current="${current}" data-peak="${peak}" style="--item-risk:${level.color};--item-risk-dark:${level.dark};--item-risk-soft:${level.soft}" aria-label="${timeLabel}, 체감온도 ${item.hi.toFixed(1)}도, ${level.name}${peak ? ", 최고 시간대" : ""}">
        <div class="forecast-time-group">
          <time class="forecast-time" datetime="${item.time}">${timeLabel}</time>
          ${peak ? '<span class="forecast-peak-badge">최고</span>' : ''}
        </div>
        <div class="forecast-measure">
          <div class="forecast-bar-scale" style="--bar-width:${barPercent}%">
            <span class="forecast-bar-fill" aria-hidden="true"></span>
            <span class="forecast-value-cluster">
              <span class="forecast-temp-label">${item.hi.toFixed(1)}℃</span>
              <span class="forecast-stage-label">${stageLabel}</span>
            </span>
            <span class="forecast-level sr-only">${level.name}</span>
          </div>
        </div>
      </article>`;
    }).join("");
  };

  if (state.hourly.length > 0) renderForecast();
})();

(() => {
  const tempInput = document.querySelector("#tempInput");
  const humidityInput = document.querySelector("#rhInput");
  const result = document.querySelector("#fieldResult");
  const resultRow = document.querySelector(".field-result-row");
  const calculator = document.querySelector(".calculator-grid");
  const applyButton = document.querySelector("#useField");

  if (!tempInput || !humidityInput || !result || !resultRow || !calculator) return;

  const legacyUpdateField = typeof window.updateField === "function" ? window.updateField : null;
  if (legacyUpdateField) {
    tempInput.removeEventListener("input", legacyUpdateField);
    humidityInput.removeEventListener("input", legacyUpdateField);
  }
  applyButton?.remove();

  const resultInfo = resultRow.querySelector("div") || resultRow;
  let status = document.querySelector("#fieldAutoStatus");
  if (!status) {
    status = document.createElement("span");
    status.id = "fieldAutoStatus";
    status.className = "field-auto-status";
    status.setAttribute("aria-live", "polite");
    status.textContent = "온도·습도 입력 시 자동 적용";
    resultInfo.append(status);
  }

  let error = document.querySelector("#fieldInputError");
  if (!error) {
    error = document.createElement("p");
    error.id = "fieldInputError";
    error.className = "field-input-error";
    error.setAttribute("role", "status");
    error.setAttribute("aria-live", "polite");
    error.hidden = true;
    calculator.insertAdjacentElement("afterend", error);
  }

  [tempInput, humidityInput].forEach((input) => {
    const describedBy = new Set((input.getAttribute("aria-describedby") || "").split(/\s+/).filter(Boolean));
    describedBy.add("fieldInputError");
    input.setAttribute("aria-describedby", [...describedBy].join(" "));
  });

  let debounceTimer = 0;

  const showError = (message) => {
    error.textContent = message;
    error.hidden = false;
    status.textContent = "입력값 확인 필요";
    tempInput.setAttribute("aria-invalid", "true");
    humidityInput.setAttribute("aria-invalid", "true");
  };

  const clearError = () => {
    error.textContent = "";
    error.hidden = true;
    tempInput.removeAttribute("aria-invalid");
    humidityInput.removeAttribute("aria-invalid");
  };

  const applyFieldValues = () => {
    const rawTemp = tempInput.value.trim();
    const rawHumidity = humidityInput.value.trim();

    if (!rawTemp || !rawHumidity) {
      showError("현장 온도와 상대습도를 모두 입력해주세요.");
      return;
    }

    const temp = Number(rawTemp);
    const humidity = Number(rawHumidity);

    if (!Number.isFinite(temp) || !Number.isFinite(humidity)) {
      showError("숫자 형식으로 입력해주세요.");
      return;
    }
    if (temp < -20 || temp > 60) {
      showError("현장 온도는 -20℃에서 60℃ 사이로 입력해주세요.");
      return;
    }
    if (humidity < 0 || humidity > 100) {
      showError("상대습도는 0%에서 100% 사이로 입력해주세요.");
      return;
    }

    const apparent = heatIndex(temp, humidity);
    if (!Number.isFinite(apparent)) {
      showError("입력값으로 체감온도를 계산할 수 없습니다.");
      return;
    }

    clearError();
    const level = getLevel(apparent);
    const changed = state.fieldTemp !== temp || state.fieldRh !== humidity || state.fieldValue !== apparent;

    state.fieldValue = apparent;
    state.fieldTemp = temp;
    state.fieldRh = humidity;
    state.fieldAppliedAt = new Date();
    state.appliedSource = "field";

    result.textContent = `${apparent.toFixed(1)}℃ · ${level.name}`;
    result.style.color = level.dark;
    status.textContent = "입력값 자동 적용";

    if (state.source === "field" && changed && typeof window.renderGuide === "function") {
      window.renderGuide();
    }
  };

  const scheduleFieldUpdate = () => {
    window.clearTimeout(debounceTimer);
    status.textContent = "입력 확인 중";
    clearError();
    debounceTimer = window.setTimeout(applyFieldValues, 400);
  };

  tempInput.addEventListener("input", scheduleFieldUpdate);
  humidityInput.addEventListener("input", scheduleFieldUpdate);
})();

(() => {
  const STALE_OBSERVATION_MS = 2 * 60 * 60 * 1000;

  const isObservationStale = () => {
    const observedAt = state.autoObserved ? new Date(state.autoObserved) : null;
    return !observedAt || Number.isNaN(observedAt.getTime())
      ? false
      : Date.now() - observedAt.getTime() > STALE_OBSERVATION_MS;
  };

  const sourceChip = document.querySelector("#heroSource");
  if (sourceChip) sourceChip.hidden = true;

  const nightShiftLabel = document.querySelector('[data-shift="night"] span');
  if (nightShiftLabel) nightShiftLabel.textContent = "18:00~익일 09:00";

  window.renderHero = function renderFreshnessAwareHero() {
    const value = state.autoValue;
    const temp = state.autoTemp;
    const humidity = state.autoRh;
    const observed = state.autoObserved;
    const stale = value !== null && isObservationStale();
    state.autoStale = stale;

    const location = document.querySelector("#heroLocation");
    const title = document.querySelector("#current-status-title");
    const headerStatus = document.querySelector("#headerStatus");
    const weatherMeta = document.querySelector("#weatherMeta");

    if (location) location.textContent = `${stationData[state.station].name} 인근 기상청 관측값`;
    if (title) title.textContent = stale ? "최근 관측 체감온도" : "현재 체감온도";

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

    if (stale) {
      $(".hero").style.setProperty("--hero-risk", "#9a6b20");
      $("#currentTemp").innerHTML = `${value.toFixed(1)}<span>℃</span>`;
      $("#currentBadge").innerHTML = '<span class="hero__level-icon" aria-hidden="true">!</span><strong>갱신 지연</strong>';
      $("#currentAction").textContent = "관측값이 2시간 이상 지났습니다. 현장 측정값을 우선하세요.";
      $("#heroTemp").textContent = `기온 ${Number.isFinite(temp) ? temp.toFixed(1) : "--"}℃`;
      $("#heroHumidity").textContent = `습도 ${Number.isFinite(humidity) ? Math.round(humidity) : "--"}%`;
      $("#heroObserved").textContent = `${formatTime(observed)} 관측 · 갱신 지연`;
      $("#updated").textContent = `${formatTime(state.generatedAt, true)} 자료 생성`;
      if (headerStatus) headerStatus.textContent = "기상자료 갱신 지연";
      if (weatherMeta) weatherMeta.textContent = "자동 관측자료가 2시간 이상 갱신되지 않았습니다. 현장 온·습도계 측정값과 회사 지침을 우선 적용하세요.";
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
    if (headerStatus) headerStatus.textContent = "기상 연동 정상";
  };

  window.renderGuide = function renderFreshnessAwareGuide() {
    const staleAuto = state.source === "auto" && isObservationStale();
    const value = state.source === "field" ? state.fieldValue : (staleAuto ? null : state.autoValue);
    const sourceLabel = state.source === "field" ? "현장 입력값" : "기상 자동값";
    const jobLabel = state.job === "yard" ? "수송" : "홈안내";
    $("#guideContext").textContent = `${jobLabel} · ${sourceLabel}`;
    $("#fieldPanel").hidden = state.source !== "field";

    if (value === null) {
      applyGuideTheme({ color: "#70808b", dark: "#46555f", soft: "#eef1f3" });
      if (staleAuto) {
        $("#guideStatus").textContent = "기상자료 갱신 지연";
        $("#guideSummary").textContent = "오래된 자동값은 행동지침에 적용하지 않습니다. 현장 입력값을 선택하세요.";
      } else {
        $("#guideStatus").textContent = state.source === "field" ? "현장값 입력 필요" : "기상정보 확인 중";
        $("#guideSummary").textContent = state.source === "field"
          ? "현장 온도와 습도를 입력하면 계산 결과가 자동으로 반영됩니다."
          : "값이 준비되면 현재 단계의 핵심 지침이 표시됩니다.";
      }
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
  };

  renderHero();
  renderGuide();
  if (state.hourly.length > 0) renderForecast();
})();
