<template>
  <span><span v-for="place in series.series">{{ place }}</span></span>
</template>
<script>
  export default {
    props: ['series']
  }
</script>
