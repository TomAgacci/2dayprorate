// chart_config.js
// Global presets + themes for Chart.js

export const ChartThemes = {
    light: {
        fontColor: "#222",
        gridColor: "#ddd",
        background: "#fff"
    },
    dark: {
        fontColor: "#eee",
        gridColor: "#444",
        background: "#111"
    },
    neon: {
        fontColor: "#0ff",
        gridColor: "#0f0",
        background: "#000"
    }
};

export function applyTheme(themeName) {
    const theme = ChartThemes[themeName] || ChartThemes.light;

    Chart.defaults.color = theme.fontColor;
    Chart.defaults.borderColor = theme.gridColor;
    document.body.style.background = theme.background;
}

// Auto‑apply theme based on system preference
export function autoTheme() {
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(prefersDark ? "dark" : "light");
}

// Initialize theme on load
autoTheme();
