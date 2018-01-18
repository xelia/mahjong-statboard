<template>
  <b-tooltip :label="`${series.start_date} - ${series.end_date}`" position="is-right" type="is-light">
    <span><span v-for="place in series.series">{{ place }}</span></span>
  </b-tooltip>
</template>
<script>
  export default {
    props: ['series']
  }
</script>
