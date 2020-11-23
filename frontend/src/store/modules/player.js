const state = {
    player: '',
    id: '',
    type: '',
    currentlyPlaying: '',
};

const getters = {
    getDetails: (state) => {
        return {
            player: state.player,
            id: state.id,
            type: state.type
        }
    },
    getCurrentlyPlaying: (state) => {
        return state.currentlyPlaying
    },
};

const mutations = {
    SET_DATA(state, data) {
        state.player = data.player;
        state.id = data.id;
        state.type = data.type;
    },
    SET_CURRENT(state, data) {
        state.currentlyPlaying = data;
    }
};

const actions = {
    setData({commit}, data){
        commit("SET_DATA", data);
    },
    setCurrentlyPlaying({commit}, data) {
        commit('SET_CURRENT', data);
    },
};

const module = {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
};

export default module;