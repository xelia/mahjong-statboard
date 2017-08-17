import Vue from 'vue'
import App from './App'
import auth from './utils/auth'
import router from './router'
import Buefy from 'buefy'

Vue.config.productionTip = false

Vue.use(Buefy, {defaultIconPack: 'fa'})

auth.init()

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
