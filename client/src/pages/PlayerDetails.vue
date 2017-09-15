<template>
  <div>
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            {{ player.name }}
          </h1>
          <h2 class="subtitle">
            {{ player.full_name }}
          </h2>
        </div>
      </div>
    </section>
    <section>
      <div class="container">
        <b-tabs v-model="activeTab" type="is-boxed" :class="{height: '80px'}">
          <b-tab-item label="Статистика">
            <stats-tab :stats="player.stats"></stats-tab>
          </b-tab-item>
          <b-tab-item label="Игры">
            <games-list-tab :player="player" v-if="activeTab == 1"></games-list-tab>
          </b-tab-item>
          <b-tab-item label="Оппоненты">
            <opponents-tab :player="player" v-if="activeTab == 2"></opponents-tab>
          </b-tab-item>
          <!--<b-tab-item v-for="(stat, rating_id) in player.stats" :label="rating_id" :key="rating_id">-->
            <!--{{ stat }}-->
          <!--</b-tab-item>-->
        </b-tabs>
      </div>
    </section>
  </div>
</template>
<script>
  import axios from 'axios'
  import StatsTab from '@/components/profile_tabs/StatsTab'
  let GamesListTab = () => import('@/components/profile_tabs/GamesListTab')
  let OpponentsTab = () => import('@/components/profile_tabs/OpponentsTab')
  export default {
    data(){
      return {
        player: {},
        activeTab: 0,
      }
    },
    created(){
      this.fetchData()
    },
    watch: {
      '$route': 'fetchData'
    },
    methods: {
      async fetchData(){
        let player = await axios.get(`/api/instances/${this.$store.state.instance.id}/players/${this.$route.params.id}/?format=json&extended=true`)
        this.player = player.data
      }
    },
    components: {
      StatsTab,
      GamesListTab,
      OpponentsTab
    }
  }
</script>
<style scoped="">
  .tab-item {
    min-height: 300px;
  }
</style>
