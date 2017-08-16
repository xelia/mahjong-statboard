<template>
  <div>
    <navbar :ratings="ratings"></navbar>
    <section class="section">
      <router-view></router-view>
    </section>
  </div>
</template>
<script>
  import axios from 'axios'
  import Navbar from '@/components/Navbar'
  export default {
    data() {
      return {
        ratings: [],
      }
    },
    components: {
      Navbar,
    },
    created() {
      this.fetchData()
    },
    methods:{
      async fetchData() {
        let ratings = await axios.get(`/api/instances/1/ratings/?format=json`)
        this.ratings = ratings.data
      }
    }
//    computed: mapGetters([
//      'isAuthenticated',
//      'loggedUser'
//    ])
  }
</script>
