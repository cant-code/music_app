<template>
  <v-footer padless rounded dark app>
    <v-row>
      <v-col class="py-0">
        <v-card>
          <v-slider :value="value" v-model="value" :max="this.songInfo.duration" :disabled="seekDisabled || !category"
                    class="ma-0 pa-0" height="1" thumb-label hide-details @mouseup="seekToPos">
            <template v-slot:thumb-label="{ value }">
              {{ millisToMinutesAndSeconds(value) }}
            </template>
          </v-slider>
          <v-row align="center">
            <v-col cols=4 class="py-0 text-left">
              <v-list-item>
                <v-list-item-avatar tile>
                  <v-img :src="songInfo.image"></v-img>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>{{songInfo.name}}</v-list-item-title>
                  <v-list-item-subtitle>{{songInfo.artists}}</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-icon>
                  <v-btn color="primary" icon @click="likeTrack">
                    <v-icon>{{ songInfo.liked }}</v-icon>
                  </v-btn>
                </v-list-item-icon>
              </v-list-item>
            </v-col>
            <v-col cols=4 class="pa-0">
              <v-list class="text-center">
                <v-list-item-icon :class="{ 'mx-0': $vuetify.breakpoint.smAndDown }">
                  <v-btn icon :disabled="!changeTrack.prev || !category" @click="playPrev">
                    <v-icon>mdi-rewind</v-icon>
                  </v-btn>
                </v-list-item-icon>
                <v-list-item-icon :class="{ 'mx-5': $vuetify.breakpoint.mdAndUp, 'mx-0': $vuetify.breakpoint.smAndDown }">
                  <v-btn icon @click="playback" :disabled="!category">
                    <v-icon v-if=play >mdi-play</v-icon>
                    <v-icon v-else>mdi-pause</v-icon>
                  </v-btn>
                </v-list-item-icon>
                <v-list-item-icon :class="{ 'ml-8': $vuetify.breakpoint.mdAndUp, 'mx-0': $vuetify.breakpoint.smAndDown }">
                  <v-btn icon :disabled="!changeTrack.next || !category" @click="playNext">
                    <v-icon>mdi-fast-forward</v-icon>
                  </v-btn>
                </v-list-item-icon>
              </v-list>
            </v-col>
            <v-col cols=4 class="py-0 text-right">
              <v-menu top offset-y :min-width="100" nudge-left="30">
                <template #activator="{ on, attrs }">
                  <v-btn icon @click="show=!show" v-bind="attrs" v-on="on" class="mx-3">
                    <v-icon>mdi-volume-high</v-icon>
                  </v-btn>
                </template>
                <v-slider v-model="volume" :disabled="seekDisabled || !category" :vertical=true :min=0 :max=100
                          thumb-label @mouseup="changeVol"/>
              </v-menu>
              <v-dialog max-width="350" v-model="dialogue">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn icon class="mr-13" @click="showDevices" v-bind="attrs" v-on="on">
                    <v-icon>mdi-devices</v-icon>
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title><h2>Devices</h2></v-card-title>
                  <hr/>
                  <v-list-item link v-for="item in devices.data"
                               :key="item.id" @click="transferPlayback(item.id, item.active)">
                    <v-list-item-title class="headline text-left">{{ item.name }}</v-list-item-title>
                    <v-list-item-icon class="ma-3 text-right">
                      <v-icon :color="item.active ? 'primary' : 'white'">{{ item.type }}</v-icon>
                    </v-list-item-icon>
                  </v-list-item>
                </v-card>
              </v-dialog>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  data() {
    return {
      dialogue: false,
      show: false,
      value: 0,
      interval: 0,
      volume: 100,
      play: true,
      seekDisabled: true,
      songInfo: {
        id: null,
        name: null,
        artists: null,
        image: null,
        duration: 100,
        liked: null,
      },
      changeTrack: {
        next: false,
        prev: false
      },
      devices: {'data': null},
      player: null,
    }
  },
  watch: {
    value (val) {
      if ((val < this.songInfo.duration) && (!this.play)) return;
      else if(val> this.songInfo.duration) {
        this.value = 0;
        clearInterval(this.interval);
      }
    },
  },
  computed: {
    category() {
      return this.$store.getters["spotify/getCategory"] === "premium";
    },
  },
  mounted() {
    if(this.$store.getters["spotify/getDetails"]) {
      const plugin = document.createElement("script");
      plugin.setAttribute(
          "src",
          "https://sdk.scdn.co/spotify-player.js"
      );
      document.body.appendChild(plugin);
      window.onSpotifyWebPlaybackSDKReady = () => {
        this.playerConnect();
      }
    }
  },
  beforeDestroy() {
    this.player.disconnect();
  },
  methods: {
    transferPlayback(id, active) {
      if((id === this.$store.getters["spotify/getDeviceID"]) && active) return
      this.$axios.put('me/player', {
        "device_ids": [id],
        "play": true
      }).then(() => this.dialogue = false).catch((e) => alert(e.message));
    },
    getType(type) {
      if(type === 'Computer') return 'mdi-laptop';
      else if(type === 'Smartphone') return 'mdi-cellphone';
      else return 'mdi-speaker';
    },
    showDevices() {
      this.$axios.get('me/player/devices').then((res) => {
        let data = [];
        res.data.devices.map((device) => {
          const type = this.getType(device.type);
          data.push({
            'id': device.id,
            'name': device.name,
            'type': type,
            'active': device.is_active
          })
        });
        this.devices = { 'data': data };
      });
    },
    playNext() {
      this.$axios.post('me/player/next');
    },
    playPrev() {
      this.$axios.post('me/player/previous');
    },
    changeVol() {
      this.$axios.put('me/player/volume?volume_percent='+this.volume);
    },
    seekToPos() {
      this.$axios.put('me/player/seek?position_ms='+this.value);
    },
    startBuffer () {
      clearInterval(this.interval)
      this.interval = setInterval(() => {
        if(!this.play) this.value += 1000;
      }, 1000)
    },
    playback() {
      if(this.play) {
        this.play = !this.play;
        this.startBuffer();
        this.$axios.put('me/player/play?device_id='+this.$store.getters["spotify/getDeviceID"])
      }
      else {
        this.play = !this.play;
        clearInterval(this.interval);
        this.$axios.put('me/player/pause');
      }
    },
    playerConnect() {
      const token = this.$store.getters["spotify/getToken"];
      // eslint-disable-next-line no-undef
      this.player = new Spotify.Player({
        name: 'Music Mixin',
        getOAuthToken: cb => {cb(token.token);}
      });
      this.player.addListener('authentication_error', () => {
        this.playerConnect();
      });
      this.player.addListener('ready', ({device_id}) => {
        this.$store.dispatch('spotify/setDeviceID', device_id);
      });
      this.player.connect();
      this.player.addListener('player_state_changed', ({
             track_window: {current_track, next_tracks, previous_tracks},
             paused,
           }) => {
        if (this.songInfo.name !== current_track.name) {
          this.seekDisabled = false;
          this.songInfo.id = current_track.id;
          this.songInfo.name = current_track.name;
          this.songInfo.artists = current_track.artists.map((val) => {
            return val.name;
          }).join(', ');
          this.songInfo.image = current_track.album.images[0].url || null;
          this.songInfo.duration = current_track.duration_ms;
          this.changeTrack.next = next_tracks.length > 0;
          this.changeTrack.prev = previous_tracks.length > 0;
          this.value = 0;
          this.startBuffer();
          this.$axios.get('me/tracks/contains?ids='+this.songInfo.id).then((response) => {
            this.songInfo.liked = response.data[0] ? 'mdi-heart' : 'mdi-heart-outline';
          })
        }
        this.play = paused;
      });
    },
    likeTrack() {
      if (this.songInfo.liked === 'mdi-heart-outline')
        this.$axios.put('me/tracks?ids=' + this.songInfo.id)
            .then(() => this.songInfo.liked = 'mdi-heart').catch(() => this.songInfo.liked = 'mdi-heart-outline');
      else
        this.$axios.delete('me/tracks?ids=' + this.songInfo.id)
            .then(() => this.songInfo.liked = 'mdi-heart-outline').catch(() => this.songInfo.liked = 'mdi-heart');
    },
    millisToMinutesAndSeconds(millis) {
      const minutes = Math.floor(millis / 60000);
      const seconds = ((millis % 60000) / 1000).toFixed(0);
      return (seconds == 60 ? (minutes+1) + ":00" : minutes + ":" + (seconds < 10 ? "0" : "") + seconds);
    },
  }
}
</script>