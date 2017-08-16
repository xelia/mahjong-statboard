export const state = () => {
  return {
    user: null,
    token: null,
  }
}

export const mutations = {
  SET_USER (state, user) {
    state.user = user || null
  },
  SET_TOKEN (state, token) {
    state.token = token || null
  }
}

export const getters = {
  isAuthenticated (state) {
    return !!state.user
  },
  loggedUser (state) {
    return state.user
  },
  loggedUserToken (state) {
    return state.token
  }
}
