(() => {
  // dataRiskLevel: 시간별 체감온도 구간의 작은 상태 강조에만 사용한다.
  const palette = {
    normal: { color: "#587080", dark: "#344955", soft: "#d5dfe4", panel: "#e6ecef" },
    interest: { color: "#4f6f5e", dark: "#30483b", soft: "#cbd8d0", panel: "#dee6e1" },
    caution: { color: "#956b24", dark: "#5e4216", soft: "#dec787", panel: "#e8d9b2" },
    warning: { color: "#a65332", dark: "#66321e", soft: "#d89b72", panel: "#e4bfa9" },
    danger: { color: "#662633", dark: "#401820", soft: "#c17b86", panel: "#d3a0aa" }
  };

  const getRiskKey = (label = "") => {
    const text = String(label).trim();
    if (text.includes("관심 미만")) return "normal";
    if (text.includes("위험")) return "danger";
    if (text.includes("경고")) return "warning";
    if (text.includes("주의")) return "caution";
    if (text.includes("관심")) return "interest";
    return "";
  };

  const applyRiskTheme = () => {
    document.querySelectorAll(".forecast-item").forEach((item) => {
      const label = item.querySelector(".forecast-level")?.textContent || "";
      const key = item.dataset.riskLevel || getRiskKey(label);
      const colors = palette[key];
      if (!colors) return;
      item.dataset.riskLevel = key;
      item.style.setProperty("--item-risk", colors.color);
      item.style.setProperty("--item-risk-dark", colors.dark);
      item.style.setProperty("--item-risk-soft", colors.soft);
    });

    const highlight = document.querySelector("#forecastHighlight");
    const key = getRiskKey(document.querySelector("#forecastLevel")?.textContent || "");
    const colors = palette[key];
    if (highlight && colors) {
      highlight.dataset.riskLevel = key;
      highlight.style.setProperty("--forecast-color", colors.color);
      highlight.style.setProperty("--forecast-dark", colors.dark);
      highlight.style.setProperty("--forecast-soft", colors.panel);
    }
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
    dialog.querySelector(".install-dialog__close")?.addEventListener("click", () => dialog.close());
    return dialog;
  };

  const showInstallGuide = (dialog) => {
    const isiOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
    const content = dialog.querySelector("#installDialogContent");
    if (!content) return;
    content.innerHTML = isiOS
      ? `<p>아이폰에서는 Safari 공유 메뉴를 이용합니다.</p>
         <ol><li>Safari 아래쪽의 <strong>공유</strong> 버튼을 누릅니다.</li><li><strong>홈 화면에 추가</strong>를 선택합니다.</li><li>오른쪽 위의 <strong>추가</strong>를 누릅니다.</li></ol>`
      : `<p>브라우저 메뉴에서 이 사이트를 앱처럼 설치할 수 있습니다.</p>
         <ol><li>브라우저 메뉴를 엽니다.</li><li><strong>앱 설치</strong> 또는 <strong>홈 화면에 추가</strong>를 선택합니다.</li></ol>`;

    if (typeof dialog.showModal === "function") dialog.showModal();
    else window.alert(isiOS ? "Safari 공유 버튼에서 ‘홈 화면에 추가’를 선택하세요." : "브라우저 메뉴에서 ‘홈 화면에 추가’를 선택하세요.");
  };

  const initQuickActions = () => {
    const header = document.querySelector(".page-header");
    if (!header || document.querySelector(".page-quick-actions")) return;

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
    const shareStatus = shareButton?.querySelector(".page-action-button__status");
    shareButton?.addEventListener("click", async () => {
      const shareData = {
        title: "순천관리역 폭염 안전 가이드",
        text: "철도역 현장직원용 폭염 안전 가이드",
        url: location.origin + location.pathname
      };
      try {
        if (navigator.share) await navigator.share(shareData);
        else if (navigator.clipboard) {
          await navigator.clipboard.writeText(shareData.url);
          if (shareStatus) shareStatus.textContent = "주소 복사됨";
          window.setTimeout(() => { if (shareStatus) shareStatus.textContent = "공유"; }, 1500);
        }
      } catch (error) {
        if (error?.name !== "AbortError" && shareStatus) {
          shareStatus.textContent = "다시 시도";
          window.setTimeout(() => { shareStatus.textContent = "공유"; }, 1500);
        }
      }
    });

    const installButton = tools.querySelector("#installApp");
    const installStatus = installButton?.querySelector(".page-action-button__status");
    const dialog = createDialog();
    let deferredPrompt = null;
    const standalone = window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
    if (standalone && installButton) installButton.hidden = true;

    window.addEventListener("beforeinstallprompt", (event) => {
      event.preventDefault();
      deferredPrompt = event;
      if (installButton) installButton.hidden = false;
    });

    installButton?.addEventListener("click", async () => {
      if (!deferredPrompt) {
        showInstallGuide(dialog);
        return;
      }
      deferredPrompt.prompt();
      const choice = await deferredPrompt.userChoice;
      deferredPrompt = null;
      if (choice.outcome === "accepted" && installStatus) {
        installStatus.textContent = "설치 완료";
        window.setTimeout(() => { if (installButton) installButton.hidden = true; }, 700);
      }
    });

    window.addEventListener("appinstalled", () => {
      deferredPrompt = null;
      if (installButton) installButton.hidden = true;
    });
  };

  const init = () => {
    applyRiskTheme();
    initQuickActions();

    // 시간별 전망과 최고 단계 문구가 다시 렌더링될 때만 색상 보조표시를 갱신한다.
    // 기준표 HTML을 감시 콜백에서 다시 만드는 코드는 제거하여 무한 반복을 방지한다.
    const observer = new MutationObserver(applyRiskTheme);
    const forecast = document.querySelector("#forecast");
    const forecastLevel = document.querySelector("#forecastLevel");
    if (forecast) observer.observe(forecast, { childList: true, subtree: true, characterData: true });
    if (forecastLevel) observer.observe(forecastLevel, { childList: true, characterData: true, subtree: true });

    if ("serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker.register("./service-worker.js?v=20260805-1305").catch((error) => {
          console.error("서비스 워커 등록 실패", error);
        });
      }, { once: true });
    }
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, { once: true });
  else init();
})();
