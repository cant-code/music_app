<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="10" sm="8" md="6" lg="5">
        <v-card elevation="24" class="pb-12 px-12 pt-6" light>
          <v-img :src="image" class="mb-8 mx-auto" :aspect-ratio="1" width="60%"/>
          <v-form ref="form">
            <v-text-field label="Username" :rules="[rules.required]" :outlined=true v-model="name"
                          :rounded=true :clearable=true prepend-inner-icon="mdi-account-music"/>
            <v-text-field label="Password" :type="show ? 'text' : 'password'" :rules="[rules.required]"
                          :outlined=true v-model="password" @click:append="show = !show"
                          :rounded=true :clearable=true :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                          prepend-inner-icon="mdi-key-variant"/>
            <v-alert v-if="message" type="error">
              {{ message }}
            </v-alert>
            <div class="text-center">
              <v-btn type="submit" rounded large color="primary" @click="validate" min-width="150">Login</v-btn>
            </div>
          </v-form>
          <v-divider class="my-2"/>
          <p class="text-center text-h5">Don't have an account?</p>
          <v-btn rounded outlined large block color="secondary" to="signup" min-width="150">Signup</v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Login',
  beforeCreate() {
    if(this.$store.getters["auth/getUserToken"]) {
      this.$router.push('/');
    }
  },
  data: () => ({
    name: '',
    rules: {
      required: v => !!v || 'Field is Required',
    },
    password: '',
    show: false,
    message: null,
    image: require('@/assets/LOGO-resize.png'),
  }),
  methods: {
    async validate(event) {
      event.preventDefault();
      if(this.$refs.form.validate()) {
        await this.$store.dispatch('auth/loginUser', {
          username: this.name,
          password: this.password
        }).then(() => this.$router.push('/')).catch(e => this.message = e.message)
      }
    }
  },
}
</script>

<style>
/*.v-main__wrap {*/
/*  background: rgb(0,212,255);*/
/*  background: radial-gradient(circle, rgba(0,212,255,1) 0%, rgba(2,0,36,1) 52%);*/
/*}*/
</style>