import jwtDecode from 'jwt-decode'
import Cookie from 'js-cookie'


export const setToken = (token) => {
  if (process.SERVER_BUILD) return
  window.localStorage.setItem('token', token)
  Cookie.set('jwt', token)
}


export const unsetToken = () => {
  if (process.SERVER_BUILD) return
  window.localStorage.removeItem('token')
  Cookie.remove('jwt')
  window.localStorage.setItem('logout', Date.now())
}


export const getUserFromCookie = (req) => {
  if (!req.headers.cookie) return
  const jwtCookie = req.headers.cookie.split(';').find(c => c.trim().startsWith('jwt='))
  if (!jwtCookie) return
  const jwt = jwtCookie.split('=')[1]
  return [jwt, jwtDecode(jwt)]
}


export const getUserFromLocalStorage = () => {
  const token = window.localStorage.token
  return token ? [token, jwtDecode(token)] : [undefined, undefined]
}
