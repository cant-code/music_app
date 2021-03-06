import Axios from 'axios'
Axios.defaults.xsrfCookieName = 'csrftoken'
Axios.defaults.xsrfHeaderName = 'X-CSRFToken'

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
               await Axios.post('/dj-rest-auth/registration/', {
                    username: data.username,
                    password1: data.password,
                    password2: data.password2,
                    email: data.email
                });
        } catch (error) {
            throw new Error('Error Occurred, please try again later');
        }
    },
    async loginUser({ dispatch }, data) {
        try {
            const response = await Axios.post('/dj-rest-auth/login/', {
                username: data.username,
                password: data.password
            });
            dispatch('setUserToken', response.data.key);
            localStorage.setItem('userToken', response.data.key);
            const Token = response.data.key;
            const response2 = await Axios.get('/dj-rest-auth/user/', {
                headers: { 'Authorization': ' Token '+Token}});
            dispatch('setUsername', response2.data.username);
            localStorage.setItem('username', response2.data.username);
            Axios.get('/spotify/get_data/', {
                headers: { 'Authorization': ' Token '+Token}}).then(async ({data}) => {
                const params = {
                    "token": data.access_token,
                    "refresh_token": data.refresh_token,
                    "expires": data.expires_at,
                    "username": data.sp_name,
                    "category": data.category
                };
                await dispatch("spotify/saveData", params, {root: true});
            }).catch(e => console.log(e));
        } catch (error) {
            throw new Error('Invalid User, please try again');
        }
    },
    async logoutUser({ dispatch }) {
        try {
            await Axios.post('/dj-rest-auth/logout/', null, {
                headers: { 'Authorization': ' Token '+state.userToken}
            });
            dispatch('setUsername', '');
            dispatch('setUserToken', '');
            dispatch('spotify/saveData', {
                'token': '',
                'refresh_token': '',
                'expires': '',
                'username': '',
                'category': '',
            }, { root: true });
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