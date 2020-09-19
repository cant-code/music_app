import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import spotify from './modules/spotify'
import player from './modules/player'

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
    spotify,
    player
  }
})
