<template>
  <button v-bind:class="buttonClass" @click="$emit('toggle')">
    Farbkorrektur Sehschwäche
  </button>
</template>
<script>
export default {
  name: "ColorCorrectioButton",
  props: ["colorBlindMode"],
  computed: {
    buttonClass: function () {
      if (this.colorBlindMode) {
        return "button-primary";
      } else {
        return "button";
      }
    },
  },
};
</script>
