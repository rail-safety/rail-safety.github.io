(() => {
  if (window.__railWeatherLoaderInitialized) return;
  window.__railWeatherLoaderInitialized = true;

  const RAW_WEATHER_URL = "https://raw.githubusercontent.com/rail-safety/rail-safety.github.io/main/weather.json";
  const LOCAL_WEATHER_URL = "weather.json";
  const REFRESH_INTERVAL_MS = 5 * 60 * 1000;

  const fetchJson = async (url, timeoutMs = 12000) => {
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), timeoutMs);
    try {
      const separator = url.includes("?") ? "&" : "?";
      const response = await fetch(`${url}${separator}v=${Date.now()}`, {
        cache: "no-store",
        signal: controller.signal,
        headers: { Accept: "application/json" }
      });
      if (!response.ok) throw new Error(`${url} ${response.status}`);
      return await response.json();
    } finally {
      window.clearTimeout(timeout);
    }
  };

  const fetchLatestWeatherData = async () => {
    try {
      return await fetchJson(RAW_WEATHER_URL);
    } catch (rawError) {
      console.warn("최신 저장소 기상자료 조회 실패, 배포본으로 재시도합니다.", rawError);
      return await fetchJson(LOCAL_WEATHER_URL);
    }
  };

  const applyWeatherData = (data) => {
    const station = data?.stations?.[state.station];
    if (!station?.current || !Array.isArray(station.hourly) || station.hourly.length === 0) {
      throw new Error("역별 기상자료 없음");
    }

    const row = station.current;
    const temp = Number(row.temp);
    const humidity = Number(row.rh);
    const apparent = Number(row.hi);
    if (![temp, humidity, apparent].every(Number.isFinite)) {
      throw new Error("잘못된 실황값");
    }

    state.autoValue = apparent;
    state.autoTemp = temp;
    state.autoRh = humidity;
    state.autoObserved = row.time;
    state.generatedAt = data.generatedAt || Date.now();
    state.hourly = station.hourly.map((item) => ({
      time: item.time,
      temp: Number(item.temp),
      rh: Number(item.rh),
      hi: Number(item.hi)
    }));

    const weatherMeta = document.querySelector("#weatherMeta");
    const headerStatus = document.querySelector("#headerStatus");
    if (weatherMeta) {
      weatherMeta.textContent = "시간별 체감온도 수치가 어느 구간에 해당하는지 보여주는 참고 표시입니다. 기상청 공식 폭염 영향예보는 일 최고 체감온도·지속일수·분야별 영향을 종합해 별도로 발표합니다. 실제 작업 판단은 현장 측정값과 회사 지침을 우선합니다.";
    }
    if (headerStatus) headerStatus.textContent = "기상 연동 정상";

    if (typeof renderHero === "function") renderHero();
    if (typeof renderForecast === "function") renderForecast();
    if (typeof renderGuide === "function") renderGuide();
  };

  const loadLatestWeather = async () => {
    const headerStatus = document.querySelector("#headerStatus");
    if (headerStatus) headerStatus.textContent = "기상 연동 중";

    try {
      const data = await fetchLatestWeatherData();
      applyWeatherData(data);
    } catch (error) {
      console.error("기상자료 갱신 실패", error);

      if (state.autoValue !== null) {
        if (headerStatus) headerStatus.textContent = "기상 갱신 재시도 필요";
        if (typeof renderHero === "function") renderHero();
        if (typeof renderForecast === "function") renderForecast();
        if (typeof renderGuide === "function") renderGuide();
        return;
      }

      state.autoValue = null;
      state.autoTemp = null;
      state.autoRh = null;
      state.autoObserved = null;
      state.hourly = [];
      if (headerStatus) headerStatus.textContent = "기상 연동 확인 필요";

      const weatherMeta = document.querySelector("#weatherMeta");
      if (weatherMeta) {
        weatherMeta.textContent = "기상청 자료를 불러오지 못했습니다. 현장 온·습도계 측정값과 회사 지침을 우선 적용하세요.";
      }
      if (typeof renderHero === "function") renderHero();
      if (typeof renderForecast === "function") renderForecast();
      if (typeof renderGuide === "function") renderGuide();
    }
  };

  window.loadWeather = loadLatestWeather;
  loadWeather = loadLatestWeather;

  window.setTimeout(loadLatestWeather, 250);
  window.setInterval(loadLatestWeather, REFRESH_INTERVAL_MS);

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") loadLatestWeather();
  });
})();
