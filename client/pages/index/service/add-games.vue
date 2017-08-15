<template>
  <div class="container">
    <div class="columns">
      <div class="column is-half">
        <b-field label="Игры" message="Формат ввода: Date(ДД.ММ.ГГ) Player1 Score1 Player2 Score2 Player3 Score3 Player4 Score4">
          <b-input type="textarea" v-model="rawGames"></b-input>
        </b-field>
        <p v-if="error" class="has-text-danger" v-html="error"></p>
        <button class="button is-info" :class="{'is-loading': loading}" @click="addGames()">Submit</button>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        loading: false,
        rawGames: '',
        error: null,
      }
    },
    methods: {
      async addGames(){
        this.loading = true
        try {
          let result = await this.$axios.post('/instances/1/games/add_games_legacy/', {
            raw_games: this.rawGames
          })
          this.error = result.data
        } catch(e){
          this.error = e.response.data
        }
        this.loading = false

      }
    }
  }
</script>
