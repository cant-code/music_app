<template>
  <v-navigation-drawer permanent expand-on-hover rail>
    <v-list>
      <v-list-item class="pl-2">
        <v-list-item-media class="mx-auto">
          <v-img :src="image"/>
        </v-list-item-media>
      </v-list-item>
      <v-list-item prepend-icon="mdi-account" value="hello" disabled>
        <v-list-item-title class="title">Hello {{ getUser }}</v-list-item-title>
      </v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list shaped>
      <v-list-item prepend-icon="mdi-home" link to="/" active-class="primary">
        <v-list-item-title class="title">Home</v-list-item-title>
      </v-list-item>
      <v-list-item prepend-icon="mdi-magnify" link to="/search" active-class="primary">
        <v-list-item-title class="title">Search</v-list-item-title>
      </v-list-item>
      <v-list-item prepend-icon="mdi-hammer-wrench" link to="/settings" active-class="primary" v-if="!showSettings">
        <v-list-item-title class="title">Settings</v-list-item-title>
      </v-list-item>
    </v-list>
    <template v-slot:append>
      <v-list>
        <v-list-item prepend-icon="mdi-logout" link @click="logout">
          <v-list-item-title class="title">Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </template>
  </v-navigation-drawer>
</template>

<script>
export default {
  data() {
    return {
      image: '/src/assets/LOGO-resize.png',
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('auth/logoutUser').then(() => {
        this.$router.push('/login');
      });
    },
  },
  computed: {
    getUser() {
      return this.$store.getters["auth/getUsername"];
    },
    showSettings() {
      return this.$store.getters['spotify/getDetails'].username;
    }
  }
}
</script>