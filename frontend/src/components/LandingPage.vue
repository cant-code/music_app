<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12">
        Please Wait...
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  mounted() {
    const params = window.location.search;
    if (window.opener) {
      window.opener.postMessage(params);
      window.close();
    }
  }
}
</script>