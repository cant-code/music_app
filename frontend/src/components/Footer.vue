<template>
  <v-footer padless rounded dark app>
    <v-row>
      <v-col class="py-0">
        <v-card>
          <v-slider :value="50" class="ma-0 pa-0" height="1" thumb-label dense hide-details/>
          <v-row align="center">
            <v-col cols=4 class="py-0 text-left">
              <v-list-item>
                <v-list-item-avatar tile>
                  <v-img src="https://cdn.vuetifyjs.com/images/cards/halcyon.png"></v-img>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>The Walker</v-list-item-title>
                  <v-list-item-subtitle>Fitz & The Trantrums</v-list-item-subtitle>
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
                <v-btn icon>
                  <v-icon v-if=play @click="play = !play">mdi-play</v-icon>
                  <v-icon v-else @click="play = !play">mdi-pause</v-icon>
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
                <v-slider v-model="volume" :vertical=true :min=0 :max=100 thumb-label/>
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
      volume: 0,
      play: true
    }
  }
}
</script>