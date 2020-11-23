<template>
  <v-app>
    <nav-drawer v-if="test"/>
    <v-main>
      <router-view/>
    </v-main>
    <foot v-if="spotify"/>
  </v-app>
</template>

<script>
import navDrawer from '@/components/Nav-Drawer';
import foot from '@/components/Footer';
export default {
  computed: {
    test() {
      return this.$store.getters["auth/getUserToken"];
    },
    spotify() {
      return this.$store.getters['spotify/getToken'].token;
    }
  },
  components: {
    navDrawer,
    foot
  }
}
</script>

<style>
html, body {
  scrollbar-width: thin !important;
}

::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background-color: #121212 !important;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background-color: #4db6ac;
}
</style>