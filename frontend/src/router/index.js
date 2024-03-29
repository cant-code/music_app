import store from "@/store";
import Home from '../views/Home.vue'
import { createRouter, createWebHistory } from "vue-router";

const formsView = () => import('@/views/Forms')
const settings = () => import('@/components/Settings')
const Landing = () => import('@/components/LandingPage')
const playlist = () => import('@/components/Browse/playlist')
const album = () => import('@/components/Browse/album')
const user = () => import('@/components/User/userData')


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
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/landing',
    name: 'Landing',
    component: Landing,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/playlists/:id',
    name: 'playlist',
    component: playlist,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('@/components/search'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/albums/:id',
    name: 'album',
    component: album,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/user',
    name: 'user',
    component: user,
    meta: {
      requiresAuth: true
    }
  },
]

const router = createRouter({
  history: createWebHistory(),
  base: import.meta.env.BASE_URL,
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
