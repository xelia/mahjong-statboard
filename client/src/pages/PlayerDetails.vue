<template>
  <div>
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            {{ player.name }}
          </h1>
          <h2 class="subtitle">
            {{ player.full_name }}
          </h2>
        </div>
      </div>
    </section>
    <section>
      <div class="container">
        <b-tabs type="is-boxed">
          <b-tab-item v-for="(stat, rating_id) in player.stats" :label="rating_id" :key="rating_id">
            {{ stat }}
          </b-tab-item>
        </b-tabs>
      </div>
    </section>
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
