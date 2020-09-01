<template>
  <v-navigation-drawer permanent :expand-on-hover=true app>
    <v-list-item>
      <v-list-item-icon>
        <v-icon dark>mdi-account</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="title">Hello, {{user}}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-divider></v-divider>
    <v-list-item link>
      <v-list-item-icon>
        <v-icon dark>mdi-home</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="title">Home</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item link>
      <v-list-item-icon>
        <v-icon dark>mdi-hammer-wrench</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="title">Settings</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <template v-slot:append>
      <v-list-item link to="about">
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
      user: "User",
    }
  }
}
</script>