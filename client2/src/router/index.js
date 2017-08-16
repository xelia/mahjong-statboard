import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/pages/Layout.vue'
import GamesList from '@/pages/GamesList.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Layout',
      component: Layout,
      children: [
        {
          path: 'games/',
          name: 'Games',
          component: GamesList,
        }
      ]
    }
  ]
})
