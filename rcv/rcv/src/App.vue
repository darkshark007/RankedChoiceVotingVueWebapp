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
    },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>