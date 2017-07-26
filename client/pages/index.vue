<template>
  <table>
    <tr v-for="game in games">
      <td>{{ game.id }}</td>
    </tr>
  </table>
</template>

<script>
import axios from 'axios';
export default {
    asyncData() {
        return axios.get('http://localhost:8000/instances/1/games/').then(
            res => {return {
                games: res.data.results
            }}
        )
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
