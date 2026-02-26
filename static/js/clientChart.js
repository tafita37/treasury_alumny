$(function () {
  /* ChartJS
   * -------
   * Data and config for chartjs
   */
  "use strict";
  var dataJour = {
    labels: [
      "Jan",
      "Fév",
      "Mar",
      "Avr",
      "Mai",
      "Juin",
      "Juil",
      "Aou",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
    datasets: [
      {
        label: "Nombre de jours",
        data: [10, 19, 3, 5, 2, 3, 12, 8, 15, 6, 9, 14],
        backgroundColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
          "rgba(199, 199, 199, 1)",
          "rgba(83, 102, 255, 1)",
          "rgba(255, 99, 255, 1)",
          "rgba(99, 255, 132, 1)",
          "rgba(255, 159, 200, 1)",
          "rgba(120, 200, 150, 1)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
          "rgba(199, 199, 199, 1)",
          "rgba(83, 102, 255, 1)",
          "rgba(255, 99, 255, 1)",
          "rgba(99, 255, 132, 1)",
          "rgba(255, 159, 200, 1)",
          "rgba(120, 200, 150, 1)",
        ],
        borderWidth: 1,
        fill: false,
      },
    ],
  };

  var dataMontant = {
    labels: [
      "Jan",
      "Fév",
      "Mar",
      "Avr",
      "Mai",
      "Juin",
      "Juil",
      "Aou",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
    datasets: [
      {
        label: "Montant",
        data: [1000, 1900, 300, 500, 200, 300, 1200, 800, 1500, 600, 900, 1400],
        backgroundColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
          "rgba(199, 199, 199, 1)",
          "rgba(83, 102, 255, 1)",
          "rgba(255, 99, 255, 1)",
          "rgba(99, 255, 132, 1)",
          "rgba(255, 159, 200, 1)",
          "rgba(120, 200, 150, 1)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
          "rgba(199, 199, 199, 1)",
          "rgba(83, 102, 255, 1)",
          "rgba(255, 99, 255, 1)",
          "rgba(99, 255, 132, 1)",
          "rgba(255, 159, 200, 1)",
          "rgba(120, 200, 150, 1)",
        ],
        borderWidth: 1,
        fill: false,
      },
    ],
  };

  var options = {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
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
  // Get context with jQuery - using jQuery's .get() method.
  if ($("#clientJourBarChart").length) {
    var clientJourBarChartCanvas = $("#clientJourBarChart")
      .get(0)
      .getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var clientJourBarChart = new Chart(clientJourBarChartCanvas, {
      type: "bar",
      data: dataJour,
      options: options,
    });
  }

  if ($("#clientMontantBarChart").length) {
    var clientMontantBarChartCanvas = $("#clientMontantBarChart")
      .get(0)
      .getContext("2d");
    // This will get the first returned node in the jQuery collection.
    var clientMontantBarChart = new Chart(clientMontantBarChartCanvas, {
      type: "bar",
      data: dataMontant,
      options: options,
    });
  }
});
