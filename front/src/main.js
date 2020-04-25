import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import App from './App.vue';
import axios from 'axios'
import store from './store';
import router from './router';
import Vuelidate from 'vuelidate';
import './filters';

Vue.use(BootstrapVue);
Vue.use(Vuelidate)

Vue.config.productionTip = false

axios.defaults.baseURL = 'http://localhost:5555';
axios.defaults.headers.get['Accepts'] = 'application/json';

const reqInterceptor = axios.interceptors.request.use(config => {
  return config;
})
const resInterceptor = axios.interceptors.response.use(res => {
  return res;
})

axios.interceptors.request.eject(reqInterceptor);
axios.interceptors.response.eject(resInterceptor);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
