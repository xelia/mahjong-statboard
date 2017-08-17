import { getUserFromCookieServerSide, getUserFromCookieClientSide,  } from '~/utils/auth'

export default function ({ app, isServer, store, req }) {
   // If nuxt generate, pass this middleware
  if (isServer && !req) return
  const [token, loggedUser] = isServer ? getUserFromCookieServerSide(req) : getUserFromCookieClientSide()
  store.commit('SET_USER', loggedUser)
  store.commit('SET_TOKEN', token)
}
