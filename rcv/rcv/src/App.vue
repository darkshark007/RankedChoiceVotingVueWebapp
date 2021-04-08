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
// import HelloWorld from './components/HelloWorld.vue'
import MenuBarLeft from './components/MenuBarLeft.vue'
import MenuBarTop from './components/MenuBarTop.vue';
import RedPoll from './components/RedPoll.vue';
// import Poll from './components/Poll.vue';
// import Test from './components/Test.vue';


console.log(">>> RedPoll:");
console.log(RedPoll);

// const routes = [
//     { name: 'default', path: '/', component: Test },
//     { name: 'foo', path: '/foo', component: Poll },
//     { name: 'bar', path: '/bar', component: RedPoll },
// ]

// const router = new VueRouter({
//     // history: VueRouter.createWebHashHistory(),
//     routes // short for `routes: routes`
// });

export default {
    // router,
    components: {
        'menu-bar-left': MenuBarLeft,
        'menu-bar-top': MenuBarTop,
        // 'poll-component': Poll,
        // 'test-component': Test,
        // 'red-poll-component': RedPoll,
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