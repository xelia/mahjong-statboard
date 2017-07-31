<template>
  <div class="container">
    <b-table :data="players">
      <template scope="props">
        <b-table-column label="Имя">
          {{ props.row.name }}
        </b-table-column>
        <b-table-column
          v-for="rating in instance.ratings"
          :label="rating.name"
          :key="rating.id"
        >
          <rating-value
            :value="{}"
            :rating="rating"
          >
          </rating-value>
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
  import RatingValue from "~/components/RatingValue"
  export default {
      async asyncData({app}) {
          let instance = await app.$axios.get('/instances/1/?format=json')
          let players = await app.$axios.get('/instances/1/players/?format=json')
          return {
              instance: instance.data,
              players: players.data
          }
      },
      data() {
          return {
              instance: null,
              players: [],
          }
      },
      methods:{
          getPlayerRating(player, rating) {
              return player.stats.find(stat => {return stat.rating == rating.id})
          }
      },
      components: {
        RatingValue
      }
  }
</script>
