<template>
  <v-footer padless rounded dark app>
    <v-row>
      <v-col class="py-0">
        <v-card>
          <v-slider :value="songInfo.pos" :max="songInfo.duration" :disabled="seekDisabled"
                    class="ma-0 pa-0" height="1" thumb-label hide-details>
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
              <v-speed-dial direction="top" :open-on-hover=true transition="slide-y-reverse-transition">
                <template v-slot:activator>
                  <v-btn dark icon>
                    <v-icon>mdi-volume-high</v-icon>
                  </v-btn>
                </template>
                <v-slider v-model="volume" :disabled="seekDisabled" :vertical=true :min=0 :max=100 thumb-label/>
              </v-speed-dial>
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
      volume: 100,
      play: true,
      seekDisabled: true,
      songInfo: {
        name: null,
        artists: null,
        image: null,
        pos: 0,
        duration: 100,
      },
    }
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
    playback() {
      if(this.play) {
        this.play = !this.play;
        console.log('Changed', this.$store.getters["spotify/getDeviceID"]);
        this.$axios.put('me/player/play?device_id='+this.$store.getters["spotify/getDeviceID"])
            .then(() => {console.log('Playing');});
      }
      else {
        this.play = !this.play;
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