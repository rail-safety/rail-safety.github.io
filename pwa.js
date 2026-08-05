(() => {
  // dataRiskLevel: 시간별 전망과 요약 카드의 단계색을 동일한 기준으로 동기화한다.
  const palette = {
    normal: { color: "#23824f", dark: "#0f5d36", soft: "#e2f3e8" },
    caution: { color: "#b97800", dark: "#6b4500", soft: "#fff0a8" },
    warning: { color: "#e56500", dark: "#883600", soft: "#ffd3a3" },
    danger: { color: "#d92d20", dark: "#8c1d17", soft: "#f8c0bc" },
    extreme: { color: "#8e1b1b", dark: "#571010", soft: "#eaa5a5" }
  };

  const getRiskKey = (label = "") => {
    const text = label.trim();
    if (text.includes("매우 위험")) return "extreme";
    if (text.includes("위험")) return "danger";
    if (text.includes("경고")) return "warning";
    if (text.includes("주의")) return "caution";
    if (text.includes("안전")) return "normal";
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
      highlight.style.setProperty("--forecast-soft", colors.soft);
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
    applyRiskTheme();
    const observer = new MutationObserver(applyRiskTheme);
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
