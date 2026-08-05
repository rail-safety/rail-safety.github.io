(() => {
  // 시간별 체감온도 구간 표시용 팔레트다. 공식 영향예보 발표 단계와는 구분한다.
  const palette = {
    normal: { color: "#587080", dark: "#344955", soft: "#d5dfe4", panel: "#e6ecef" },
    interest: { color: "#4f6f5e", dark: "#30483b", soft: "#cbd8d0", panel: "#dee6e1" },
    caution: { color: "#956b24", dark: "#5e4216", soft: "#dec787", panel: "#e8d9b2" },
    warning: { color: "#a65332", dark: "#66321e", soft: "#d89b72", panel: "#e4bfa9" },
    danger: { color: "#662633", dark: "#401820", soft: "#c17b86", panel: "#d3a0aa" }
  };

  const correctedGuides = {
    normal: {
      summary: "기본 예방수칙을 준비하고 체감온도 변화를 확인하세요.",
      yard: [
        "작업 전 물·온열질환 예방용품 준비",
        "불필요한 옥외 대기와 이동 최소화",
        "작업 후 실내 또는 그늘에서 몸 상태 확인"
      ],
      platform: [
        "안내 전 물·온열질환 예방용품 준비",
        "승강장 대기 시 차양·그늘 우선 이용",
        "안내 사이 실내 복귀 및 몸 상태 확인"
      ]
    },
    interest: {
      summary: "폭염안전 5대 기본수칙을 적용하고 적절한 냉방휴식을 확보하세요.",
      yard: [
        "시원한 물과 냉방·그늘 휴식공간 확보",
        "폭염 집중 시간대 작업 최소화 및 작업시간 조정 검토",
        "냉각조끼·넥쿨러 등 개인 보냉장구 준비",
        "작업 전후 본인과 동료의 온열질환 증상 확인"
      ],
      platform: [
        "시원한 물과 실내·그늘 휴식공간 확보",
        "안내 전 대기시간과 안내 후 승강장 체류 최소화",
        "냉각조끼·넥쿨러 등 개인 보냉장구 준비",
        "연속 안내 시 교대 또는 적절한 냉방휴식 확보"
      ]
    },
    caution: {
      summary: "매 2시간 이내 20분 이상 휴식하고 작업시간을 조정하세요.",
      yard: [
        "매 2시간 이내 20분 이상 냉방·그늘 휴식",
        "작업시간대 조정 또는 옥외작업 단축",
        "온열질환 민감군·고강도 작업자는 휴식 추가",
        "2인 이상 상호 말투·걸음·반응 확인"
      ],
      platform: [
        "매 2시간 이내 20분 이상 냉방·그늘 휴식",
        "승강장 안내시간 단축 및 실내 복귀 동선 확보",
        "연속 안내 전 교대자와 휴식시간 지정",
        "온열질환 민감군·고강도 업무 담당자는 휴식 추가"
      ]
    },
    warning: {
      summary: "매시간 15분 휴식하고 무더위 시간대 옥외작업을 조정·중지하세요.",
      yard: [
        "매시간 15분씩 냉방·그늘 휴식",
        "무더위 시간대에는 불가피한 경우 외 옥외작업 중지",
        "불가피한 작업은 최소 인원·최단시간 수행하고 휴식 충분히 부여",
        "담당자를 지정해 작업자의 건강상태 확인"
      ],
      platform: [
        "매시간 15분씩 냉방·그늘 휴식",
        "무더위 시간대 안내 인원·시간 조정 및 옥외 대기 제거",
        "연속 안내를 피하고 교대자·실내 복귀시간 지정",
        "담당자가 안내 직원과 인턴사원의 건강상태 확인"
      ]
    },
    danger: {
      summary: "재난·안전관리에 필요한 긴급조치 외 옥외작업을 중지하세요.",
      yard: [
        "재난·안전관리에 필요한 긴급조치 외 옥외작업 중지",
        "긴급작업도 최소 인원·최단시간 수행하고 휴식 충분히 부여",
        "온열질환 민감군의 옥외작업 제한",
        "보냉장구·연락수단 확보 및 담당자의 건강상태 지속 확인",
        "말투·걸음·의식 이상 시 즉시 작업 중지 및 119 신고"
      ],
      platform: [
        "재난·안전관리에 필요한 긴급 안내 외 옥외업무 최소화",
        "긴급 안내 시 교대 운영하고 냉방휴식 충분히 부여",
        "온열질환 민감군의 장시간 승강장 업무 제한",
        "담당자가 직원·인턴사원의 건강상태 지속 확인",
        "말투·걸음·의식 이상 시 즉시 교대·냉각 및 119 신고"
      ]
    }
  };

  const correctedForecastAdvice = {
    normal: "기본 예방수칙을 준비하고 이후 체감온도 변화를 확인하세요.",
    interest: "물·냉방휴식 장소·보냉장구를 준비하고 폭염 집중 시간대 노출을 줄이세요.",
    caution: "매 2시간 이내 20분 이상 휴식하고 작업시간 조정·교대계획을 확인하세요.",
    warning: "매시간 15분 휴식하고 무더위 시간대 옥외작업 조정·중지를 준비하세요.",
    danger: "긴급조치 외 옥외작업을 중지하고 보냉·교대·응급연락체계를 확인하세요."
  };

  const syncApplicationModel = () => {
    if (typeof levels === "undefined" || !Array.isArray(levels)) return;

    levels.splice(0, levels.length,
      { min: 38, key: "danger", name: "위험 수준", ...palette.danger, symbol: "!", rank: 4 },
      { min: 35, key: "warning", name: "경고 수준", ...palette.warning, symbol: "!", rank: 3 },
      { min: 33, key: "caution", name: "주의 수준", ...palette.caution, symbol: "!", rank: 2 },
      { min: 31, key: "interest", name: "관심 수준", ...palette.interest, symbol: "!", rank: 1 },
      { min: -99, key: "normal", name: "관심 미만", ...palette.normal, symbol: "✓", rank: 0 }
    );

    if (typeof guides !== "undefined") {
      Object.keys(guides).forEach((key) => delete guides[key]);
      Object.assign(guides, correctedGuides);
    }
    if (typeof forecastAdvice !== "undefined") {
      Object.keys(forecastAdvice).forEach((key) => delete forecastAdvice[key]);
      Object.assign(forecastAdvice, correctedForecastAdvice);
    }
  };

  const getRiskKey = (label = "") => {
    const text = label.trim();
    if (text.includes("관심 미만")) return "normal";
    if (text.includes("위험")) return "danger";
    if (text.includes("경고")) return "warning";
    if (text.includes("주의")) return "caution";
    if (text.includes("관심")) return "interest";
    return "";
  };

  const applyRiskTheme = () => {
    document.querySelectorAll(".forecast-item").forEach((item) => {
      const key = getRiskKey(item.querySelector(".forecast-level")?.textContent);
      if (!key) return;
      item.dataset.riskLevel = key;
      const colors = palette[key];
      item.style.setProperty("--item-risk", colors.color);
      item.style.setProperty("--item-risk-dark", colors.dark);
      item.style.setProperty("--item-risk-soft", colors.soft);
    });

    const highlight = document.querySelector("#forecastHighlight");
    const key = getRiskKey(document.querySelector("#forecastLevel")?.textContent);
    if (highlight && key) {
      highlight.dataset.riskLevel = key;
      const colors = palette[key];
      highlight.style.setProperty("--forecast-color", colors.color);
      highlight.style.setProperty("--forecast-dark", colors.dark);
      highlight.style.setProperty("--forecast-soft", colors.panel);
    }
  };

  const officialCriteriaNote = "시간별 체감온도 수치가 어느 구간에 해당하는지 보여주는 참고 표시입니다. 기상청 공식 폭염 영향예보는 일 최고 체감온도·지속일수·분야별 영향을 종합해 별도로 발표합니다. 실제 작업 판단은 현장 측정값과 회사 지침을 우선합니다.";

  const applyOfficialCriteriaCopy = () => {
    const weatherMeta = document.querySelector("#weatherMeta");
    if (weatherMeta && weatherMeta.textContent !== officialCriteriaNote) weatherMeta.textContent = officialCriteriaNote;

    const title = document.querySelector("#standards-title");
    if (title) title.textContent = "2026년 체감온도 구간별 대응 기준";

    const list = document.querySelector(".standards-list");
    if (list) {
      list.innerHTML = `
        <div class="standard-row standard-row--interest"><strong>31℃</strong><span><b>관심 수준</b> · 폭염안전 5대 기본수칙 및 적절한 휴식</span></div>
        <div class="standard-row standard-row--caution"><strong>33℃</strong><span><b>주의 수준</b> · 매 2시간 이내 20분 이상 휴식, 작업시간 조정·옥외작업 단축</span></div>
        <div class="standard-row standard-row--warning"><strong>35℃</strong><span><b>경고 수준</b> · 매시간 15분 휴식, 무더위 시간대 불가피한 경우 외 옥외작업 중지</span></div>
        <div class="standard-row standard-row--danger"><strong>38℃</strong><span><b>위험 수준</b> · 재난·안전관리 긴급조치 외 옥외작업 중지</span></div>`;
    }

    const note = document.querySelector(".standards-note");
    if (note) note.textContent = "위 단계명은 시간별 체감온도 수치의 구간 표시입니다. 기상청 공식 영향예보 단계는 일 최고 체감온도와 지속일수, 분야별 영향을 종합해 발표합니다. 작업장에서는 현장 체감온도와 고용노동부·안전보건공단 대응지침, 회사 폭염 대응계획을 함께 적용합니다.";
  };

  // 상단 히어로는 항상 기상청 자동값만 표시한다.
  // 현장 입력값은 아래 현장 업무 지침의 적용 기준에만 사용한다.
  const lockHeroToAutomaticWeather = () => {
    if (typeof renderHero !== "function") return;

    renderHero = function renderAutomaticWeatherHero() {
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
    };

    renderHero();
  };

  const createDialog = () => {
    const dialog = document.createElement("dialog");
    dialog.className = "install-dialog";
    dialog.innerHTML = `
      <div class="install-dialog__body">
        <h2 id="installDialogTitle">홈 화면에 추가</h2>
        <div id="installDialogContent"></div>
        <button class="install-dialog__close" type="button">확인</button>
      </div>`;
    document.body.append(dialog);
    dialog.querySelector(".install-dialog__close").addEventListener("click", () => dialog.close());
    return dialog;
  };

  const showInstallGuide = (dialog) => {
    const isiOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
    const content = dialog.querySelector("#installDialogContent");
    content.innerHTML = isiOS
      ? `<p>아이폰에서는 웹페이지가 설치 창을 직접 열 수 없습니다.</p>
         <ol><li>Safari에서 아래쪽의 <strong>공유</strong> 버튼을 누릅니다.</li><li><strong>홈 화면에 추가</strong>를 선택합니다.</li><li>오른쪽 위의 <strong>추가</strong>를 누릅니다.</li></ol>`
      : `<p>브라우저 메뉴에서 이 사이트를 앱처럼 설치할 수 있습니다.</p>
         <ol><li>브라우저 메뉴를 엽니다.</li><li><strong>앱 설치</strong> 또는 <strong>홈 화면에 추가</strong>를 선택합니다.</li></ol>`;
    dialog.showModal();
  };

  const init = () => {
    syncApplicationModel();
    lockHeroToAutomaticWeather();
    applyOfficialCriteriaCopy();
    applyRiskTheme();

    const observer = new MutationObserver(() => {
      applyRiskTheme();
      applyOfficialCriteriaCopy();
    });
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });

    const header = document.querySelector(".page-header");
    if (!header) return;

    const tools = document.createElement("div");
    tools.className = "shell page-quick-actions";
    tools.setAttribute("aria-label", "페이지 빠른 기능");
    tools.innerHTML = `
      <button class="page-action-button" id="sharePage" type="button">
        <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 16V3m0 0 4 4m-4-4-4 4M5 13v7h14v-7" /></svg>
        <span class="page-action-button__status">공유</span>
      </button>
      <button class="page-action-button" id="installApp" type="button">
        <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 3v12m0 0 4-4m-4 4-4-4M5 19h14" /></svg>
        <span class="page-action-button__status">홈 화면 추가</span>
      </button>`;
    header.append(tools);

    const shareButton = tools.querySelector("#sharePage");
    const shareStatus = shareButton.querySelector(".page-action-button__status");
    shareButton.addEventListener("click", async () => {
      const shareData = {
        title: "순천관리역 폭염 안전 가이드",
        text: "철도역 현장직원용 폭염 안전 가이드",
        url: location.origin + location.pathname
      };
      try {
        if (navigator.share) {
          await navigator.share(shareData);
        } else {
          await navigator.clipboard.writeText(shareData.url);
          shareStatus.textContent = "주소 복사됨";
          setTimeout(() => { shareStatus.textContent = "공유"; }, 1500);
        }
      } catch (error) {
        if (error?.name !== "AbortError") {
          shareStatus.textContent = "다시 시도";
          setTimeout(() => { shareStatus.textContent = "공유"; }, 1500);
        }
      }
    });

    const installButton = tools.querySelector("#installApp");
    const installStatus = installButton.querySelector(".page-action-button__status");
    const dialog = createDialog();
    let deferredPrompt = null;
    const standalone = window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
    if (standalone) installButton.hidden = true;

    window.addEventListener("beforeinstallprompt", (event) => {
      event.preventDefault();
      deferredPrompt = event;
      installButton.hidden = false;
    });

    installButton.addEventListener("click", async () => {
      if (!deferredPrompt) {
        showInstallGuide(dialog);
        return;
      }
      deferredPrompt.prompt();
      const choice = await deferredPrompt.userChoice;
      deferredPrompt = null;
      if (choice.outcome === "accepted") {
        installStatus.textContent = "설치 완료";
        setTimeout(() => { installButton.hidden = true; }, 700);
      }
    });

    window.addEventListener("appinstalled", () => {
      deferredPrompt = null;
      installButton.hidden = true;
    });

    if ("serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker.register("./service-worker.js?v=20260805-0945").catch((error) => {
          console.error("서비스 워커 등록 실패", error);
        });
      });
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
