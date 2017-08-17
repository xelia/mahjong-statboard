<template>
  <div>
    <navbar :ratings="ratings" :user="loggedUser"></navbar>
    <section class="section">
      <nuxt-child></nuxt-child>
    </section>
  </div>
</template>
<script>
  import { mapGetters } from 'vuex'
  import Navbar from '~/components/Navbar'
  export default {
    async asyncData({app}) {
      let ratings = await app.$axios.get(`/instances/1/ratings/?format=json`)
      return{
        ratings: ratings.data
      }
    },
    data() {
      return {
        ratings: [],
      }
    },
    components: {
      Navbar,
    },
    computed: mapGetters([
      'isAuthenticated',
      'loggedUser'
    ])
  }
</script>
<style lang="scss">
  @import "~bulma/sass/utilities/initial-variables";

  $link: #428bca;

  @import "~bulma";
  @import "~buefy/src/scss/buefy";
</style>
