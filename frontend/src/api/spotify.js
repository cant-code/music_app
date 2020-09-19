import Axios from 'axios';
import store from '@/store'

const instance = Axios.create({
    baseURL: 'https://api.spotify.com/v1/',
})

instance.interceptors.request.use( (config) => {
    if (store.getters["spotify/getToken"]) {
        config.headers.common["Authorization"] = `Bearer ${store.getters["spotify/getToken"].token}`;
    }
    return config;
}, null);

function createResponseInterceptor () {
    const interceptor = instance.interceptors.response.use(response => response,
        (error) => {
        // reject promise if custom error
        console.log(error.response);
        if (error.response.status !== 401) {
            return Promise.reject(error);
        }
        instance.interceptors.response.eject(interceptor);
        return store.dispatch('spotify/refreshToken').then(() => {
            error.response.config.headers['Authorization'] = `Bearer ${store.getters["spotify/getToken"].token}`;
            return instance(error.response.config);
        }).catch(e => {
            console.log(e);
            store.dispatch('auth/logoutUser').then(() => {
                this.router.push('/login');
            });
            return Promise.reject(e);
        }).finally(createResponseInterceptor);
    });
}

createResponseInterceptor();

export default instance;