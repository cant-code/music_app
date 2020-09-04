import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import spotify from './modules/spotify'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    auth,
    spotify
  }
})
