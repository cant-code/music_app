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
            <h2><span>Description: {{ this.description}}</span></h2>
            <div><span>Followers: {{this.followers}}</span></div>
          </div>
          <div>
            <v-btn :disabled="!category" class="ma-2" x-large icon color="primary" @click="playlist">
              <v-icon x-large>mdi-play-circle</v-icon>
            </v-btn>
            <v-btn class="ma-2" x-large icon color="primary" @click="likePlaylist">
              <v-icon x-large>{{ liked }}</v-icon>
            </v-btn>
          </div>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-list>
        <v-list-item link v-for="(item) in filteredArray" :key="item.track.id" color="primary"
                     @click="track(item.track.id)" :input-value="currentlyPlaying === item.track.id">
          <v-list-item-avatar v-if="item.track.album.images[0]">
            <v-img alt="Not Found" :src="item.track.album.images[0].url"></v-img>
          </v-list-item-avatar>
          <v-list-item-title>{{ item.track.name }}</v-list-item-title>
          <v-list-item-subtitle class="text-right">
            {{ artists(item.track.artists) }}
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "genres",
  computed: {
    filteredArray() {
      return this.playlists.items.filter(item => {
        return item.track !== null;
      });
    },
    category() {
      return this.$store.getters["spotify/getCategory"] === "premium";
    },
    currentlyPlaying() {
      return this.$store.getters["player/getCurrentlyPlaying"];
    },
  },
  updated() {
    this.isMore = false;
  },
  data() {
    return {
      value: true,
      image: '',
      name: '',
      categoryID: null,
      followers: null,
      description: null,
      liked: null,
      owner: null,
      playlists: {
        limit: 25,
        offset: 0,
        total: 1,
        items: []
      },
      isMore: true,
    };
  },
  methods: {
    async getCategoryPlaylists() {
      try {
        if (this.playlists.total > this.playlists.offset) {
          const response = await this.$axios.get(`playlists/${this.categoryID}`);
          console.log(response);
          this.name = response.data.name;
          this.image = response.data.images[0].url;
          this.owner = response.data.owner.display_name;
          this.followers = response.data.followers.total.toLocaleString();
          this.description = response.data.description;
          const playlists = response.data.tracks;
          this.playlists.total = playlists.total;
          this.playlists.items.push(...playlists.items);
          this.$axios.get('/playlists/'+this.categoryID+'/followers/contains?ids='
              +this.$store.getters["spotify/getDetails"].username).then((response) => {
              this.liked = response.data[0] ? 'mdi-heart' : 'mdi-heart-outline';
          });
          this.isMore = false;
        }
      } catch (e) {
        console.log(e);
      }
    },
    likePlaylist() {
      if (this.liked === 'mdi-heart-outline')
        this.$axios.put('playlists/' + this.categoryID + '/followers', {
          "public": false
        }).then(() => this.liked = 'mdi-heart').catch(() => this.liked = 'mdi-heart-outline');
      else
        this.$axios.delete('playlists/' + this.categoryID + '/followers')
            .then(() => this.liked = 'mdi-heart-outline').catch(() => this.liked = 'mdi-heart');
    },
    artists(artistList) {
      return artistList.map((val) => {
        return val.name;
      }).join(', ');
    },
    async playlist() {
      try {
        await this.$store.dispatch('player/setData', {
          player: 'spotify',
          id: this.categoryID,
          type: 'playlist'
        });
        this.$axios.put('me/player/play?device_id='+this.$store.getters["spotify/getDeviceID"], {
          "context_uri": "spotify:playlist:"+this.categoryID,
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
          "context_uri": "spotify:playlist:"+this.categoryID,
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
    this.categoryID = id;
    this.getCategoryPlaylists();
  }
};
</script>