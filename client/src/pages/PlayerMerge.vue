<template>
  <div class="container">
    <h1 class="title">Удаление твинков</h1>
    <b-field label="Основной аккаунт" :message="errors.main_player" :type="errors.main_player ? 'is-danger' : ''">
      <b-select v-model="mainPlayer" :loading="loading">
        <option v-for="player in playersList" :value="player.name" :key="player.id">
          {{ player.name }} ({{ player.games_count }})
        </option>
      </b-select>
    </b-field>
    <b-field
      label="Второй аккаунт (этот аккаунт будет удален)"
      :message="errors.player_to_delete"
      :type="errors.player_to_delete ? 'is-danger' : ''"
    >
      <b-select v-model="playerToDelete" :loading="loading">
        <option v-for="player in playersList" :value="player.name" :key="player.id">
          {{ player.name }} ({{ player.games_count }})
        </option>
      </b-select>
    </b-field>
    <b-field>
      <p class="has-text-danger" v-if="errors.non_field_errors">{{ errors.non_field_errors[0] }}</p>
      <p class="has-text-danger" v-if="errors.detail">{{ errors.detail }}</p>
      <p class="has-text-success" v-if="result !== null">{{ result }} игр успешно изменено</p>
    </b-field>
    <button class="button" @click="confirmSubmit" :class="{ 'is-loading': submitting }">Submit</button>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    data() {
      return {
        mainPlayer: null,
        playerToDelete: null,
        playersList: [],
        errors: {},
        loading: false,
        submitting: false,
        result: null,
      }
    },
    created() {
      this.fetchData()
    },
    watch: {
      '$route': 'fetchData'
    },
    methods: {
      async fetchData() {
        this.loading = true
        let playersList = await axios.get(`/api/instances/${this.$store.state.instance.id}/players/?format=json`)
        this.playersList = playersList.data
        this.playersList.sort((a, b) => a.name.localeCompare(b.name))
        this.loading = false
      },
      confirmSubmit(){
        let message = `Все игры игрока ${this.playerToDelete}
          будут переданы игроку ${this.mainPlayer}. Продолжить?`
        this.$dialog.confirm({
          message: message,
          onConfirm: this.submit
        })
      },
      async submit() {
        this.errors = {}
        this.result = null
        this.submitting = true
        try {
          let result = await axios.post(
            `api/instances/${this.$store.state.instance.id}/player-merge/`,
            {main_player: this.mainPlayer, player_to_delete: this.playerToDelete}
          )
          this.result = result.data
        } catch(error){
          this.errors = error.response.data
        }
        this.submitting = false
      }
    },
  }
</script>
