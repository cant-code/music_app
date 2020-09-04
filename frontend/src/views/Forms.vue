<template>
  <login v-if="displayPage"/>
  <signup v-else/>
</template>

<script>
import Login from '@/components/forms/login'
import Signup from '@/components/forms/signup'
export default {
  components: {
    login: Login,
    signup: Signup
  },
  computed: {
    displayPage() {
      return this.$route.path === '/login';
    }
  }
}
</script>