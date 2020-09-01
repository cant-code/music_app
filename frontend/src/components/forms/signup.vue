<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card elevation="12" class="pa-12" color="white">
          <h2 class="text-h2 mb-7 text-center primary--text">SignUp</h2>
          <v-divider class="mb-4"/>
          <v-form ref="form">
            <v-text-field :rules="[rules.required, rules.nameRule]" label="Username"
                          :outlined=true v-model="name"
                          :rounded=true :clearable=true
                          prepend-inner-icon="mdi-account-music"/>
            <v-text-field :rules="[rules.required, rules.emailRule]" label="Email"
                          :outlined=true v-model="email" type="email"
                          :rounded=true :clearable=true
                          prepend-inner-icon="mdi-email"/>
            <v-text-field :rules="[rules.required, rules.passRule]" label="Password"
                          :type="show ? 'text' : 'password'" :outlined=true
                          v-model="password" @click:append="show = !show"
                          :rounded=true :clearable=true :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                          prepend-inner-icon="mdi-key-variant"/>
            <v-text-field :rules="[rules.required, passComp]" label="Confirm Password"
                          :type="show2 ? 'text' : 'password'" :outlined=true
                          v-model="password2" @click:append="show2 = !show2"
                          :rounded=true :clearable=true :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                          prepend-inner-icon="mdi-key-variant"/>
            <v-btn rounded large color="primary" dark @click="validate">Login</v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Signup',
  data: () => ({
    name: '',
    rules: {
      required: v => !!v || 'Field is Required',
      nameRule: v => (v && v.length >= 8) || 'Name must be atleast 8 characters',
      emailRule: v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      passRule: v => /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z_@./#&+-]{8,}$/.test(v)
          || 'Password must be alphanumeric having atleast one Uppercase character',
    },
    password: '',
    password2: '',
    email: '',
    show: false,
    show2: false
  }),
  computed: {
    passComp() { return () => (this.password === this.password2) || 'Password doesnt match'; }
  },
  methods: {
    validate() {
      console.log(this.$refs.form.validate());
    }
  }
}
</script>