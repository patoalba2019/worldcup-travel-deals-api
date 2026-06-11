document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }

  const services = {
    remotejobs: {
      url: "https://patoapis-remotejobs-api.onrender.com/health",
      detail: (data) => `${data.metadata?.job_count ?? "Available"} jobs ready`,
    },
    worldcup: {
      url: "https://worldcup-travel-deals-api.onrender.com/health",
      detail: (data) => `${data.host_city_count ?? 16} host cities ready`,
    },
    globaldeals: {
      url: "https://global-deal-radar-api.onrender.com/health",
      detail: (data) => `${data.cache?.deal_count ?? "Live"} deal signals ready`,
    },
    omnireply: {
      url: "https://worldcup-travel-deals-api.onrender.com/omni/health",
      detail: (data) => `${data.channels?.length ?? 8} channels ready`,
    },
  };

  document.querySelectorAll("[data-status]").forEach(async (element) => {
    const service = services[element.dataset.status];
    const message = element.querySelector(".status-message");

    if (!service || !message) {
      return;
    }

    try {
      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), 55000);
      const response = await fetch(service.url, {
        cache: "no-store",
        signal: controller.signal,
      });
      window.clearTimeout(timeout);

      if (!response.ok) {
        throw new Error(`Health check returned ${response.status}`);
      }

      const data = await response.json();
      element.classList.add("ready");
      message.textContent = service.detail(data);
    } catch {
      element.classList.add("unavailable");
      message.textContent = "Live status refreshing";
    }
  });
});
