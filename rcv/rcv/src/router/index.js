import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '../views/Home.vue'

import HelloWorld from '../components/HelloWorld.vue'
import RedPoll from '../components/RedPoll.vue';
import Poll from '../components/Poll.vue';
// import Test from './components/Test.vue';

Vue.use(VueRouter)


console.log(">>> RedPoll:");
console.log(RedPoll);

const routes = [
    { name: 'default', path: '/', component: HelloWorld },
    { name: 'foo', path: '/foo', component: Poll },
    { name: 'bar', path: '/bar', component: RedPoll },
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
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
