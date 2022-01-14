import { createApp } from "vue";
import App from "./App.vue";
import Chart from "chart.js/auto";
// chart.js defaults
// https://www.chartjs.org/docs/latest/api/interfaces/Defaults.html
Chart.defaults.font.size = 18;
Chart.defaults.font.family =
  '"Raleway", "HelveticaNeue", "Helvetica Neue","Helvetica", "Arial", "sans-serif"';
Chart.defaults.backgroundColor = ["#B782A2", "#66748C", "#D3BD94"];

createApp(App).mount("#app");
