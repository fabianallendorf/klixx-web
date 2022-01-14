<template>
  <tr>
    <td v-for="(data, index) in rowData" :key="index">{{ data }}</td>
  </tr>
</template>
<script>
export default {
  name: "TableRow",
  props: ["rowData"]
};
</script>
