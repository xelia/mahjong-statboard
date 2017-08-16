<template>
  <div class="container">
    <b-pagination
      :simple="false"
      :per-page="30"
      :total="total_games"
      :current.sync="page"
      @change="changePage($event)"
    />
    <daily-games-table :key="date" :date="date" :games="games" v-for="(games, date) in groupedGames" ></daily-games-table>
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
import DailyGamesTable from '@/components/DailyGamesTable'
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
        let url = `/api/instances/1/games/?format=json`
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
      DailyGamesTable
    }
}
</script>
