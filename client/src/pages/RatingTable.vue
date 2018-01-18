<template>
  <div class="container">
    <b-table
      :data="sortedPlayers"
      :striped="true"
      :narrowed="true"
      :mobileCards="true"
      :backend-sorting="true"
      @sort="doSort"
      :loading="loading"
    >
      <template slot-scope="props">
        <b-table-column label="Место" width="1">
          {{ props.index + 1 }}
        </b-table-column>
        <b-table-column label="Имя">
          <router-link :to="`/player/${props.row.id}`">{{ props.row.name }}</router-link>
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
            :value="props.row.stats[rating.id].value"
            :rating="rating"
          >
          </rating-value>
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>
<script>
  import axios from 'axios'
  import RatingValue from "@/components/RatingValue"
  export default {
      data() {
          return {
              ratings: [],
              players: [],
              stats: [],
              sortField: null,
              sortDirection: 'asc',
              loading: false
          }
      },
      async created(){
        await this.fetchData()
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
                  if (this.sortDirection === 'desc') val *= -1
                  return val
                })
              }
              return players
          }
      },
      methods:{
         async fetchData() {
           this.loading = true
           let [ratings, players, stats] = await Promise.all([
             axios.get(`/api/instances/${this.$store.state.instance.id}/ratings/?format=json&archived=false`),
             axios.get(`/api/instances/${this.$store.state.instance.id}/players/?format=json&active=1`),
             axios.get(`/api/instances/${this.$store.state.instance.id}/stats/?format=json`),
           ])
           this.ratings = ratings.data
           this.players = players.data
           this.stats = stats.data
           this.loading = false
         },
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
