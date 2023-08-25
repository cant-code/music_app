import Vuex from 'vuex'
import auth from './modules/auth'
import spotify from './modules/spotify'
import player from './modules/player'

export default Vuex.createStore({
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
