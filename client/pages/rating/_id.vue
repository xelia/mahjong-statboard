<template>
  <div class="container">
    <h1 class="title">{{ rating.name }}</h1>
    <b-table :data="filteredPlayers">
      <template scope="props">
        <b-table-column label="Место" :width="1">
          {{ statsByPlayer[props.row.id].place }}
        </b-table-column>
        <b-table-column label="Игрок">
          {{ props.row.name }}
        </b-table-column>
        <b-table-column label="Лучшая серия" v-if="rating.is_series">
          <rating-value :rating="rating" :value="statsByPlayer[props.row.id].value.best"/>
          <series-details :series="statsByPlayer[props.row.id].value.best"/>
        </b-table-column>
        <b-table-column label="Текущая серия" v-if="rating.is_series">
          <rating-value :rating="rating" :value="statsByPlayer[props.row.id].value.current"/>
          <series-details :series="statsByPlayer[props.row.id].value.current"/>
        </b-table-column>
        <b-table-column label="Значение" v-if="!rating.is_series">
          {{ statsByPlayer[props.row.id].value }}
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>
<script>
  import RatingValue from "~/components/RatingValue"
  import SeriesDetails from "~/components/SeriesDetails"
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
        RatingValue,
        SeriesDetails
      }
  }
</script>
