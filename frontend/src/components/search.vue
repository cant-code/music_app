<template>
  <v-container>
    <v-text-field v-model="searchTerm" hide-details label="Search" outlined></v-text-field>
    <v-btn @click="search" class="my-2">Search</v-btn>
    <hr/>
    <section>
      <h2>Albums</h2>
      <v-sheet class="mx-auto" elevation="8">
        <v-slide-group class="pa-4" v-if="albums.total > 0">
          <v-slide-item v-for="item in albums.items" :key="item.id">
            <v-card class="ma-2" width="250px" height="250px" :to="/albums/+item.id">
              <v-img :src="item.images[0].url" v-if="item.images[0].url" class="white--text align-end"
                     gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)">
                <v-card-title v-text="item.name"></v-card-title>
              </v-img>
            </v-card>
          </v-slide-item>
        </v-slide-group>
        <v-alert v-else type="error">No Results found</v-alert>
      </v-sheet>
    </section>
    <section>
      <h2>Tracks</h2>
      <v-sheet class="mx-auto" elevation="8">
        <v-slide-group class="pa-4" v-if="tracks.total > 0">
          <v-slide-item v-for="item in tracks.items" :key="item.id">
            <v-card class="ma-2" width="250px" height="250px" @click="track(item.id)">
              <v-img :src="item.album.images[0].url" v-if="item.album.images[0].url" class="white--text align-end"
                     gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)">
                <v-card-title v-text="item.name"></v-card-title>
              </v-img>
            </v-card>
          </v-slide-item>
        </v-slide-group>
        <v-alert v-else type="error">No Results found</v-alert>
      </v-sheet>
    </section>
    <section>
      <h2>Playlists</h2>
      <v-sheet class="mx-auto" elevation="8">
        <v-slide-group class="pa-4" v-if="playlists.total > 0">
          <v-slide-item v-for="item in playlists.items" :key="item.id">
            <v-card class="ma-2" width="250px" height="250px" :to="/playlists/+item.id">
              <v-img :src="item.images[0].url" v-if="item.images[0].url" class="white--text align-end"
                     gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)">
                <v-card-title v-text="item.name"></v-card-title>
              </v-img>
            </v-card>
          </v-slide-item>
        </v-slide-group>
        <v-alert v-else type="error">No Results found</v-alert>
      </v-sheet>
    </section>
  </v-container>
</template>

<script>
export default {
  name: "Search",
  data() {
    return {
      searchTerm: null,
      albums: {},
      playlists: {},
      artists: {},
      tracks: {}
    }
  },
  methods: {
    search() {
      this.$axios.get('search?q='+this.searchTerm+'&type=album,artist,playlist,track').then((res) => {
            this.albums = { 'total': res.data.albums.total, 'items': res.data.albums.items };
            this.playlists = { 'total': res.data.playlists.total, 'items': res.data.playlists.items };
            this.artists = { 'total': res.data.artists.total, 'items': res.data.artists.items };
            this.tracks = { 'total': res.data.tracks.total, 'items': res.data.tracks.items };
          }).catch(e => console.log(e));
    },
    async track(clickedId) {
      try {
        await this.$axios.put('me/player/play?device_id=' + this.$store.getters["spotify/getDeviceID"], {
          "uris": ["spotify:track:"+clickedId],
        }).then(() => {
          console.log('Playing');
        });
      } catch (e) {
        console.log(e);
      }
    }
  }
}
</script>

<style scoped>

</style>