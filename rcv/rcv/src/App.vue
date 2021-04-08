<template>
  <div>
      <menu-bar-top/>
      <div>
          <menu-bar-left/>
          <router-view></router-view>
      </div>
  </div>
</template>

<script>
import MenuBarLeft from './components/MenuBarLeft.vue'
import MenuBarTop from './components/MenuBarTop.vue';

export default {
    components: {
        'menu-bar-left': MenuBarLeft,
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
        };
        fetch(`api/create_or_update_poll/`, data);

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
  margin-top: 60px;
}
</style>