<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',
  metaInfo() {
     return {
       title: (this.$store.state.instance && this.$store.state.instance.title) ? this.$store.state.instance.title: 'Рейтинг'
     }
  }
}
</script>
<style>
  @import "~font-awesome/css/font-awesome.css";
</style>
<style lang="scss">
  @import "~bulma/sass/utilities/initial-variables";

  $primary: #428bca;
  $link: #428bca;

  @import "~bulma";
  @import "~buefy/src/scss/buefy";
</style>
