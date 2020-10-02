<template>
  <v-container>
    <v-card :loading="isMore">
      <v-row color="secondary">
        <v-col cols="3">
          <v-img class="text-left pa-1 mx-auto" aspect-ratio="1" :src="this.image"></v-img>
        </v-col>
        <v-divider vertical></v-divider>
        <v-col>
          <div>
            <h1>{{ this.name }}</h1>
            <h2><span>Label: {{ this.label}}</span></h2>
            <div><span>Popularity: {{this.popularity}}</span></div>
          </div>
          <div>
            <v-btn :disabled="!category" class="ma-2" x-large icon color="primary" @click="album">
              <v-icon x-large>mdi-play-circle</v-icon>
            </v-btn>
            <v-btn class="ma-2" x-large icon color="primary" @click="likeAlbum">
              <v-icon x-large>{{ liked }}</v-icon>
            </v-btn>
          </div>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-list>
        <v-list-item link v-for="(item, index) in filteredArray" :key="index" @click="track(item.id)">
          <v-list-item-title>{{ item.name }}</v-list-item-title>
          <v-list-item-subtitle class="text-right">
            {{ artists(item.artists) }}
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "Albums",
  computed: {
    filteredArray() {
      return this.albums.items.filter(item => {
        return item !== null;
      });
    },
    category() {
      return this.$store.getters["spotify/getCategory"] === "premium";
    }
  },
  updated() {
    this.isMore = false;
  },
  data() {
    return {
      value: true,
      image: '',
      name: '',
      albumID: null,
      popularity: null,
      album_type: null,
      liked: null,
      label: null,
      albums: {
        total: 1,
        items: []
      },
      isMore: true
    };
  },
  methods: {
    async getAlbum() {
      try {
          const response = await this.$axios.get(`albums/${this.albumID}`);
          console.log(response)
          this.name = response.data.name;
          this.image = response.data.images[0].url;
          this.label = response.data.label;
          this.popularity = response.data.popularity+'%';
          this.album_type = response.data.album_type;
          const playlists = response.data.tracks;
          this.albums.total = playlists.total;
          this.albums.items.push(...playlists.items);
          this.$axios.get('me/albums/contains?ids=' +this.albumID)
              .then((response) => {
                this.liked = response.data[0] ? 'mdi-heart' : 'mdi-heart-outline';
              });
          this.isMore = false;
      } catch (e) {
        console.log(e);
      }
    },
    likeAlbum() {
      if (this.liked === 'mdi-heart-outline')
        this.$axios.put('albums?ids=' + this.albumID)
            .then(() => this.liked = 'mdi-heart').catch(() => this.liked = 'mdi-heart-outline');
      else
        this.$axios.delete('albums?ids=' + this.albumID)
            .then(() => this.liked = 'mdi-heart-outline').catch(() => this.liked = 'mdi-heart');
    },
    artists(artistList) {
      return artistList.map((val) => {
        return val.name;
      }).join(', ');
    },
    async album() {
      try {
        await this.$store.dispatch('player/setData', {
          player: 'spotify',
          id: this.albumID,
          type: 'album'
        });
        this.$axios.put('me/player/play?device_id='+this.$store.getters["spotify/getDeviceID"], {
          "context_uri": "spotify:album:"+this.albumID,
        }).then(() => {console.log('Playing');});
      }
      catch (e) {
        console.log(e);
      }
    },
    async track(clickedId) {
      try {
        await this.$store.dispatch('player/setData', {
          player: 'spotify',
          id: clickedId,
          type: 'track'
        });
        this.$axios.put('me/player/play?device_id=' + this.$store.getters["spotify/getDeviceID"], {
          "context_uri": "spotify:album:"+this.albumID,
          "offset": {"uri":"spotify:track:" + clickedId},
        }).then(() => {
          console.log('Playing');
        });
      } catch (e) {
        console.log(e);
      }
    }
  },
  created() {
    const {id} = this.$route.params;
    this.albumID = id;
    this.getAlbum();
  }
};
</script>