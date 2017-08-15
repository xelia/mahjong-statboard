import { getUserFromCookie, getUserFromLocalStorage } from '~/utils/auth'

export default function ({ app, isServer, store, req }) {
   // If nuxt generate, pass this middleware
  if (isServer && !req) return
  const [token, loggedUser] = isServer ? getUserFromCookie(req) : getUserFromLocalStorage()
  store.commit('SET_USER', loggedUser)
  app.$axios.setToken(token, 'jwt')
}
