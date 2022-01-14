<template>
  <canvas :id="chartId" :height="height" :width="width"></canvas>
</template>
<script>
import { Chart } from "chart.js";

export default {
  name: "ScatterChart",
  props: {
    height: {
      type: Number,
      required: false,
      default: 500,
    },
    width: {
      type: Number,
      required: false,
      default: 500,
    },
    scales: {
      type: Object,
      required: false,
      default: {},
    },
    db: {
      type: Object,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
    backgroundColor: {
      type: Array[String],
      required: false,
      default: Chart.defaults.backgroundColor,
    },
  },
  data() {
    this.chart = null;
    return {
      chartId: Math.random().toString(36).slice(-5),
      chartData: {},
      options: {
        plugins: {
          legend: false,
          title: { text: "Schätzungen", display: true },
        },
      },
      shownBefore: false,
      firstBets: [],
    };
  },
  watch: {
    backgroundColor: function () {
      for (let index = 0; index < this.firstBets.length; index++) {
        this.chartData.datasets[0].pointBackgroundColor[index] =
          this.firstBets[index] === "x"
            ? this.backgroundColor[0]
            : this.backgroundColor[1];
      }
      this.chart.update();
    },
    show: function () {
      if (this.show && !this.shownBefore) {
        this.shownBefore = true;
      }
    },
  },
  created() {
    this.options.scales = this.scales;
    const statement = this.db.prepare(
      "SELECT data from klixx where type=(SELECT id from types WHERE value=?) ORDER BY created DESC LIMIT 1",
      [this.type]
    );
    statement.step();
    let initialChartData = JSON.parse(statement.get()[0]);
    this.firstBets = [...initialChartData.firstBets];
    this.chartData = initialChartData;
    this.chartData.datasets[0].pointBackgroundColor = [];
    for (let index = 0; index < this.firstBets.length; index++) {
      this.chartData.datasets[0].pointBackgroundColor[index] =
        this.firstBets[index] === "x"
          ? this.backgroundColor[0]
          : this.backgroundColor[1];
    }
  },
  mounted() {
    const chartElement = document.getElementById(this.chartId);
    delete this.chartData.datasets[0].label;
    this.chart = new Chart(chartElement, {
      type: "scatter",
      data: this.chartData,
      options: this.options,
    });
  },
};
</script>
