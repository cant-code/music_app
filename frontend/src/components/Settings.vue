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
let windowObjectReference = null;
let previousUrl = null;
let name = 'Spotify';
export default {
  methods: {
      async openSignInWindow () {
        await Axios.get('http://localhost:8000/spotify/gettoken/', {
          headers: { 'Authorization': ' Token '+this.$store.getters["auth/getUserToken"]}
        }).then((url) => {
          console.log(url);
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
      receiveMessage(event) {
        const { data } = event;
        console.log(data);
        if (data.source === 'lma-login-redirect') {
          const { payload } = data;
          console.log(payload);
          // const redirectUrl = `/auth/google/login${payload}`;
          // console.log(redirectUrl);
          // window.location.pathname = redirectUrl;
        }
      }
  },
}
</script>