(() => {
  const button = document.querySelector("#refreshWeather");
  const source = document.querySelector("#heroSource");
  const status = document.querySelector("#headerStatus");
  if (!button || !source || typeof loadWeather !== "function") return;

  const label = button.querySelector(".hero__refresh-label");
  let resetTimer;

  const syncVisibility = () => {
    button.hidden = source.textContent.trim() !== "기상청 실황";
  };

  new MutationObserver(syncVisibility).observe(source, {
    childList: true,
    characterData: true,
    subtree: true
  });
  syncVisibility();

  button.addEventListener("click", async () => {
    if (button.disabled) return;

    clearTimeout(resetTimer);
    button.disabled = true;
    button.classList.add("is-loading");
    button.setAttribute("aria-busy", "true");
    label.textContent = "갱신 중";
    if (status) status.textContent = "기상정보 수동 갱신 중";

    await loadWeather();

    const succeeded = status?.textContent === "기상 연동 정상";
    label.textContent = succeeded ? "갱신 완료" : "다시 시도";
    button.classList.remove("is-loading");
    button.removeAttribute("aria-busy");
    button.disabled = false;

    resetTimer = window.setTimeout(() => {
      label.textContent = "새로고침";
    }, 1400);
  });
})();
