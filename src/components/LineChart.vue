<script>
import axios from "axios";
import { Line } from "vue-chartjs";

export default {
  name: "LineChart",
  props: ["apiUrl", "title"],
  extends: Line,
  mounted() {
    axios.get(this.apiUrl).then(response => {
      this.renderChart(
        {
          labels: response.data.labels,
          datasets: response.data.datasets
        },
        {
          responsive: true,
          maintainAspectRatio: false
        }
      );
    });
  }
};
</script>
