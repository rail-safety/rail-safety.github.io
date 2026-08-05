(() => {
  if (typeof state === "undefined" || typeof $ !== "function" || typeof $$ !== "function") return;

  // 주간은 실제 근무 종료시각까지 같은 근무일로 보고,
  // 야간은 09시 퇴근 기준으로 자정 이후에도 전날 18시부터의 근무를 유지한다.
  getShiftWindow = function getCorrectShiftWindow(now = new Date()) {
    const start = new Date(now);
    const end = new Date(now);

    if (state.shift === "day") {
      start.setHours(9, 0, 0, 0);
      end.setHours(18, 40, 0, 0);

      if (now > end) {
        start.setDate(start.getDate() + 1);
        end.setDate(end.getDate() + 1);
      }

      return { start, end, endExclusive: false };
    }

    const todayNine = new Date(now);
    todayNine.setHours(9, 0, 0, 0);
    const todayEighteen = new Date(now);
    todayEighteen.setHours(18, 0, 0, 0);

    if (now < todayNine) {
      start.setDate(start.getDate() - 1);
      start.setHours(18, 0, 0, 0);
      end.setHours(9, 0, 0, 0);
    } else {
      start.setHours(18, 0, 0, 0);
      end.setDate(end.getDate() + 1);
      end.setHours(9, 0, 0, 0);
    }

    return { start, end, endExclusive: true };
  };

  getForecastRows = function getCorrectForecastRows() {
    const { start, end, endExclusive } = getShiftWindow(new Date());

    return state.hourly
      .filter((item) => {
        const date = new Date(item.time);
        if (Number.isNaN(date.getTime()) || date < start) return false;
        return endExclusive ? date < end : date <= end;
      })
      .sort((a, b) => new Date(a.time) - new Date(b.time));
  };

  const nightShiftLabel = document.querySelector('[data-shift="night"] span');
  if (nightShiftLabel) nightShiftLabel.textContent = "18:00~익일 09:00";

  const refreshButton = document.querySelector("#refreshWeather");
  if (refreshButton) refreshButton.setAttribute("aria-label", "기상청 관측값 다시 불러오기");

  const resetFieldInput = () => {
    state.fieldValue = null;
    state.fieldTemp = null;
    state.fieldRh = null;
    state.fieldAppliedAt = null;
    state.source = "auto";
    state.appliedSource = "auto";

    const tempInput = document.querySelector("#tempInput");
    const humidityInput = document.querySelector("#rhInput");
    const result = document.querySelector("#fieldResult");
    const status = document.querySelector("#fieldAutoStatus");
    const error = document.querySelector("#fieldInputError");

    if (tempInput) {
      tempInput.value = "";
      tempInput.removeAttribute("aria-invalid");
    }
    if (humidityInput) {
      humidityInput.value = "";
      humidityInput.removeAttribute("aria-invalid");
    }
    if (result) {
      result.textContent = "값을 입력하세요";
      result.style.color = "";
    }
    if (status) status.textContent = "온도·습도 입력 시 자동 적용";
    if (error) {
      error.textContent = "";
      error.hidden = true;
    }
  };

  $$('[data-station]').forEach((button) => {
    button.addEventListener("click", () => {
      // 캡처 단계에서는 app.js가 아직 새 역을 state에 반영하기 전이다.
      if (button.dataset.station === state.station) return;

      resetFieldInput();
      state.autoValue = null;
      state.autoTemp = null;
      state.autoRh = null;
      state.autoObserved = null;
      state.generatedAt = null;
      state.autoStale = false;
      state.hourly = [];

      queueMicrotask(() => {
        setPressed('[data-source]', "source", "auto");
        if (typeof renderHero === "function") renderHero();
        if (typeof renderForecast === "function") renderForecast();
        if (typeof renderGuide === "function") renderGuide();
      });

      // 이전 입력의 debounce가 늦게 끝나더라도 빈 입력 오류가 남지 않게 정리한다.
      window.setTimeout(() => {
        const tempInput = document.querySelector("#tempInput");
        const humidityInput = document.querySelector("#rhInput");
        if ((tempInput?.value || "").trim() || (humidityInput?.value || "").trim()) return;

        const status = document.querySelector("#fieldAutoStatus");
        const error = document.querySelector("#fieldInputError");
        if (status) status.textContent = "온도·습도 입력 시 자동 적용";
        if (error) {
          error.textContent = "";
          error.hidden = true;
        }
      }, 450);
    }, { capture: true });
  });

  if (state.hourly.length > 0 && typeof renderForecast === "function") renderForecast();
})();
