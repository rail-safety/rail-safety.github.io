(() => {
  if (typeof state === "undefined" || typeof $ !== "function" || typeof $$ !== "function") return;

  // 법정 의무, 정부 권고, 내부 업무지침의 성격을 명확히 구분한다.
  guides.interest.summary = "장시간 작업 시 법정 폭염작업 기준에 해당합니다. 냉방·통풍, 작업시간 조정과 필요한 휴식을 적용하세요.";
  guides.interest.yard = [
    "시원한 물과 냉방·그늘 휴식공간 확보",
    "냉방·통풍 또는 작업시간 조정 등 폭염 노출 저감조치",
    "냉각조끼·넥쿨러 등 개인 보냉장구 준비",
    "작업 전후 본인과 동료의 온열질환 증상 확인"
  ];
  guides.interest.platform = [
    "시원한 물과 실내·그늘 휴식공간 확보",
    "승강장 체류 최소화 및 작업시간 조정",
    "냉각조끼·넥쿨러 등 개인 보냉장구 준비",
    "연속 안내 시 교대 또는 적절한 냉방휴식 확보"
  ];

  guides.caution.summary = "법정 기준에 따라 매 2시간 이내 20분 이상 휴식하고, 정부 권고에 따라 작업시간을 조정하세요.";
  guides.caution.yard = [
    "법정 기준: 매 2시간 이내 20분 이상 냉방·그늘 휴식",
    "정부 권고: 작업시간대 조정 또는 옥외작업 단축",
    "온열질환 민감군·고강도 작업자는 휴식 추가",
    "2인 이상 상호 말투·걸음·반응 확인"
  ];
  guides.caution.platform = [
    "법정 기준: 매 2시간 이내 20분 이상 냉방·그늘 휴식",
    "정부 권고: 승강장 안내시간 단축 및 실내 복귀 동선 확보",
    "연속 안내 전 교대자와 휴식시간 지정",
    "온열질환 민감군·고강도 업무 담당자는 휴식 추가"
  ];

  guides.warning.summary = "정부 권고에 따라 14~17시에는 불가피한 경우 외 옥외작업을 중지하고 충분히 휴식하세요.";
  guides.warning.yard = [
    "안전보건공단 예방요령: 매시간 15분씩 냉방·그늘 휴식",
    "정부 권고: 14~17시 불가피한 경우 외 옥외작업 중지",
    "불가피한 작업은 최소 인원·최단시간 수행하고 휴식 충분히 부여",
    "담당자를 지정해 작업자의 건강상태 확인"
  ];
  guides.warning.platform = [
    "안전보건공단 예방요령: 매시간 15분씩 냉방·그늘 휴식",
    "정부 권고: 14~17시 안내 인원·시간 조정 및 옥외 대기 제거",
    "연속 안내를 피하고 교대자·실내 복귀시간 지정",
    "담당자가 안내 직원과 인턴사원의 건강상태 확인"
  ];

  guides.danger.summary = "정부 권고에 따라 재난·안전관리에 필요한 긴급조치 외 옥외작업을 중지하세요.";
  guides.danger.yard = [
    "정부 권고: 재난·안전관리 긴급조치 외 옥외작업 중지",
    "긴급작업도 최소 인원·최단시간 수행하고 휴식 충분히 부여",
    "온열질환 민감군의 옥외작업 제한",
    "보냉장구·연락수단 확보 및 담당자의 건강상태 지속 확인",
    "말투·걸음·의식 이상 시 즉시 작업 중지 및 119 신고"
  ];
  guides.danger.platform = [
    "정부 권고: 재난·안전관리에 필요한 긴급 안내 외 옥외업무 최소화",
    "긴급 안내 시 교대 운영하고 냉방휴식 충분히 부여",
    "온열질환 민감군의 장시간 승강장 업무 제한",
    "담당자가 직원·인턴사원의 건강상태 지속 확인",
    "말투·걸음·의식 이상 시 즉시 교대·냉각 및 119 신고"
  ];

  forecastAdvice.interest = "장시간 작업은 법정 폭염작업 기준에 해당할 수 있습니다. 물·냉방휴식·작업시간 조정을 준비하세요.";
  forecastAdvice.caution = "법정 휴식기준을 적용하고 작업시간 조정·옥외작업 단축을 준비하세요.";
  forecastAdvice.warning = "정부 권고에 따라 14~17시 불가피한 경우 외 옥외작업 중지를 준비하세요.";
  forecastAdvice.danger = "정부 권고에 따라 긴급조치 외 옥외작업 중지와 응급연락체계를 확인하세요.";

  const actionDescription = document.querySelector(".action-section .section-description");
  if (actionDescription) {
    actionDescription.textContent = "법정 기준·정부 권고·회사 폭염 대응계획을 함께 반영한 업무 안내입니다.";
  }

  const standardsTitle = document.querySelector("#standards-title");
  if (standardsTitle) standardsTitle.textContent = "체감온도별 법정·권고 조치";

  const standardsList = document.querySelector(".standards-list");
  if (standardsList) {
    standardsList.innerHTML = `
      <div class="standard-row standard-row--interest"><strong>31℃</strong><span><b>법정 적용기준</b> · 장시간 작업은 폭염작업에 해당하며 냉방·통풍, 작업시간 조정 또는 필요한 휴식 등 조치</span></div>
      <div class="standard-row standard-row--caution"><strong>33℃</strong><span><b>법정 의무</b> · 매 2시간 이내 20분 이상 휴식<br><small><b>정부 권고</b> · 작업시간 조정 또는 옥외작업 단축</small></span></div>
      <div class="standard-row standard-row--warning"><strong>35℃</strong><span><b>정부 권고</b> · 14~17시 불가피한 경우 외 옥외작업 중지</span></div>
      <div class="standard-row standard-row--danger"><strong>38℃</strong><span><b>정부 권고</b> · 재난·안전관리 긴급조치 외 옥외작업 중지</span></div>`;
  }

  const standardsNote = document.querySelector(".standards-note");
  if (standardsNote) {
    standardsNote.textContent = "법정 기준은 산업안전보건기준에 관한 규칙, 정부 권고는 2026년 고용노동부 대응지침 기준입니다. 회사 계획이 더 엄격하면 회사 기준을 우선합니다. 33℃ 휴식 예외는 별도 냉방·보냉조치를 갖춘 제한적 경우에 한하며 현장 개인 판단으로 생략하지 않습니다.";
  }

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
  if (refreshButton) refreshButton.setAttribute("aria-label", "페이지 전체 새로고침");

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

  if (typeof renderHero === "function") renderHero();
  if (typeof renderGuide === "function") renderGuide();
  if (state.hourly.length > 0 && typeof renderForecast === "function") renderForecast();
})();
