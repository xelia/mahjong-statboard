<template>
  <div class="container">
    <h1 class="title">{{ rating.name }}</h1>
    <b-table :data="filteredPlayers" :loading="loading">
      <template scope="props">
        <b-table-column label="Место" :width="1">
          {{ statsByPlayer[props.row.id].place }}
        </b-table-column>
        <b-table-column label="Игрок">
          {{ props.row.name }}
        </b-table-column>
        <b-table-column label="Лучшая серия" :visible="rating.is_series">
          <rating-value :rating="rating" :value="statsByPlayer[props.row.id].value.best"/>
          <series-details :series="statsByPlayer[props.row.id].value.best"/>
        </b-table-column>
        <b-table-column label="Текущая серия" :visible="rating.is_series">
          <rating-value :rating="rating" :value="statsByPlayer[props.row.id].value.current"/>
          <series-details :series="statsByPlayer[props.row.id].value.current"/>
        </b-table-column>
        <b-table-column label="Значение" :visible="!rating.is_series">
          {{ statsByPlayer[props.row.id].value }}
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>
<script>
  import axios from 'axios'
  import RatingValue from "@/components/RatingValue"
  import SeriesDetails from "@/components/SeriesDetails"
  export default {
      data() {
          return {
              rating: {},
              players: [],
              stats: [],
              loading: false,
          }
      },
      created(){
        this.fetchData()
      },
      watch:{
        '$route': 'fetchData'
      },
      methods: {
        async fetchData() {
          this.loading = true
          let rating = await axios.get(`/api/instances/1/ratings/${this.$route.params.id}/?format=json`)
          let players = await axios.get('/api/instances/1/players/?format=json')
          let stats = await axios.get(`/api/instances/1/stats/?rating=${this.$route.params.id}&format=json`)
          this.rating = rating.data
          this.players = players.data
          this.stats = stats.data
          this.loading = false
        }
      },
      computed: {
          statsByPlayer() {
              return this.stats.reduce((acc, val) => {acc[val.player] = val; return acc}, {})
          },
          filteredPlayers() {
              let players = this.players.filter(player => player.id in this.statsByPlayer)
              players.sort((a,b) => {return this.statsByPlayer[a.id].place - this.statsByPlayer[b.id].place})
              return players
          }
      },
      components: {
        RatingValue,
        SeriesDetails
      }
  }
</script>
