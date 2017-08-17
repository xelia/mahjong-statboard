<template>
  <div class="container">
    <h1 class="title">{{ player.name }}</h1>
    <div v-for="stat in player.stats">{{ stat }}</div>
  </div>
</template>
<script>
  import axios from 'axios'
  export default {
    data(){
      return {
        player: {},
      }
    },
    created(){
      this.fetchData()
    },
    watch: {
      '$route': 'fetchData'
    },
    methods: {
      async fetchData(){
        let player = await axios.get(`/api/instances/1/players/${this.$route.params.id}/?format=json&stats=true`)
        this.player = player.data
      }
    }
  }
</script>
