import jwtDecode from 'jwt-decode'
import Cookie from 'js-cookie'


export const setToken = (token) => {
  if (process.SERVER_BUILD) return
  Cookie.set('jwt', token, {expires: new Date(jwtDecode(token).exp * 1000)})
}

export const unsetToken = () => {
  if (process.SERVER_BUILD) return
  Cookie.remove('jwt')
}

export const getUserFromCookieServerSide = (req) => {
  if (!req.headers.cookie) return
  const jwtCookie = req.headers.cookie.split(';').find(c => c.trim().startsWith('jwt='))
  if (!jwtCookie) return [undefined, undefined]
  const jwt = jwtCookie.split('=')[1]
  return [jwt, jwtDecode(jwt)]
}

export const getUserFromCookieClientSide = () => {
  const jwt = Cookie.get('jwt')
  if(!jwt){
    return [undefined, undefined]
  }
  return [jwt, jwtDecode(jwt)]
}
