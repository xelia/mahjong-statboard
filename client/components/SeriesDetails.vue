<template>
  <span>{{ series.avg_place }}/{{ series.score_sum }} <span v-for="place in series.series">{{ place }}</span></span>
</template>
<script>
  export default {
    props: ['series']
  }
</script>
