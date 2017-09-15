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
      let instance = null
      //TODO: сделать нормально
      if(['rating.tesuji.ru', 'newrating.tesuji.ru', 'localhost'].includes(hostname)) {
        instance = await axios.get('/api/instances/1/')
      }else {
        instance = await axios.get('/api/instances/2/')
      }
      commit('setInstance', instance.data)
    }
  },
  strict: debug,
})

export default store
