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
    computed: {
        // isRedirecting() {
        //     let loc = window.location;
        //     if (loc.ancestorOrigins && loc.ancestorOrigins[0] === 'https://multipolls.app') return true;
        //     return false;
        // }
    },
    mounted() {
        // if (this.isRedirecting) {
        //     console.log(window.location);
        //     console.log(window);
        // }
    },
    // watch: {
    //     $route(to, from) {
    //         if (this.isRedirecting) {
    //             // react to route changes...
    //             let newUrl = `${window.location.ancestorOrigins[0]}/#${to.fullPath}`;
    //             let newUrlFragment = `/#${to.fullPath}`;
    //             let newHash = `#${to.fullPath}`;
    //             console.log(newUrl, newUrlFragment, newHash);
    //             // console.log('New Url: ')
    //             // console.log(newUrl);
    //             // history.pushState({},"MultiPolls",newUrl);
    //             // window.parent.history.pushState({},"MultiPolls",newUrlFragment);
    //             // console.log(newUrlFragment);
    //             // window.parent.location.href = newUrl;
    //             // window.top.location.hash = newHash;
    //             window.open(newUrl, "_top", null, true);

    //         }
    //     },
    // },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.subheader {
    text-align: left;
    padding: 20px;
    padding-left: 50px;
}

.descriptionText {
    font-style: italic;
    white-space: pre-line;
}

.wrapper {
    text-align: center;
    padding: 15px;
}

.wrapWords {
    overflow-wrap: break-word !important;
    word-break: break-word !important;

}
.appWidth {
    max-width: 590px;
}

.route-item {
    text-align: left;
    text-decoration: none;
}

</style>