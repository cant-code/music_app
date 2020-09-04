<template>
  <v-app>
    <nav-drawer v-if="test"/>
    <v-main>
      <router-view/>
    </v-main>
    <foot v-if="test"/>
  </v-app>
</template>

<script>
import navDrawer from '@/components/Nav-Drawer';
import foot from '@/components/Footer';
import {get} from "axios";
export default {
  async beforeCreate() {
    const response = await get('http://localhost:8000/get-token/');
    document.cookie = "csrftoken=" + response.data.token;
  },
  computed: {
    test() {
      return this.$store.getters["auth/getUserToken"];
    }
  },
  components: {
    navDrawer,
    foot
  }
}
</script>