<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card class="mx-auto" outlined color="primary" max-width="300px">
          <v-list-item link @click="openSignInWindow">
            <v-list-item-icon>
              <v-icon>mdi-spotify</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Connect Spotify</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Axios from "axios";
Axios.defaults.xsrfCookieName = 'csrftoken'
Axios.defaults.xsrfHeaderName = 'X-CSRFToken'
let windowObjectReference = null;
let previousUrl = null;
let name = 'Spotify';
export default {
  methods: {
      openSignInWindow () {
        Axios.get('/spotify/gettoken/', {
          headers: { 'Authorization': ' Token '+this.$store.getters["auth/getUserToken"]}
        }).then((url) => {
          window.removeEventListener('message', this.receiveMessage);
          const strWindowFeatures = 'toolbar=no, menubar=no, width=600, height=700, top=100, left=100';
          if (windowObjectReference === null || windowObjectReference.closed) {
            windowObjectReference = window.open(url.data, name, strWindowFeatures);
          } else if (previousUrl !== url) {
            windowObjectReference = window.open(url.data, name, strWindowFeatures);
            windowObjectReference.focus();
          } else {
            windowObjectReference.focus();
          }
          window.addEventListener('message', event => this.receiveMessage(event), false);
          previousUrl = url;
        });
      },
      async receiveMessage(event) {
        if (event.data) {
          if (event.data.startsWith('?code')) {
            const {data} = event;
            let code = data.split("?code=")[1].split("&")[0]
            await Axios.get('/spotify/auth/', {
              params: {code: code},
              headers: {'Authorization': ' Token ' + this.$store.getters["auth/getUserToken"]}
            }).then(({data}) => {
              const params = {
                "token": data.access_token,
                "refresh_token": data.refresh_token,
                "expires": data.expires_at,
                "username": data.user.id,
                "category": data.user.product
              };
              this.$store.dispatch("spotify/saveData", params).then(() => this.$router.push('/'));
            });
          }
        }
      }
  },
}
</script>