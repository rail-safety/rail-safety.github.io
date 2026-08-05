(() => {
  const button = document.querySelector("#refreshWeather");
  const status = document.querySelector("#headerStatus");
  if (!button) return;

  const label = button.querySelector(".hero__refresh-label");
  button.hidden = false;
  button.setAttribute("aria-label", "페이지 전체 새로고침");

  button.addEventListener("click", () => {
    if (button.disabled) return;

    button.disabled = true;
    button.classList.add("is-loading");
    button.setAttribute("aria-busy", "true");
    if (label) label.textContent = "새로고침 중";
    if (status) status.textContent = "페이지 전체 새로고침 중";

    window.setTimeout(() => {
      window.location.reload();
    }, 80);
  });
})();
