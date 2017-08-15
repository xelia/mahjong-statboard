<template>
  <div class="container">
    <h1 class="title">{{ player.name }}</h1>
    <div v-for="stat in player.stats">{{ stat }}</div>
  </div>

</template>
<script>
  export default {
    async asyncData({app, params}){
      let player = await app.$axios.get(`/instances/1/players/${params.id}/?format=json&stats=true`)
      return {
        player: player.data
      }
    },
    data(){
      return {
        player: null,
      }
    }
  }
</script>
