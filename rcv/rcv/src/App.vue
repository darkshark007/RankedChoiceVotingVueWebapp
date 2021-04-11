<template>
  <v-app>
    <div>
        <menu-bar-top/>
        <div>
            <router-view></router-view>
        </div>
    </div>
  </v-app>
</template>

<script>
import MenuBarTop from './components/MenuBarTop.vue';
import Utils from './utils.js';

export default {
    components: {
        'menu-bar-top': MenuBarTop,
    },
    data: () => {
        return {
            title: 'Welcome to My Journalzzz',
            days: [1,2,3,4],
          };
    },
    mounted: () => {

        let data = {
            'fish': 'trout',
            'nested': {
              'bird': 'swallow',
            }
        };
        Utils.post(`api/create_or_update_poll/`, data);

    },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>