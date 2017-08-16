<template>
    <span>
      <span v-if="value">
        <span v-if="rating.is_series">{{ value.avg_place }} / {{ value.score_sum }} </span>
        <span v-else>{{ value }}</span>
      </span>
    </span>
</template>

<script>
  export default {
    props: ['rating', 'value'],
  }
</script>
