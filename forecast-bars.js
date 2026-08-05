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
    const currentLevel = state.autoValue === null ? null : getLevel(state.autoValue);
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

  const originalRenderGuide = window.renderGuide;
  if (typeof originalRenderGuide === "function") {
    window.renderGuide = function renderGuideWithAutomaticFieldCopy() {
      originalRenderGuide();
      if (state.source === "field" && state.fieldValue === null) {
        const guideSummary = document.querySelector("#guideSummary");
        if (guideSummary) guideSummary.textContent = "현장 온도와 습도를 입력하면 계산 결과가 자동으로 반영됩니다.";
      }
    };
  }

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
