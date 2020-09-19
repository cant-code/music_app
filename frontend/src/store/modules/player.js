const state = {
    player: '',
    id: '',
    type: ''
};

const getters = {
    getDetails: (state) => {
        return {
            player: state.player,
            id: state.id,
            type: state.type
        }
    },
};

const mutations = {
    SET_DATA(state, data) {
        state.player = data.player;
        state.id = data.id;
        state.type = data.type;
    },
};

const actions = {
    setData({commit}, data){
        commit("SET_DATA", data);
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