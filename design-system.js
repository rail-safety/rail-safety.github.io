(() => {
  const heroCardStyles = document.createElement("link");
  heroCardStyles.rel = "stylesheet";
  heroCardStyles.href = "hero-card.css?v=a631c706d633";
  heroCardStyles.dataset.designComponent = "hero-card";
  document.head.append(heroCardStyles);

  const statusTokens = {
    brand: {
      surface: "var(--brand-surface)",
      border: "var(--brand-border)",
      text: "var(--brand-text)",
      solid: "var(--brand-solid)",
      accent: "var(--brand-accent)"
    },
    safe: {
      surface: "var(--safe-surface)",
      border: "var(--safe-border)",
      text: "var(--safe-text)",
      solid: "var(--safe-solid)",
      accent: "var(--safe-accent)"
    },
    caution: {
      surface: "var(--caution-surface)",
      border: "var(--caution-border)",
      text: "var(--caution-text)",
      solid: "var(--caution-solid)",
      accent: "var(--caution-accent)"
    },
    warning: {
      surface: "var(--warning-surface)",
      border: "var(--warning-border)",
      text: "var(--warning-text)",
      solid: "var(--warning-solid)",
      accent: "var(--warning-accent)"
    },
    danger: {
      surface: "var(--danger-surface)",
      border: "var(--danger-border)",
      text: "var(--danger-text)",
      solid: "var(--danger-solid)",
      accent: "var(--danger-accent)"
    }
  };

  const levelKeyToStatus = {
    normal: "safe",
    interest: "safe",
    caution: "caution",
    warning: "warning",
    danger: "danger"
  };

  const statusFromText = (value = "") => {
    const text = String(value);
    if (text.includes("위험")) return "danger";
    if (text.includes("경고")) return "warning";
    if (text.includes("주의") || text.includes("갱신 지연")) return "caution";
    if (text.includes("관심") || text.includes("미만")) return "safe";
    return "brand";
  };

  const statusFromLevel = (level) => {
    if (level?.key && levelKeyToStatus[level.key]) return levelKeyToStatus[level.key];
    return statusFromText(level?.name || "");
  };

  const setImportant = (target, property, value) => {
    target?.style.setProperty(property, value, "important");
  };

  const applyHeroStatus = () => {
    const hero = document.querySelector(".hero");
    const badge = document.querySelector("#currentBadge");
    if (!hero || !badge) return;

    const status = statusFromText(badge.textContent);
    const token = statusTokens[status];
    hero.dataset.riskLevel = status;
    setImportant(hero, "--hero-surface", token.surface);
    setImportant(hero, "--hero-border", token.border);
    setImportant(hero, "--hero-text", token.text);
    setImportant(hero, "--hero-solid", token.solid);
    setImportant(hero, "--hero-accent", token.accent);
  };

  const applyGuideStatus = (level) => {
    const root = document.documentElement;
    const status = level ? statusFromLevel(level) : statusFromText(document.querySelector("#guideStatus")?.textContent || "");
    const token = statusTokens[status];

    setImportant(root, "--risk", token.solid);
    setImportant(root, "--risk-dark", token.accent);
    setImportant(root, "--risk-soft", token.surface);
    setImportant(root, "--risk-border", token.border);

    const dot = document.querySelector("#guideLevelDot");
    if (dot) {
      dot.style.background = token.solid;
      dot.style.boxShadow = "none";
    }
  };

  if (typeof levels !== "undefined" && Array.isArray(levels)) {
    levels.forEach((level) => {
      const status = levelKeyToStatus[level.key] || "brand";
      const token = statusTokens[status];
      level.color = token.solid;
      level.dark = token.accent;
      level.soft = token.surface;
      level.border = token.border;
      level.text = token.text;
    });
  }

  if (typeof applyGuideTheme === "function") {
    applyGuideTheme = function applyTokenGuideTheme(level) {
      applyGuideStatus(level);
    };
  }

  const refreshDynamicUI = () => {
    if (typeof renderHero === "function") renderHero();
    if (typeof renderForecast === "function") renderForecast();
    if (typeof renderGuide === "function") renderGuide();
    applyHeroStatus();
    applyGuideStatus();
  };

  const observeText = (selector, callback) => {
    const target = document.querySelector(selector);
    if (!target) return;
    new MutationObserver(callback).observe(target, {
      childList: true,
      subtree: true,
      characterData: true
    });
  };

  observeText("#currentBadge", applyHeroStatus);
  observeText("#guideStatus", () => applyGuideStatus());

  refreshDynamicUI();
})();
