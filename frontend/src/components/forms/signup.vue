<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="10" sm="8" md="6" lg="5">
        <v-card elevation="12" class="pb-12 px-12 pt-6" theme="light">
          <v-img :src="image" class="mb-8 mx-auto" :aspect-ratio="1" width="60%"/>
          <v-form ref="form">
            <v-text-field :rules="[rules.required, rules.nameRule]" label="Username" variant="outlined" v-model="name"
                          :clearable=true prepend-inner-icon="mdi-account-music" class="mb-2"/>
            <v-text-field :rules="[rules.required, rules.emailRule]" label="Email" variant="outlined"
                          v-model="email" type="email" :clearable=true prepend-inner-icon="mdi-email" class="mb-2"/>
            <v-text-field :rules="[rules.required, rules.passRule]" label="Password"
                          :type="show ? 'text' : 'password'" variant="outlined"
                          v-model="password" @click:append-inner="show = !show"
                          :clearable=true :append-inner-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                          prepend-inner-icon="mdi-key-variant" class="mb-2"/>
            <v-text-field :rules="[rules.required, passComp]" label="Confirm Password"
                          :type="show2 ? 'text' : 'password'" variant="outlined"
                          v-model="password2" @click:append-inner="show2 = !show2"
                          :clearable=true :append-inner-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                          prepend-inner-icon="mdi-key-variant" class="mb-2"/>
            <v-alert v-if="message" type="error" class="mb-2">
              {{ message }}
            </v-alert>
            <div class="text-center">
              <v-btn type="submit" rounded size="large" color="primary" @click="validate" min-width="150">Signup</v-btn>
            </div>
          </v-form>
          <v-divider class="my-2"/>
          <p class="text-center mb-2">Have an account? <router-link to="login" tag="a"><a>Log in</a></router-link></p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Signup',
  beforeCreate() {
    if(this.$store.getters["auth/getUserToken"]) {
      this.$router.push('/');
    }
  },
  data: () => ({
    name: '',
    rules: {
      required: v => !!v || 'Field is Required',
      nameRule: v => /^[-\w.$@*!]{5,30}$/.test(v) || 'Incorrect Input',
      emailRule: v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      passRule: v => /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z_@./#&+-]{8,}$/.test(v)
          || 'Password must be alphanumeric having atleast one Uppercase character',
    },
    password: '',
    password2: '',
    email: '',
    show: false,
    show2: false,
    message: null,
    image: './src/assets/LOGO-resize.png',
  }),
  computed: {
    passComp() { return () => (this.password === this.password2) || 'Password doesnt match'; }
  },
  methods: {
    async validate(event) {
      event.preventDefault();
      let res = await this.$refs.form.validate();
      if(res.valid) {
        this.$store.dispatch('auth/registerUser',{
          username: this.name,
          password: this.password,
          password2: this.password2,
          email: this.email
        }).then(() => {this.$router.push('/login');}).catch(e => this.message = e.message);
      }
    }
  }
}

</script>