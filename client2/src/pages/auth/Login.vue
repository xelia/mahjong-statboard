<template>
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-half">
        <b-field label="Username">
          <b-input v-model="username" :message="error.username" :type="error.username?'is-danger':''"></b-input>
        </b-field>
        <b-field label="Password" :message="error.password" :type="error.password?'is-danger':''">
          <b-input v-model="password" type="password"></b-input>
        </b-field>
        <p v-if="error.non_field_errors" class="has-text-danger">{{ error.non_field_errors[0] }}</p>
        <button class="button" :class="{'is-loading': loading}" @click="Login()">Login</button>
      </div>
    </div>
  </div>
</template>
<script>
  import {setToken} from '~/utils/auth'
  export default {
    middleware: ['anonymous'],
    data() {
      return {
        username: '',
        password: '',
        loading: false,
        error: {},
      }
    },
    methods: {
      async login() {
        this.loading = true
        this.error={}
        try {
          let result = await this.$axios.post('/auth/login/', {
              username: this.username,
              password: this.password,
            },
          )
          setToken(result.data.token)
          this.$router.push('/')
        } catch(e){
          this.error = e.response.data
        }
        this.loading = false
      }
    }
  }
</script>
