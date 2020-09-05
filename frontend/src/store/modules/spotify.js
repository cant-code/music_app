const state = {
    spot_Username: localStorage.getItem('spot_Username') || '',
    token: localStorage.getItem('token') || '',
    refresh_token: localStorage.getItem('refresh_token') || '',
    expires: localStorage.getItem('expires') || '',
    category: localStorage.getItem('category') || ''
};

const getters = {
    getDetails: (state) => {
        return {
            username: state.spot_Username,
            category: state.category
        }
    },
    getToken: (state) => {return {token: state.token, refresh_token: state.refresh_token, expires: state.expires}},
};

const mutations = {
    SET_DATA(state, data) {
        state.spot_Username = data.username;
        state.token = data.token;
        state.refresh_token = data.refresh_token;
        state.expires = data.expires;
        state.category = data.category;
    },
    SET_TOKEN(state, data) {
        state.token = data.token;
        state.refresh_token = data.refresh_token;
        state.expires = data.expires;
    },
};

const actions = {
    async saveData({ dispatch }, data) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('expires', data.expires);
        localStorage.setItem('spot_Username', data.username);
        localStorage.setItem('category', data.category);
        dispatch('setDetails', data);
    },
    setDetails({ commit }, data) {
        commit("SET_DATA", data);
    },
    setToken({ commit }, data) {
        commit("SET_TOKEN", data);
    }
};

const module = {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
};

export default module;