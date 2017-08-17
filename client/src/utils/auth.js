import axios from 'axios'
import jwtDecode from 'jwt-decode'
import router from '@/router'


export default {
    user: {
        authenticated: false,
        token: null,
        data: {}
    },

    init() {
        let token = localStorage.getItem('auth_token')
        if(token){this.setToken(token)}
        axios.interceptors.request.use(config => {
            if(this.user.token){config.headers['Authorization'] = 'JWT ' + this.user.token}
            return config
        });
        axios.interceptors.response.use(undefined, error => {
            if(error.response.status === 401 && error.response.data.detail === 'Signature has expired.'){
              this.logout()
            } else {
              return Promise.reject(error);
            }
        });
    },

    setToken(token){
        this.user.token = token
        this.user.authenticated = Boolean(token)
        this.user.data = token ? jwtDecode(token) : {}
        localStorage.setItem('auth_token', token)
    },

    async login(username, password){
        let response = await axios.post('/api/auth/login/', {username: username, password: password})
        let token = response.data.token
        this.setToken(token)
        router.push({path: '/'})
    },

    logout() {
        this.user.authenticated = false
        this.user.data = {}
        this.user.token = null
        localStorage.removeItem('auth_token')
        window.location.assign('/')
    },
}
