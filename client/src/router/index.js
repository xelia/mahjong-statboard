import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/pages/Layout.vue'
import store from '@/store'
const GamesList = () => import('@/pages/GamesList.vue')
const RatingTable = () => import('@/pages/RatingTable.vue')
const RatingDetails = () => import('@/pages/RatingDetails.vue')
const PlayerDetails = () => import('@/pages/PlayerDetails.vue')
const AddGames = () => import('@/pages/AddGames.vue')
const Login = () => import('@/pages/auth/Login.vue')
const MeetingsList = () => import('@/pages/MeetingsList.vue')
const PlayerMerge = () => import('@/pages/PlayerMerge.vue')

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: '/',
          name: 'RatingTable',
          component: RatingTable,
        },
        {
          path: '/games/',
          name: 'GamesList',
          component: GamesList,
        },
        {
          path: '/rating/:id/',
          name: 'RatingDetails',
          component: RatingDetails,
        },
        {
          path: '/player/:id/',
          name: 'PlayerDetails',
          component: PlayerDetails,
        },
        {
          path: '/meetings/',
          name: 'MeetingsList',
          component: MeetingsList,
        },
        {
          path: '/auth/login/',
          name: 'Login',
          component: Login,
        },
        {
          path: '/service/add-games/',
          name: 'AddGames',
          component: AddGames,
        },
        {
          path: '/service/player-merge/',
          name: 'PlayerMerge',
          component: PlayerMerge,
        },
      ]
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  await store.dispatch('loadInstance', window.location.hostname)
  next()
})

export default router
