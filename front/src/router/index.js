import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '../store/index';
import Home from '../views/Landingpage.vue';

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/Guids',
    name: 'Guids',
    component: () => import('../views/Guids.vue')
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
    component: () => import('../views/Grades.vue'),
    beforeEnter (to, from, next) {
      if (store.state.idToken) {
        next();
      } else {
        next('/login');
      }
    }
  },
  {
    path: '/Lessons/:id',
    name: 'Lessons',
    component: () => import('../views/Lessons.vue'),
    beforeEnter (to, from, next) {
      if (store.state.idToken) {
        next();
      } else {
        next('/login');
      }
    }
  },
  {
    path: '/ExamType/:id',
    name: 'ExamType',
    component: () => import('../views/ExamType.vue'),
    beforeEnter (to, from, next) {
      if (store.state.idToken) {
        next();
      } else {
        next('/login');
      }
    }
  },
  {
    path: '/Courses/:type',
    name: 'Courses',
    component: () => import('../views/Courses.vue'),
    beforeEnter (to, from, next) {
      if (store.state.idToken) {
        next();
      } else {
        next('/login');
      }
    }
  },
  {
    path: '*',redirect:'/Grades'
  }
]

const router = new VueRouter({
  routes,
  mode: 'history',
})

export default router
