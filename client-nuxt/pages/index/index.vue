<template>
  <div class="container">
    <b-table
      :data="sortedPlayers"
      :striped="true"
      :narrowed="true"
      :mobileCards="true"
      :backend-sorting="true"
      @sort="doSort"
    >
      <template scope="props">
        <b-table-column label="Место" width="1">
          {{ props.index }}
        </b-table-column>
        <b-table-column label="Имя">
          <nuxt-link :to="`/players/${props.row.id}`">{{ props.row.name }}</nuxt-link>
        </b-table-column>
        <b-table-column
          v-for="rating in ratings"
          :label="rating.name"
          :key="rating.id"
          :field="rating.id.toString()"
          sortable
        >
          <rating-value
            v-if="props.row.stats && props.row.stats[rating.id]"
            :value="rating.is_series? props.row.stats[rating.id].value.best : props.row.stats[rating.id].value"
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
          let ratings = await app.$axios.get('/instances/1/ratings/?format=json')
          let players = await app.$axios.get('/instances/1/players/?format=json')
          let stats = await app.$axios.get(`/instances/1/stats/?format=json`)
          return {
              ratings: ratings.data,
              players: players.data,
              stats: stats.data,
              sortField: null,
              sortDirection: 'asc'
          }
      },
      data() {
          return {
              ratings: [],
              players: [],
              stats: [],
          }
      },
      created(){
        this.doSort(this.ratings[0].id, 'asc')
      },
      computed: {
          playersWithStats(){
              let players = [...this.players]
              let stats = this.stats.reduce(
                  (acc, val) => {
                      acc[val.player] = acc[val.player] || {};
                      acc[val.player][val.rating] = val;
                      return acc
                  }, {}
              )
              for (let player of players){
                  player['stats'] = stats[player.id]
              }
              return players
          },
          sortedPlayers(){
              let players = [...this.playersWithStats]
              if(this.sortField) {
                players.sort((a, b) => {
                  if(!a.stats || !a.stats[this.sortField])
                    return 1
                  if(!b.stats || !b.stats[this.sortField])
                    return -1;
                  let val = a.stats[this.sortField].place - b.stats[this.sortField].place
                  if (this.sortDirection == 'desc') val *= -1
                  return val
                })
              }
              return players
          }
      },
      methods:{
          doSort(sortField, sortDirection){
              this.sortField = sortField
              this.sortDirection = sortDirection
          }
      },
      components: {
        RatingValue
      }
  }
</script>
