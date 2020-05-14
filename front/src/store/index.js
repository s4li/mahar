import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '../router/index'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    idToken: null,
    userId: null,
    user: null,
    alerttext : '',
    showAlert:false,
    currenturl:'/Grades',
  },
  mutations: {
    authUser (state, userData) {
      state.idToken = userData.token
      state.userId = userData.userId
    },
    storeUser (state, user) {
      state.user = user;
    },
    clearAuthData (state) {
      state.idToken = null
      state.userId = null
    },
    StoreCurrentUrl(state,url){
      state.currenturl = url
    }
  },
  actions: {
    setLogoutTimer ({commit}, expirationTime) {
      setTimeout(() => {
        commit('clearAuthData')
        localStorage.removeItem('FullName')
        localStorage.removeItem('token')
        localStorage.removeItem('userId')
      }, expirationTime * 1000 )
    },
    signup ({commit, dispatch}, authData) {
      axios.post('/register', {
        full_name : authData.FullName,
        mobile : authData.Mobile,
        password : authData.Password,
        returnSecureToken: true
      })
        .then(res => {
          const token = res.data.token
          localStorage.setItem('token', res.data.token)
          localStorage.setItem('userId', res.data.id)
          localStorage.setItem('FullName', res.data.full_name)
          axios.defaults.headers.common['Authorization'] = `Bearer: ${token}`
          commit('authUser', {
            token: res.data.token,
            userId: res.data.id
          });
          dispatch('storeUser', authData);
          dispatch('setLogoutTimer', 86400)
          this.state.showAlert = false
          router.replace('/Grades')
        })
        .catch(error => {
          this.state.showAlert = true
          if (error.response.status == 401){
            this.state.alerttext = error.response.data.result
          }else{
            this.state.alerttext = 'خطای غیرمنتظره'
          }
          localStorage.removeItem('FullName')
          localStorage.removeItem('token')
          localStorage.removeItem('userId')
        })
    },
    login ({commit, dispatch}, authData) {
      axios.post('/login', {
        mobile : authData.Mobile,
        password : authData.Password,
        returnSecureToken: true
      })
        .then(res => {
          const token = res.data.token
          localStorage.setItem('token', res.data.token)
          localStorage.setItem('userId', res.data.id)
          localStorage.setItem('FullName', res.data.full_name)
          axios.defaults.headers.common['Authorization'] = `Bearer: ${token}`
            commit('authUser', {
            token: res.data.token,
            userId: res.data.id
            });
            dispatch('setLogoutTimer', 86400)
          this.state.showAlert = false
          router.replace('/Grades')
        })
        .catch((error) =>{
          this.state.showAlert = true
          if (error.response.status == 401){
            this.state.alerttext = error.response.data.result
          }else{
            this.state.alerttext = 'خطای غیرمنتظره'
          }
          localStorage.removeItem('FullName')
          localStorage.removeItem('token')
          localStorage.removeItem('userId')
        })
    },
    tryAutoLogin ({commit}) {
      const token = localStorage.getItem('token')
      const userId = localStorage.getItem('userId')
      if (!token) {
        return
      }else{
        commit('authUser', {token: token,userId: userId})
        const myurl = this.getters.geturl
        router.push(myurl)
      }
    },
    saveurl({commit},url){
      commit('StoreCurrentUrl',url)
    },
    logout ({commit}) {
      commit('clearAuthData')
      localStorage.removeItem('FullName')
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
      this.state.showAlert = false
      delete axios.defaults.headers.common['Authorization']
      router.replace('/')
    },
    storeUser ({state}) {
      if (!state.idToken) {
        return
      }
    },
    fetchUser ({state,commit}) {
      if (!state.idToken) {
        return
      }
      axios.get('/get-user-information',{params: {id: state.userId}})
        .then(res => {
          const user = {
            FullName:res.data.full_name,
            Mobile:res.data.full_name
          }
          commit('storeUser', user)
        })
        .catch(error => console.log(error,'error2'))
    }
  },
  getters: {
    user (state) {
      return state.user
    },
    isAuthenticated (state) {
      return state.idToken !== null
    },
    geturl(state){
      return state.currenturl
    }
  }
})
