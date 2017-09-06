import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/pages/Layout.vue'
const GamesList = () => import('@/pages/GamesList.vue')
const RatingTable = () => import('@/pages/RatingTable.vue')
const RatingDetails = () => import('@/pages/RatingDetails.vue')
const PlayerDetails = () => import('@/pages/PlayerDetails.vue')
const AddGames = () => import('@/pages/AddGames.vue')
const Login = () => import('@/pages/auth/Login.vue')
const MeetingsList = () => import('@/pages/MeetingsList.vue')

Vue.use(Router)

export default new Router({
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
        }
      ]
    },
  ]
})
