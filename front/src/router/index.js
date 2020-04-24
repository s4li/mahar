import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Landingpage.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/Singup',
    name: 'SingUp',
    component: () => import('../views/SingUp.vue')
  },
  {
    path: '/Grades',
    name: 'Grades',
    component: () => import('../views/Grades.vue')
  },
  {
    path: '/Guids',
    name: 'Guids',
    component: () => import('../views/Guids.vue')
  },
  {
    path: '*',redirect:'/MyAccount'
  }
]

const router = new VueRouter({
  routes,
  mode: 'history',
})

export default router
