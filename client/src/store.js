import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

const store = new Vuex.Store({
  state(){
    return {
      instance: null
    }
  },
  mutations: {
    setInstance (state, instance){
      state.instance = instance
    }
  },
  actions: {
    async loadInstance({commit}, hostname){
      let instance = await axios.get(`/api/instances/?domain=${hostname}`)
      commit('setInstance', instance.data.results[0])
    }
  },
  strict: debug,
})

export default store
