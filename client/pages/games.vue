<template>
  <div class="container">
    <div class=""
    <b-pagination
      :simple="false"
      :per-page="30"
      :total="total_games"
      :current.sync="page"
      @change="changePage($event)"
      order="is-centered"
    />
    <daily-games-table :key="date" :date="date" :games="games" v-for="(games, date) in groupedGames" ></daily-games-table>
    <b-pagination
      :simple="false"
      :per-page="30"
      :total="total_games"
      :current.sync="page"
      @change="changePage($event)"
      order="is-centered"
    />
  </div>
</template>

<script>
import DailyGamesTable from '~/components/DailyGamesTable'
import {groupBy} from 'lodash'

export default {
    async asyncData({app, query}) {
        let page = query.page || 1
        let url = `/instances/1/games/?format=json`
        if (page) {url = `${url}&page=${page}`}
        let res = await app.$axios.get(url)
        return {
            games: res.data.results,
            total_games: res.data.count,
            page: parseInt(page),
        }
    },
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
    methods: {
        changePage(page) {
          this.$router.push({path: '/games', query: {page: page}})
        }
    },
    components: {
      DailyGamesTable
    }
}
</script>

<style>
</style>
