$(function () {
  "use strict";

  // Variables pour stocker les graphiques
  var barChartEncaissement, barChartDecaissement;

  // Récupérer les inputs année
  var $anneeEncaissement = $('.col-lg-6:first input[type="number"]');
  var $anneeDecaissement = $('.col-lg-6:last input[type="number"]');

  // Valeur par défaut (année courante)
  var currentYear = new Date().getFullYear();
  $anneeEncaissement.val(currentYear);
  $anneeDecaissement.val(currentYear);

  var clientPieData = {
    datasets: [
      {
        data: [20000, 21120, 15000],
        backgroundColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
        ],
        borderColor: [
          "rgba(255,99,132,1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
        ],
      },
    ],
    labels: ["L’Oréal", "TotalEnergies", "BNP Paribas"],
  };

  var clientPieOptions = {
    responsive: true,
    animation: {
      animateScale: true,
      animateRotate: true,
    },
    legend: {
      display: false,
    },
    cutoutPercentage: 60,
    legendCallback: function (chart) {
      var total = chart.data.datasets[0].data.reduce(function (acc, val) {
        return acc + val;
      }, 0);
      var text = [];
      text.push('<div class="report-chart">');
      chart.data.labels.forEach(function (label, index) {
        text.push(
          '<div class="d-flex justify-content-between mx-4 mx-xl-5 mt-3">',
        );
        text.push('<div class="d-flex align-items-center">');
        text.push(
          '<div class="mr-3" style="width:20px; height:20px; border-radius:50%; background-color:' +
            chart.data.datasets[0].backgroundColor[index] +
            '"></div>',
        );
        text.push('<p class="mb-0">' + label + "</p>");
        text.push("</div>");
        text.push(
          '<p class="mb-0">' +
            ((chart.data.datasets[0].data[index] / total) * 100).toFixed(2) +
            " %</p>",
        );

        text.push("</div>");
      });
      text.push("</div>");
      return text.join("");
    },
  };

  var clientChartPlugins = {
    beforeDraw: function (chart) {
      var width = chart.chart.width,
        height = chart.chart.height,
        ctx = chart.chart.ctx;

      ctx.restore();
      var fontSize = 3.125;
      ctx.font = "500 " + fontSize + "em sans-serif";
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#13381B";

      var text = chart.data.datasets[0].data.reduce(function (acc, val) {
          return acc + val;
        }, 0),
        textX = Math.round((width - ctx.measureText(text).width) / 2),
        textY = height / 2;

      ctx.fillText(text, textX, textY);
      ctx.save();
    },
  };

  if ($("#clientChart").length) {
    var clientChartCanvas = $("#clientChart").get(0).getContext("2d");
    var clientChart = new Chart(clientChartCanvas, {
      type: "doughnut",
      data: clientPieData,
      options: clientPieOptions,
      plugins: clientChartPlugins,
    });

    // Inject custom legend
    document.getElementById("clientChartLegend").innerHTML =
      clientChart.generateLegend();
  }

  var fournisseurPieData = {
    datasets: [
      {
        data: [12000, 15000, 18000], // Montants réalistes pour chaque fournisseur
        backgroundColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
        ],
        borderColor: [
          "rgba(255,99,132,1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
        ],
      },
    ],
    labels: ["Air Liquide", "Veolia", "Saint-Gobain"], // Fournisseurs français réalistes
  };

  var fournisseurPieOptions = {
    responsive: true,
    animation: {
      animateScale: true,
      animateRotate: true,
    },
    legend: {
      display: false,
    },
    cutoutPercentage: 60,
    legendCallback: function (chart) {
      var total = chart.data.datasets[0].data.reduce(function (acc, val) {
        return acc + val;
      }, 0);
      var text = [];
      text.push('<div class="report-chart">');
      chart.data.labels.forEach(function (label, index) {
        text.push(
          '<div class="d-flex justify-content-between mx-4 mx-xl-5 mt-3">',
        );
        text.push('<div class="d-flex align-items-center">');
        text.push(
          '<div class="mr-3" style="width:20px; height:20px; border-radius:50%; background-color:' +
            chart.data.datasets[0].backgroundColor[index] +
            '"></div>',
        );
        text.push('<p class="mb-0">' + label + "</p>");
        text.push("</div>");
        text.push(
          '<p class="mb-0">' +
            ((chart.data.datasets[0].data[index] / total) * 100).toFixed(2) +
            " %</p>",
        );
        text.push("</div>");
      });
      text.push("</div>");
      return text.join("");
    },
  };

  var fournisseurChartPlugins = {
    beforeDraw: function (chart) {
      var width = chart.chart.width,
        height = chart.chart.height,
        ctx = chart.chart.ctx;

      ctx.restore();
      var fontSize = 3.125;
      ctx.font = "500 " + fontSize + "em sans-serif";
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#13381B";

      var text = chart.data.datasets[0].data.reduce(function (acc, val) {
          return acc + val;
        }, 0),
        textX = Math.round((width - ctx.measureText(text).width) / 2),
        textY = height / 2;

      ctx.fillText(text, textX, textY);
      ctx.save();
    },
  };

  if ($("#fournisseurChart").length) {
    var fournisseurChartCanvas = $("#fournisseurChart").get(0).getContext("2d");
    var fournisseurChart = new Chart(fournisseurChartCanvas, {
      type: "doughnut",
      data: fournisseurPieData,
      options: fournisseurPieOptions,
      plugins: fournisseurChartPlugins,
    });

    // Inject custom legend
    document.getElementById("fournisseurChartLegend").innerHTML =
      fournisseurChart.generateLegend();
  }

  var optionsEncaissement = {
    scales: {
      yAxes: [
        {
          display: true,
          gridLines: {
            display: true,
            drawBorder: false,
            color: "#F2F2F2",
          },
          ticks: {
            display: true,
            min: 0,
            // max: 560,
            callback: function (value, index, values) {
              return value + " €";
            },
            autoSkip: true,
            maxTicksLimit: 10,
            fontColor: "#6C7383",
          },
        },
      ],
    },
    legend: {
      display: false,
    },
    elements: {
      point: {
        radius: 0,
      },
    },
  };

  var optionsDecaissement = {
    scales: {
      yAxes: [
        {
          display: true,
          gridLines: {
            display: true,
            drawBorder: false,
            color: "#F2F2F2",
          },
          ticks: {
            display: true,
            min: 0,
            // max: 560,
            callback: function (value, index, values) {
              return value + " €";
            },
            autoSkip: true,
            maxTicksLimit: 10,
            fontColor: "#6C7383",
          },
        },
      ],
    },
    legend: {
      display: false,
    },
    elements: {
      point: {
        radius: 0,
      },
    },
  };

  // Fonction pour charger toutes les données (encaissement et décaissement)
  function loadAllData(year) {
    if (year.toString().length !== 4) return;

    fetch(`/forecast/forecast_financial_data/?year=${year}`)
      .then((response) => response.json())
      .then((data) => {
        // Mettre à jour l'encaissement
        if ($("#barChartEncaissement").length) {
          var dataEncaissement = {
            labels: [
              "Jan",
              "Feb",
              "Mar",
              "Avr",
              "Mai",
              "Juin",
              "Juil",
              "Aoû",
              "Sep",
              "Oct",
              "Nov",
              "Déc",
            ],
            datasets: [
              {
                label: "Prévision",
                data: data.encaissement_prevision,
                backgroundColor: "rgba(255, 99, 132, 1)",
              },
              {
                label: "Réel",
                data: data.encaissement_reel,
                backgroundColor: "rgba(255, 159, 64, 1)",
              },
            ],
          };

          if (barChartEncaissement) {
            barChartEncaissement.destroy();
          }

          var barChartEncaissementCanvas = $("#barChartEncaissement")
            .get(0)
            .getContext("2d");
          barChartEncaissement = new Chart(barChartEncaissementCanvas, {
            type: "bar",
            data: dataEncaissement,
            options: optionsEncaissement,
          });
          document.getElementById("encaissement-legend").innerHTML =
            barChartEncaissement.generateLegend();
        }

        // Mettre à jour le décaissement
        if ($("#barChartDecaissement").length) {
          var dataDecaissement = {
            labels: [
              "Jan",
              "Feb",
              "Mar",
              "Avr",
              "Mai",
              "Juin",
              "Juil",
              "Aoû",
              "Sep",
              "Oct",
              "Nov",
              "Déc",
            ],
            datasets: [
              {
                label: "Prévision",
                data: data.decaissement_prevision,
                backgroundColor: "rgba(255, 99, 132, 1)",
              },
              {
                label: "Réel",
                data: data.decaissement_reel,
                backgroundColor: "rgba(255, 159, 64, 1)",
              },
            ],
          };

          if (barChartDecaissement) {
            barChartDecaissement.destroy();
          }

          var barChartDecaissementCanvas = $("#barChartDecaissement")
            .get(0)
            .getContext("2d");
          barChartDecaissement = new Chart(barChartDecaissementCanvas, {
            type: "bar",
            data: dataDecaissement,
            options: optionsDecaissement,
          });
          document.getElementById("decaissement-legend").innerHTML =
            barChartDecaissement.generateLegend();
        }
      });
  }

  // Fonction pour charger les données d'encaissement
  function loadEncaissementData(year) {
    if (year.toString().length !== 4) return;

    fetch(`/forecast/forecast_financial_data/?year=${year}`)
      .then((response) => response.json())
      .then((data) => {
        var dataEncaissement = {
          labels: [
            "Jan",
            "Feb",
            "Mar",
            "Avr",
            "Mai",
            "Juin",
            "Juil",
            "Aoû",
            "Sep",
            "Oct",
            "Nov",
            "Déc",
          ],
          datasets: [
            {
              label: "Prévision",
              data: data.encaissement_prevision,
              backgroundColor: "rgba(255, 99, 132, 1)",
            },
            {
              label: "Réel",
              data: data.encaissement_reel,
              backgroundColor: "rgba(255, 159, 64, 1)",
            },
          ],
        };

        if ($("#barChartEncaissement").length) {
          // Détruire l'ancien graphique s'il existe
          if (barChartEncaissement) {
            barChartEncaissement.destroy();
          }

          var barChartEncaissementCanvas = $("#barChartEncaissement")
            .get(0)
            .getContext("2d");
          barChartEncaissement = new Chart(barChartEncaissementCanvas, {
            type: "bar",
            data: dataEncaissement,
            options: optionsEncaissement,
          });
          document.getElementById("encaissement-legend").innerHTML =
            barChartEncaissement.generateLegend();
        }
      });
  }

  // Fonction pour charger les données de décaissement
  function loadDecaissementData(year) {
    if (year.toString().length !== 4) return;

    fetch(`/forecast/forecast_financial_data/?year=${year}`)
      .then((response) => response.json())
      .then((data) => {
        var dataDecaissement = {
          labels: [
            "Jan",
            "Feb",
            "Mar",
            "Avr",
            "Mai",
            "Juin",
            "Juil",
            "Aoû",
            "Sep",
            "Oct",
            "Nov",
            "Déc",
          ],
          datasets: [
            {
              label: "Prévision",
              data: data.decaissement_prevision,
              backgroundColor: "rgba(255, 99, 132, 1)",
            },
            {
              label: "Réel",
              data: data.decaissement_reel,
              backgroundColor: "rgba(255, 159, 64, 1)",
            },
          ],
        };

        if ($("#barChartDecaissement").length) {
          // Détruire l'ancien graphique s'il existe
          if (barChartDecaissement) {
            barChartDecaissement.destroy();
          }

          var barChartDecaissementCanvas = $("#barChartDecaissement")
            .get(0)
            .getContext("2d");
          barChartDecaissement = new Chart(barChartDecaissementCanvas, {
            type: "bar",
            data: dataDecaissement,
            options: optionsDecaissement,
          });
          document.getElementById("decaissement-legend").innerHTML =
            barChartDecaissement.generateLegend();
        }
      });
  }

  // Événement sur l'input encaissement
  $anneeEncaissement.on("input", function () {
    var year = $(this).val();
    if (year.length === 4) {
      loadEncaissementData(year);
    }
  });

  // Événement sur l'input décaissement
  $anneeDecaissement.on("input", function () {
    var year = $(this).val();
    if (year.length === 4) {
      loadDecaissementData(year);
    }
  });

  // Charger les données initiales
  loadAllData(currentYear);
});
