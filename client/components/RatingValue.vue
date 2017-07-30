<template>
  <div>
    <span v-for="place in bestSeriesPlaces">{{ place }}</span>
  </div>
</template>

<script>
  export default {
    props: ['rating', 'value'],
    computed: {
      bestSeriesPlaces() {
        if(!this.value){
          return []
        }
        if(!this.value.value){
          return []
        }
        return this.value.value.best.series
      }
    }
  }
</script>
