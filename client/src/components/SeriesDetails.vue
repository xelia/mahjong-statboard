<template>
  <b-tooltip :label="`${series.start_date} - ${series.end_date}`" position="is-top" type="is-light">
    <span class="series-details">
      <span v-for="(place, index) in series.series" :key="index">{{ place }}</span>
    </span>
  </b-tooltip>
</template>
<script>
  export default {
    props: ['series']
  }
</script>
<style scoped>
  .series-details {
    padding-left: 0.5em;
  }
</style>
