<template>
  <div>
    <b-table
      :data="games"
    >
      <template scope="props">
        <b-table-column field="date" label="Дата">
            {{ props.row.date }}
        </b-table-column>
        <b-table-column field="date" label="Игрок1">
            {{ props.row.results[0].player }}
        </b-table-column>
        <b-table-column field="date" label="Счет">
            {{ props.row.results[0].score }}
        </b-table-column>
      </template>
      <div slot="empty">qwe</div>
    </b-table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  async asyncData({query}) {
        let page = query.page
        let url = `http://localhost:8000/instances/1/games/`
        if (page) {url = `${url}?page=${page}`}
        let res = await axios.get(url)
        return {games: res.data.results}
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
