<template>
  <v-container>
    <v-row>
      <v-col v-for="(item, index) in categories" :key="index" cols=6 md=3 sm=4>
        <v-card :to="/genres/+item.id">
          <v-img :src="item.images[0].url" class="white--text align-end"
                 gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)">
            <v-card-title v-text="item.name"></v-card-title>
          </v-img>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      categories: ""
    };
  },
  methods: {
    async getCategories() {
      try {
        const response = await this.$axios.get("browse/featured-playlists");
        console.log(response);
        this.categories = response.data.playlists.items;
      } catch (e) {
        console.log(e);
      }
    }
  },
  created() {
    this.getCategories();
  }
}
</script>