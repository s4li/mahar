import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

import router from '../router/index';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: null,
    userId: null,
    user: null
  },
  mutations: {
    authUser (state, userData) {
      state.token = userData.token;
      state.userId = userData.userId;
    },
    storeUser (state, user) {
      state.user = user;
    },
    clearAuthData (state) {
      state.token = null;
      state.userId = null;
    }
  },
  actions: {
    signup ({commit, dispatch}, authData) {
      console.log(authData.Password)
      axios.post('/api/register', {
        full_name : authData.FullName,
        mobile : authData.Mobile,
        password : authData.Password,
        returnSecureToken: true
      })
        .then(res => {
          console.log(res.data)
          commit('authUser', {
            token: res.data.token,
            userId: res.data.id
          });
          localStorage.setItem('token', res.data.token);
          localStorage.setItem('userId', res.data.id);
          localStorage.setItem('FullName', res.data.full_name);
          dispatch('storeUser', authData);
          router.replace('/Grades')
        })
        .catch(error => console.log(error,'error'));
    },
    login ({commit}, authData) {
      axios.post('/api/login', {
        mobile : authData.Mobile,
        password : authData.Password,
        returnSecureToken: true
      })
        .then(res => {
          console.log(res.data)
          localStorage.setItem('token', res.data.token);
          localStorage.setItem('userId', res.data.id);
          localStorage.setItem('FullName', res.data.full_name);
          commit('authUser', {
            token: res.data.token,
            userId: res.data.id
          });
          router.replace('/Grades')
        })
        .catch(error => console.log(error));
    },
    tryAutoLogin ({commit}) {
      const token = localStorage.getItem('token');
      if (!token) {
        return;
      }
      const userId = localStorage.getItem('userId');
      commit('authUser', {
        token: token,
        userId: userId
      });
    },
    logout ({commit}) {
      commit('clearAuthData');
      localStorage.removeItem('FullName');
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
      router.replace('/login');
    },
    storeUser ({state}) {
      if (!state.token) {
        return;
      }
    },
    fetchUser ({state}) {
      if (!state.token) {
        return
      }
      axios.get('/api/get-user-information/' + state.userId)
        .then(res => {
          console.log(res)
          //commit('storeUser', res.data)
        })
        .catch(error => console.log(error))
    }
  },
  getters: {
    user (state) {
      return state.user
    },
    isAuthenticated (state) {
      return state.token !== null
    }
  }
})
