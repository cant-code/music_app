import Vue from 'vue'
import store from "@/store";
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
const formsView = () => import('@/views/Forms')
const settings = () => import('@/components/Settings')
const Landing = () => import('@/components/LandingPage')

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: formsView,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: formsView,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: settings,
  },
  {
    path: '/landing',
    name: 'Landing',
    component: Landing
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach(function(to, from, next) {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters["auth/getUserToken"]) {
      next({
        path: '/login',
      })
    } else {
      next()
    }
  } else {
    next()
  }
});

export default router
