// charts.js
// Custom wrapper for Chart.js usage in 2dayprorate dashboard

export function createBarChart(ctx, label, data) {
    return new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Maintenance", "Profit", "Eviction (%)"],
            datasets: [{
                label,
                data,
                backgroundColor: ["#0078ff", "#00c853", "#ff5252"]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

export function createLineChart(ctx, cities, maintenance, profit, eviction) {
    return new Chart(ctx, {
        type: "line",
        data: {
            labels: cities,
            datasets: [
                {
                    label: "Maintenance",
                    data: maintenance,
                    borderColor: "#0078ff",
                    fill: false
                },
                {
                    label: "Profit",
                    data: profit,
                    borderColor: "#00c853",
                    fill: false
                },
                {
                    label: "Eviction (%)",
                    data: eviction,
                    borderColor: "#ff5252",
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}
