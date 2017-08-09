<template>
  <div>
    <navbar :ratings="ratings"></navbar>
    <section class="section">
      <nuxt-child :key="$route.path"></nuxt-child>
    </section>
  </div>
</template>
<script>
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
    }
  }
</script>
<style lang="scss">
  @import "~bulma/sass/utilities/initial-variables";

  $link: #428bca;

  @import "~bulma";
  @import "~buefy/src/scss/buefy";
</style>
