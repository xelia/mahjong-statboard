<template>
    <span>
      <span v-if="value">
        <span v-if="rating.is_series">
          <span v-if="series === 'best'">{{ value.best.avg_place }} / {{ value.best.score_sum }}</span>
          <span v-else>{{ value.current.avg_place }} / {{ value.current.score_sum }}</span>
        </span>
        <span v-else>{{ value }}</span>
      </span>
    </span>
</template>

<script>
  export default {
    props: {
      'rating': {},
      'value': {},
      'series': {default: 'best'}
    },
  }
</script>
