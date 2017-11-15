<template>
  <b-table
    :data="opponents"
    :narrowed="true"
    :mobileCards="false"
    :loading="loading"
  >
    <template slot-scope="props">
      <b-table-column label="Игрок">
        <router-link :to="`/player/${props.row.player.id}`">{{ props.row.player.name }}</router-link>
      </b-table-column>
      <b-table-column label="Игр">
        {{ props.row.wins + props.row.losses }}
      </b-table-column>
      <b-table-column label="Побед">
        {{ props.row.wins }}
      </b-table-column>
      <b-table-column label="Поражений">
        {{ props.row.losses }}
      </b-table-column>
    </template>
  </b-table>
</template>

<script>
  import axios from 'axios'
  export default {
    props: ['player'],
    data() {
      return {
        opponents: [],
        loading: false
      }
    },
    mounted(){
      this.fetchData()
    },
    watch:{
      'player': 'fetchData'
    },
    methods: {
      async fetchData() {
        this.loading = true
        let res = await axios.get(`/api/instances/${this.$store.state.instance.id}/players/${this.player.id}/opponents/`)
        this.opponents = res.data
        this.loading = false
      },
    }
  }
</script>
