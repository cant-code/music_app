<template>
  <v-navigation-drawer permanent :expand-on-hover=true app>
    <v-list-item class="pl-2">
      <v-list-item-avatar class="mx-auto">
        <v-img :src="image"/>
      </v-list-item-avatar>
    </v-list-item>
    <v-list-item>
      <v-list-item-icon>
        <v-icon dark>mdi-account</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="title">Hello {{getUser}}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-divider></v-divider>
    <v-list shaped>
      <v-list-item link to="/" active-class="primary">
        <v-list-item-icon>
          <v-icon dark>mdi-home</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title class="title">Home</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link to="/search" active-class="primary">
        <v-list-item-icon>
          <v-icon dark>mdi-magnify</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title class="title">Search</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link to="/settings" active-class="primary" v-if="!showSettings">
        <v-list-item-icon>
          <v-icon dark>mdi-hammer-wrench</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title class="title">Settings</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <template v-slot:append>
      <v-list-item link @click="logout">
        <v-list-item-icon><v-icon>mdi-logout</v-icon></v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title class="title">Logout</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </template>
  </v-navigation-drawer>
</template>

<script>
export default {
  data() {
    return {
      image: require('@/assets/LOGO-resize.png'),
    }
  },
  methods: {
    logout() {
        this.$store.dispatch('auth/logoutUser').then(() => {this.$router.push('/login');});
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