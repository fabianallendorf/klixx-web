<template>
  <span>
    <h5>Aktueller Stand: {{ createdFormatted }}</h5>
  </span>
</template>

<script>
import { DateTime } from "luxon";

export default {
  name: "Title",
  data() {
    return {
      created: DateTime.now(),
    };
  },
  props: {
    db: {
      type: Object,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
  },
  computed: {
    createdFormatted: function () {
      return this.created.toLocaleString(DateTime.DATETIME_MED);
    },
  },
  created() {
    const statement = this.db.prepare(
      "SELECT created from klixx ORDER BY created DESC LIMIT 1"
    );
    statement.step();
    this.created = DateTime.fromSQL(statement.get()[0]);
  },
};
</script>
