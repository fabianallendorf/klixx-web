<template>
  <table class="u-full-width">
    <thead>
      <tr>
        <th v-for="header in tableData.columns" :key="header">{{ header }}</th>
      </tr>
    </thead>
    <tbody>
      <TableRow v-for="row in tableData.data" :key="row.id" :rowData="row" />
    </tbody>
  </table>
</template>

<script>
import TableRow from "./TableRow.vue";

export default {
  name: "Table",
  components: { TableRow },
  data() {
    return {
      tableData: { columns: [], data: [] }
    };
  },
  props: {
    db: {
      type: Object,
      required: true
    },
    type: {
      type: String,
      required: true
    }
  },
  mounted() {
    const statement = this.db.prepare(
      "SELECT data from klixx where type=(SELECT id from types WHERE value=?) ORDER BY created DESC LIMIT 1",
      [this.type]
    );
    statement.step();
    this.tableData = JSON.parse(statement.get()[0]);
  }
};
</script>
