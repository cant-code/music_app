<template>
  <v-app>
    <v-main>
      <login/>
    </v-main>
  </v-app>
</template>

<script>
import Login from '@/components/forms/login'
export default {
  components: {
    login: Login
  }
}
</script>