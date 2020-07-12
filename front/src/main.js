import 'bootstrap/dist/css/bootstrap.css'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Vuelidate from 'vuelidate'
import './filters'
import './registerServiceWorker'


Vue.use(BootstrapVue);
Vue.use(Vuelidate)
Vue.config.productionTip = false
Vue.prototype.$http = axios


axios.defaults.baseURL = 'http://localhost:5555/api'
//axios.defaults.baseURL = 'https://doplus.ir/api'
axios.defaults.headers.get['Accepts'] = 'application/json'

const token = localStorage.getItem('token')

if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = `Bearer: ${token}`
}else{
  Vue.prototype.$http.defaults.headers.common['Authorization'] = null
}

const reqInterceptor = axios.interceptors.request.use(config => {
  return config
})
const resInterceptor = axios.interceptors.response.use(res => {
  return res
})

axios.interceptors.request.eject(reqInterceptor)
axios.interceptors.response.eject(resInterceptor)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
