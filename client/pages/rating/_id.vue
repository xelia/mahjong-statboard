<template>
  <b-table :data="filteredPlayers" v-if="rating.is_series">
    <template scope="props">
      <b-table-column label="Игрок">
        {{ props.row.name }}
      </b-table-column>
      <b-table-column label="Лучшая серия">
        {{ statsByPlayer[props.row.id].value.best }}
      </b-table-column>
      <b-table-column label="Текущая серия">
        {{ statsByPlayer[props.row.id].value.current }}
      </b-table-column>
    </template>
  </b-table>
</template>
<script>
  import RatingValue from "~/components/RatingValue"
  export default {
      async asyncData({app, params}) {
          let rating = await app.$axios.get(`/instances/1/ratings/${params.id}/?format=json`)
          let players = await app.$axios.get('/instances/1/players/?format=json')
          let stats = await app.$axios.get(`/instances/1/stats/?rating=${params.id}&format=json`)
          return {
              rating: rating.data,
              players: players.data,
              stats: stats.data,
          }
      },
      data() {
          return {
              rating: null,
              players: [],
              stats: [],
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
        RatingValue
      }
  }
</script>
