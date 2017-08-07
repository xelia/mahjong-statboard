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
        <b-table-column label="Имя">
          {{ props.row.name }}
        </b-table-column>
        <b-table-column
          v-for="rating in ratings"
          :label="rating.name"
          :key="rating.id"
          :field="rating.id.toString()"
          sortable
        >
          <rating-value
            v-if="groupedStats[props.row.id] && groupedStats[props.row.id][rating.id]"
            :value="rating.is_series?groupedStats[props.row.id][rating.id].value.best:groupedStats[props.row.id][rating.id].value"
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
      computed: {
          groupedStats() {
              return this.stats.reduce(
                  (acc, val) => {
                      acc[val.player] = acc[val.player] || {};
                      acc[val.player][val.rating] = val;
                      return acc
                  }, {}
              )

          },
          sortedPlayers(){
              console.log('qwe')
              let players = [...this.players]
              if(this.sortField) {
                players.sort((a, b) => {
                  if (!this.groupedStats[a.id] || !this.groupedStats[a.id][this.sortField])
                    return 1
                  if(!this.groupedStats[b.id] || !this.groupedStats[b.id][this.sortField])
                    return -1;
                  let val = this.groupedStats[a.id][this.sortField].place - this.groupedStats[b.id][this.sortField].place
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
