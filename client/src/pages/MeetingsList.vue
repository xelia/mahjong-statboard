<template>
  <div class="container">
    <b-table
      :data="meetings"
      :narrowed="true"
      :mobileCards="true"
      :loading="loading"
      :paginated="true"
      :per-page="30"
    >
      <template slot-scope="props">
        <b-table-column field="date" label="Дата">
          <span style="white-space: nowrap;">{{ props.row.date }}</span>
        </b-table-column>
        <b-table-column field="games" label="Число игр">
          {{ props.row.games_count }}
        </b-table-column>
        <b-table-column field="games" label="Число игроков">
          {{ props.row.players_count }}
        </b-table-column>
        <b-table-column field="players" label="Игроки">
          <div class="tags"><span v-for="player in props.row.players" class="tag" :key="player">{{ player }} </span></div>
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
      return {
        meetings: [],
        loading: false,
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
        let url = `/api/instances/${this.$store.state.instance.id}/meetings/?format=json`
        this.loading = true
        let res = await axios.get(url)
        this.meetings = res.data
        this.loading = false
      },
    },
}
</script>
