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
