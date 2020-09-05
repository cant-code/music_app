import Axios from 'axios'

const state = {
    username: localStorage.getItem('username') || '',
    userToken: localStorage.getItem('userToken') || ''
};

const getters = {
    getUsername: (state) => {return state.username},
    getUserToken: (state) => {return state.userToken}
};

const mutations = {
    SET_USERNAME(state, token) {
        state.username = token;
    },
    SET_USER_TOKEN(state, token) {
        state.userToken = token;
    }
};

const actions = {
    // eslint-disable-next-line no-unused-vars
    async registerUser({ commit }, data) {
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
    async loginUser({ dispatch }, data) {
        try {
            const response = await Axios.post('http://localhost:8000/dj-rest-auth/login/', {
                username: data.username,
                password: data.password
            });
            dispatch('setUserToken', response.data.key);
            localStorage.setItem('userToken', response.data.key);
            const Token = response.data.key;
            const response2 = await Axios.get('http://localhost:8000/dj-rest-auth/user/', {
                headers: { 'Authorization': ' Token '+Token}});
            dispatch('setUsername', response2.data.username);
            localStorage.setItem('username', response2.data.username);
        } catch (error) {
            console.log(error);
        }
    },
    async logoutUser({ dispatch }) {
        try {
            await Axios.post('http://localhost:8000/dj-rest-auth/logout/', null, {
                headers: { 'Authorization': ' Token '+state.userToken}
            });
            dispatch('setUsername', '');
            dispatch('setUserToken', '');
            localStorage.clear();
        } catch (error) {
            console.log(error);
        }
    },
    setUsername({ commit }, token) {
        commit("SET_USERNAME", token);
    },
    setUserToken({ commit }, token) {
        commit("SET_USER_TOKEN", token);
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