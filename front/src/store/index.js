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
    showAlert : false,
    currenturl:'/Grades'
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
    StoreCurrentUrl(state,newurl){
      state.currenturl = newurl
    }
  },
  actions: {
    signup ({commit, dispatch}, authData) {
      axios.post('/register', {
        full_name : authData.FullName,
        mobile : authData.Mobile,
        password : authData.Password,
        returnSecureToken: true
      })
        .then(res => {
          commit('authUser', {
            token: res.data.token,
            userId: res.data.id
          });
          localStorage.setItem('token', res.data.token)
          localStorage.setItem('userId', res.data.id)
          localStorage.setItem('FullName', res.data.full_name)
          dispatch('storeUser', authData);
          router.replace('/Grades')
        })
        .catch(error => console.log(error,'error'))
    },
    login ({commit}, authData) {
      axios.post('/login', {
        mobile : authData.Mobile,
        password : authData.Password,
        returnSecureToken: true
      })
        .then(res => {
          localStorage.setItem('token', res.data.token)
          localStorage.setItem('userId', res.data.id)
          localStorage.setItem('FullName', res.data.full_name)
          setTimeout(() => {
            commit('authUser', {
            token: res.data.token,
            userId: res.data.id
            });
        this.state.showAlert = true
          router.replace('/Grades')
        }, 20)
        })
        .catch(error =>{
          this.state.showAlert = true
          console.log(error)
        })
    },
    tryAutoLogin ({commit}) {
      const token = localStorage.getItem('token')
      const userId = localStorage.getItem('userId')
      if (!token) {
        return
      }else{
        commit('authUser', {token: token,userId: userId})
        router.replace(this.state.currenturl)
      }
    },
    logout ({commit}) {
      commit('clearAuthData')
      localStorage.removeItem('FullName')
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
      this.state.showAlert = false
      router.replace('/login')
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
    }
  }
})
