<template>
    <span v-if="value">
      <span v-if="rating.is_series">{{ value.best.avg_place }} / {{ value.best.score_sum }} </span>
      <span v-else>{{ value.value }}</span>
    </span>
</template>

<script>
  export default {
    props: ['rating', 'value'],
  }
</script>
