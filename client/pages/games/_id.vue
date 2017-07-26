<template>
  <table>
    {{ $route.params }}
    <tr v-for="game in games">
      <td>{{ game.id }}</td>
    </tr>
  </table>
</template>

<script>
import axios from 'axios';
export default {
    async asyncData({params}) {
        let data = await axios.get('http://localhost:8000/instances/1/games/')
        return {games: data.results}
    },
    data() {
        return {
            games: [],
        }
    }
}
</script>

<style>
</style>
