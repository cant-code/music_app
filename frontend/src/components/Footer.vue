<template>
  <v-footer padless rounded dark app>
    <v-row>
      <v-col class="py-0">
        <v-card>
          <v-slider :value="value" v-model="value" :max="this.songInfo.duration" :disabled="seekDisabled"
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
              </v-list-item>
            </v-col>
            <v-col cols=4 class="pa-0 text-center">
              <v-list-item-icon :class="{ 'mx-0': $vuetify.breakpoint.smAndDown }">
                <v-btn icon>
                  <v-icon>mdi-rewind</v-icon>
                </v-btn>
              </v-list-item-icon>
              <v-list-item-icon :class="{ 'mx-5': $vuetify.breakpoint.mdAndUp, 'mx-0': $vuetify.breakpoint.smAndDown }">
                <v-btn icon @click="playback">
                  <v-icon v-if=play >mdi-play</v-icon>
                  <v-icon v-else>mdi-pause</v-icon>
                </v-btn>
              </v-list-item-icon>
              <v-list-item-icon :class="{ 'ml-8': $vuetify.breakpoint.mdAndUp, 'mx-0': $vuetify.breakpoint.smAndDown }">
                <v-btn icon>
                  <v-icon>mdi-fast-forward</v-icon>
                </v-btn>
              </v-list-item-icon>
            </v-col>
            <v-col cols=4 class="py-0 text-center">
              <v-menu top offset-y :min-width="100" nudge-left="30">
                <template #activator="{ on, attrs }">
                  <v-btn icon @click="show=!show" v-bind="attrs" v-on="on">
                    <v-icon>mdi-volume-high</v-icon>
                  </v-btn>
                </template>
                <v-slider v-model="volume" :disabled="seekDisabled" :vertical=true :min=0 :max=100
                          thumb-label @mouseup="changeVol"/>
              </v-menu>
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
      show: false,
      value: 0,
      interval: 0,
      volume: 100,
      play: true,
      seekDisabled: true,
      songInfo: {
        name: null,
        artists: null,
        image: null,
        duration: 100,
      },
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
  methods: {
    changeVol() {
      this.$axios.put('me/player/volume?volume_percent='+this.volume).then(() => {console.log('Volume Changed')});
    },
    seekToPos() {
      this.$axios.put('me/player/seek?position_ms='+this.value).then(() => {console.log('Seeked playback')});
    },
    startBuffer () {
      clearInterval(this.interval)
      this.interval = setInterval(() => {
        this.value += 1000
      }, 1000)
    },
    playback() {
      if(this.play) {
        this.play = !this.play;
        this.startBuffer();
        console.log('Changed', this.$store.getters["spotify/getDeviceID"]);
        this.$axios.put('me/player/play?device_id='+this.$store.getters["spotify/getDeviceID"])
            .then(() => {console.log('Playing');});
      }
      else {
        this.play = !this.play;
        clearInterval(this.interval);
        console.log('Changed', this.$store.getters["spotify/getDeviceID"]);
        this.$axios.put('me/player/pause').then(() => {console.log('Paused');});
      }
    },
    playerConnect() {
      const token = this.$store.getters["spotify/getToken"];
      // eslint-disable-next-line no-undef
      const player = new Spotify.Player({
        name: 'Music Mixin',
        getOAuthToken: cb => {cb(token.token);}
      });
      player.addListener('authentication_error', ({message}) => {
        console.error(message);
        this.playerConnect();
      });
      player.addListener('ready', ({device_id}) => {
        console.log('Ready with Device ID', device_id);
        this.$store.dispatch('spotify/setDeviceID', device_id);
      });
      player.connect();
      player.addListener('player_state_changed', ({
             track_window: {current_track},
             position,
             paused,
           }) => {
        console.log('Currently Playing', current_track);
        if (position === 0) {
          this.seekDisabled = false;
          this.songInfo.name = current_track.name;
          this.songInfo.artists = current_track.artists.map((val) => {
            return val.name;
          }).join(', ');
          this.songInfo.image = current_track.album.images[0].url || null;
          this.songInfo.duration = current_track.duration_ms;
          this.startBuffer();
        }
        this.play = paused;
      });
    },
    millisToMinutesAndSeconds(millis) {
      const minutes = Math.floor(millis / 60000);
      const seconds = ((millis % 60000) / 1000).toFixed(0);
      return (seconds == 60 ? (minutes+1) + ":00" : minutes + ":" + (seconds < 10 ? "0" : "") + seconds);
    },
  }
}
</script>