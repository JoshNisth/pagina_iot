const filterProfile = document.getElementById("filterProfile");
const filterUser = document.getElementById("filterUser");
const filterDate = document.getElementById("filterDate");
const applyFiltersButton = document.getElementById("applyFilters");

let userChart, profileExcessChart, profileChart, realTimeChart;

function loadFilters() {
    fetch("php/getFilters.php")
        .then(response => response.json())
        .then(data => {
            data.profiles.forEach(profile => {
                filterProfile.innerHTML += `<option value="${profile.id}">${profile.name}</option>`;
            });
            data.users.forEach(user => {
                filterUser.innerHTML += `<option value="${user.id}">${user.name}</option>`;
            });
        });
}

function loadMetrics(filters) {
    fetch(`php/getMetrics.php?filters=${encodeURIComponent(JSON.stringify(filters))}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("mostActiveUser").querySelector("p").textContent = `${data.mostActiveUser.name} (${data.mostActiveUser.percentage}%)`;
            document.getElementById("mostPopularProfile").querySelector("p").textContent = `${data.mostPopularProfile.name} (${data.mostPopularProfile.percentage}%)`;
        });
}

function loadCharts(filters) {
    // Registros por Usuario
    fetch(`php/getChartsData.php?action=getUserChart&filters=${encodeURIComponent(JSON.stringify(filters))}`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById("userChart").getContext("2d");
            if (userChart) userChart.destroy();
            userChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: "Registros por Usuario",
                        data: data.values,
                        backgroundColor: "#36A2EB"
                    }]
                }
            });
        });

    // Excesos de Límite por Perfil
    fetch(`php/getChartsData.php?action=getProfileExcessChart&filters=${encodeURIComponent(JSON.stringify(filters))}`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById("profileExcessChart").getContext("2d");
            if (profileExcessChart) profileExcessChart.destroy();
            profileExcessChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: "Excesos de Límite por Perfil",
                        data: data.values,
                        backgroundColor: "#FF6384"
                    }]
                }
            });
        });

    // Registros por Perfil
    fetch(`php/getChartsData.php?action=getProfileChart&filters=${encodeURIComponent(JSON.stringify(filters))}`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById("profileChart").getContext("2d");
            if (profileChart) profileChart.destroy();
            profileChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: "Registros por Perfil",
                        data: data.values,
                        backgroundColor: "#4BC0C0"
                    }]
                }
            });
        });
}

function loadRealTimeChart() {
    const ctx = document.getElementById("realTimeChart").getContext("2d");

    if (!realTimeChart) {
        realTimeChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: [],
                datasets: [{
                    label: "Niveles de Ruido",
                    data: [],
                    borderColor: "rgba(75, 192, 192, 1)",
                    backgroundColor: "rgba(75, 192, 192, 0.2)"
                }]
            }
        });
    }

    // Cargar datos iniciales de tiempo real
    fetch("php/getRealTimeData.php")
        .then(response => response.json())
        .then(data => {
            realTimeChart.data.labels = data.timestamps;
            realTimeChart.data.datasets[0].data = data.values;
            realTimeChart.update();
        });

    // Actualizar cada 5 segundos
    setInterval(() => {
        fetch("php/getRealTimeData.php")
            .then(response => response.json())
            .then(data => {
                realTimeChart.data.labels = data.timestamps;
                realTimeChart.data.datasets[0].data = data.values;
                realTimeChart.update();
            });
    }, 5000);
}

document.addEventListener("DOMContentLoaded", () => {
    loadFilters();

    const initialFilters = {
        profile: filterProfile.value,
        user: filterUser.value,
        date: filterDate.value,
    };

    loadMetrics(initialFilters);
    loadCharts(initialFilters);
    loadRealTimeChart();

    applyFiltersButton.addEventListener("click", () => {
        const filters = {
            profile: filterProfile.value,
            user: filterUser.value,
            date: filterDate.value,
        };

        loadMetrics(filters);
        loadCharts(filters);
    });
});
