import Axios from "axios";

const state = {
    spot_Username: localStorage.getItem('spot_Username') || '',
    token: localStorage.getItem('token') || '',
    refresh_token: localStorage.getItem('refresh_token') || '',
    expires: localStorage.getItem('expires') || '',
    category: localStorage.getItem('category') || '',
    device_id: ''
};

const getters = {
    getDetails: (state) => {
        return {
            username: state.spot_Username,
            category: state.category
        }
    },
    getExpiry: (state) => {return {expires: state.expires}},
    getToken: (state) => {return {token: state.token}},
    getDeviceID: (state) => {return state.device_id}
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
    SET_DEVICEID(state, data) {
        state.device_id = data;
    }
};

const actions = {
    async refreshToken({dispatch, rootGetters}){
        await Axios.get('http://localhost:8000/spotify/refresh_token/', {
            headers: {'Authorization': ' Token ' + rootGetters["auth/getUserToken"] }
        }).then(({data}) => {
            console.log(data);
            const params = {
                "token": data.access_token,
                "refresh_token": data.refresh_token,
                "expires": data.expires_at,
            };
            dispatch('setToken', params).then(() => {
                console.log('Success');
            });
        });
    },
    async saveData({ commit }, data) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('expires', data.expires);
        localStorage.setItem('spot_Username', data.username);
        localStorage.setItem('category', data.category);
        commit("SET_DATA", data);
    },
    setToken({ commit }, data) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('expires', data.expires);
        commit("SET_TOKEN", data);
    },
    setDeviceID({commit}, data) {
        commit("SET_DEVICEID", data);
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