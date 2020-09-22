module.exports = {
  "devServer": {
    "proxy": {
      "/dj-rest-auth" : {
        target: "http://localhost:8000",
        changeOrigin: true
      },
      "/spotify" : {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  },
  "transpileDependencies": [
    "vuetify"
  ],
  outputDir: './dist/',
  assetsDir: 'static',
}