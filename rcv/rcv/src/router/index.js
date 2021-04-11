import Vue from 'vue'
import VueRouter from 'vue-router'

import HelloWorld from '../views/HelloWorld.vue'
import MyPolls from '../views/MyPolls.vue';

import EditPoll from '../views/EditPoll.vue';
import Test from '../views/Test.vue';

Vue.use(VueRouter)

const routes = [
    { name: 'default', path: '/', component: Test },
    { name: 'mypolls', path: '/mypolls', component: MyPolls },
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
