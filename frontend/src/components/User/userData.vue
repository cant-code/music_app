<template>
  <v-container>
    <button @click="getPlaylists">Click me</button>
    <button @click="getAlbums">Click me</button>
    <button @click="getTracks">Click me</button>
  </v-container>
</template>

<script>
export default {
  methods: {
    async getPlaylists() {
      try {
        const res = await this.$axios.get('me/playlists');
        console.log(res);
      }
      catch (e) {
        console.log(e);
      }
    },
    async getTracks() {
      try {
        const res = await this.$axios.get('me/tracks');
        console.log(res);
      }
      catch (e) {
        console.log(e);
      }
    },
    async getAlbums() {
      try {
        const res = await this.$axios.get('me/albums');
        console.log(res);
      }
      catch (e) {
        console.log(e);
      }
    },
  }
}
</script>