<template>
  <v-app>
    <nav-drawer/>
    <v-main></v-main>
    <foot/>
  </v-app>
</template>

<script>
import navDrawer from '@/components/Nav-Drawer';
import foot from '@/components/Footer';
export default {
  components: {
    navDrawer,
    foot
  }
}
</script>
