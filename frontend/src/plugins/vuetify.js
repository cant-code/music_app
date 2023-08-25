import {createVuetify} from "vuetify";
import 'vuetify/styles';
import colors from 'vuetify/lib/util/colors'

export default createVuetify({
    theme: {
        defaultTheme: 'dark',
        themes: {
            dark: {
                colors: {
                    primary: colors.teal.lighten2,
                    secondary: colors.red.darken3,
                    accent: colors.green.darken4,
                }
            }
        }
    },
});
