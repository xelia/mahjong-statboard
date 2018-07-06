<template>
  <div class="container">
    <b-pagination
      :simple="false"
      :per-page="30"
      :total="total_games"
      :current.sync="page"
      @change="changePage($event)"
    />
    <div class="container" v-for="(games, date) in groupedGames" :key="date">
      <nav class="level">
        <p class="subtitle level-item">{{ date }}</p>
      </nav>
      <games-table :games="games"></games-table>
    </div>
    <b-pagination
      :simple="false"
      :per-page="30"
      :total="total_games"
      :current.sync="page"
      @change="changePage($event)"
    />
  </div>
</template>

<script>
import axios from 'axios'
import GamesTable from '@/components/GamesTable'
import {groupBy} from 'lodash'

export default {
    data() {
        return {
            games: [],
            total_games: 0,
            page: 1
        }
    },
    computed: {
        groupedGames() {
            return groupBy(this.games, game => game.date)
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
        let page = this.$route.query.page || 1
        let url = `/api/instances/${this.$store.state.instance.id}/games/?format=json`
        if (page) {url = `${url}&page=${page}`}
        let res = await axios.get(url)
        this.games = res.data.results
        this.total_games = res.data.count
        this.page = parseInt(page)
      },
      changePage(page) {
        this.$router.push({path: '/games', query: {page: page}})
      }
    },
    components: {
      GamesTable
    }
}
</script>
