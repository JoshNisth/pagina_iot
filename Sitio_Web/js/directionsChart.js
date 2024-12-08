document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("directionsChart").getContext("2d");
  let directionsChart;

  function fetchAndRenderData() {
      fetch("php/getDirectionsData.php")
          .then(response => response.json())
          .then(data => {
              if (directionsChart) directionsChart.destroy();

              directionsChart = new Chart(ctx, {
                  type: "bar",
                  data: {
                      labels: data.labels,
                      datasets: [{
                          label: "Cantidad por Dirección",
                          data: data.values,
                          backgroundColor: "#36A2EB",
                          borderColor: "#0369A1",
                          borderWidth: 1,
                      }]
                  },
                  options: {
                      responsive: true,
                      scales: {
                          y: {
                              beginAtZero: true,
                              title: {
                                  display: true,
                                  text: "Cantidad"
                              }
                          },
                          x: {
                              title: {
                                  display: true,
                                  text: "Direcciones"
                              }
                          }
                      },
                      plugins: {
                          legend: {
                              display: false
                          }
                      }
                  }
              });
          })
          .catch(error => console.error("Error al cargar datos:", error));
  }

  // Cargar datos inicialmente
  fetchAndRenderData();

  // Actualizar datos cada 5 segundos
  setInterval(fetchAndRenderData, 5000);
});
