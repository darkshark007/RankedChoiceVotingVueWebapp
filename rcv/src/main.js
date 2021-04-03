import loadComponent from '/static/moduleLoader.js';

let MenuBarLeft = loadComponent('/static/components/MenuBarLeft.vue');
let MenuBarTop = loadComponent('/static/components/MenuBarTop.vue');
let RedPoll = loadComponent('/static/components/RedPoll.vue');
let Poll = loadComponent('/static/components/Poll.vue');
let Test = loadComponent('/static/components/Test.vue');
console.log(RedPoll);
const routes = [
    { name: 'default', path: '/', component: Test },
    { name: 'foo', path: '/foo', component: Poll },
    { name: 'bar', path: '/bar', component: RedPoll },
]


const router = new VueRouter({
    // history: VueRouter.createWebHashHistory(),
    routes // short for `routes: routes`
});

const app = new Vue({
    router,
    el: '#app',
    components: {
        'menu-bar-left': MenuBarLeft,
        'menu-bar-top': MenuBarTop,
        'poll-component': Poll,
        'test-component': Test,
        'red-poll-component': RedPoll,
    },
    data: () => {
        return {
            title: 'Welcome to My Journalzzz',
            days: [1,2,3,4],
          };
    },
    mounted: () => {
        console.log(Poll);

        let data = {
            'fish': 'trout',
        };
        // axios.get(`api/create_or_update_poll/`, data);

    },
    template: `
        <div>
            <menu-bar-top/>
            <div>
                <menu-bar-left/>
                <router-view></router-view>
            </div>
        </div>
    `,
});

// app.use(router);
// app.mount('#app');