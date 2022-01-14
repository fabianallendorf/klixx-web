<template>
  <canvas :id="chartId" :width="width" :height="height"></canvas>
</template>
<script>
import Chart from "chart.js/auto";

export default {
  name: "DoughnutChart",
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
    },
    show: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  data() {
    this.chart = null;
    return {
      chartId: Math.random().toString(36).slice(-5),
      chartData: {},
      options: { maintainAspectRatio: false },
      shownBefore: false,
    };
  },
  created() {
    const statement = this.db.prepare(
      "SELECT data from klixx where type=(SELECT id from types WHERE value=?) ORDER BY created DESC LIMIT 1",
      [this.type]
    );
    statement.step();
    this.chartData = JSON.parse(statement.get()[0]);
  },
  mounted() {
    let context = document.getElementById(this.chartId);
    this.chart = new Chart(context, {
      type: "doughnut",
      data: { ...this.chartData },
      options: { ...this.options },
    });
  },
  watch: {
    show: function () {
      if (this.show && !this.shownBefore) {
        this.shownBefore = true;
      }
    },
    backgroundColor: function () {
      for (let index = 0; index < this.chartData.datasets.length; index++) {
        this.chartData.datasets[index].backgroundColor = this.backgroundColor;
      }
      this.chart.update();
    },
  },
};
</script>
