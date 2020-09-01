import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        dark: true,
        themes: {
            dark: {
                primary: colors.teal.lighten2,
                secondary: colors.red.darken3,
                accent: colors.green.darken4,
            }
        }
    },
});
