import Axios from 'axios'

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
    SET_TOKEN(state, token) {
        state.token = token;
    }
};

const actions = {
    // eslint-disable-next-line no-unused-vars
    async getDetails({ commit }, data) {
        try {
            await Axios.post('http://localhost:8000/dj-rest-auth/registration/', {
                username: data.username,
                password1: data.password,
                password2: data.password2,
                email: data.email
            });
        } catch (error) {
            console.log(error);
        }
    },
    setDetails({ commit }, data) {
        commit("SET_DATA", data);
    },
    setToken({ commit }, token) {
        commit("SET_TOKEN", token);
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