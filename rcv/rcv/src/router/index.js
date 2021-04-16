import Vue from 'vue'
import VueRouter from 'vue-router'

import HelloWorld from '../views/HelloWorld.vue'
import About from '../views/About.vue'

import MyPolls from '../views/MyPolls.vue';
import MyBallots from '../views/MyBallots.vue';
import EditPoll from '../views/EditPoll.vue';
import EditBallot from '../views/EditBallot.vue';
import Poll from '../views/Poll.vue';

Vue.use(VueRouter)

const routes = [
    { name: 'default', path: '/', component: About },
    { name: 'mypolls', path: '/mypolls', component: MyPolls },
    { name: 'myballots', path: '/myballots', component: MyBallots },
    { name: 'poll', path: '/poll/:id', component: Poll, props: true  },
    { name: 'editBallotsWithId', path: '/editBallots/:pollid/:ballotid', component: EditBallot, props: true },
    { name: 'editBallots', path: '/editBallots/:pollid', component: EditBallot },
    { name: 'editPollWithId', path: '/editPoll/:id', component: EditPoll, props: true },
    { name: 'editPoll', path: '/editPoll', component: EditPoll },
    { name: 'helloworld', path: '/helloworld', component: HelloWorld },
];


// const routes = [
//   {
//     path: '/',
//     name: 'Home',
//     component: Home
//   },
//   {
//     path: '/about',
//     name: 'About',
//     // route level code-splitting
//     // this generates a separate chunk (about.[hash].js) for this route
//     // which is lazy-loaded when the route is visited.
//     component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
//   }
// ]

const router = new VueRouter({
  // mode: 'history',
  // base: process.env.BASE_URL,
  routes
})

export default router
