import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

import router from '../router/index';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    idToken: null,
    userId: null,
    user: null
  },
  mutations: {
    authUser (state, userData) {
      state.idToken = userData.token;
      state.userId = userData.userId;
    },
    storeUser (state, user) {
      state.user = user;
    },
    clearAuthData (state) {
      state.idToken = null;
      state.userId = null;
    }
  },
  actions: {
    setLogoutTimer ({commit}, expirationTime) {
      setTimeout(() => {
        commit('clearAuthData');
      }, expirationTime * 1000);
    },
    signup ({commit, dispatch}, authData) {
      axios.post('/api/register', {
        full_name : authData.FullName,
        mobile : authData.Mobile,
        password : authData.Password,
        returnSecureToken: true
      })
        .then(res => {
          console.log(res.data)
          commit('authUser', {
            token: res.data.idToken,
            userId: res.data.localId
          });
          const now = new Date();
          const expirationDate = new Date(now.getTime() + res.data.expiresIn * 1000);
          localStorage.setItem('token', res.data.idToken);
          localStorage.setItem('userId', res.data.id);
          localStorage.setItem('expirationDate', expirationDate);
          dispatch('storeUser', authData);
          dispatch('setLogoutTimer', res.data.expiresIn);
        })
        .catch(error => console.log(error,'error'));
    },
    login ({commit, dispatch}, authData) {
      axios.post('/api/login', {
        mobile : authData.Mobile,
        password : authData.Password,
        returnSecureToken: true
      })
        .then(res => {
          console.log(res.data)
          const now = new Date();
          const expirationDate = new Date(now.getTime() + res.data.expiresIn * 1000);
          localStorage.setItem('token', res.data.idToken);
          localStorage.setItem('userId', res.data.id);
          localStorage.setItem('expirationDate', expirationDate);
          commit('authUser', {
            token: res.data.idToken,
            userId: res.data.localId
          })
          dispatch('setLogoutTimer', res.data.expiresIn);
        })
        .catch(error => console.log(error));
    },
    tryAutoLogin ({commit}) {
      const token = localStorage.getItem('token');
      if (!token) {
        return;
      }
      const expirationDate = localStorage.getItem('expirationDate');
      const now = new Date();
      if (now >= expirationDate) {
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
      localStorage.removeItem('expirationDate');
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
      router.replace('/login');
    },
    storeUser ({state}) {
      if (!state.idToken) {
        return;
      }
      //axios.post('/users.json' + '?auth=' + state.idToken, userData)
      //  .then(res => console.log(res))
      //  .catch(error => console.log(error))
    },
    fetchUser ({state}) {
      if (!state.idToken) {
        return
      }
      axios.get('/api/get-user-information/' + state.user.Mobile)
        .then(res => {
          console.log(res)
          //commit('storeUser', users[0])
        })
        .catch(error => console.log(error))
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
