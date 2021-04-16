<template>
    <div id="menu-top">
        <v-card
        class="mx-auto overflow-hidden"
        >
            <v-app-bar
                color="green darken-4"
            >
                <!--<v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>-->
                <v-toolbar-title v-for="item in items.left" :key="item.route">
                    <nav-button
                        :route="item.route"
                        :title="item.desc"
                    ></nav-button>
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-toolbar-title v-for="item in items.right" :key="item.route">
                    <nav-button
                        :route="item.route"
                        :title="item.desc"
                    ></nav-button>
                </v-toolbar-title>
            </v-app-bar>
            <!--
            <v-navigation-drawer
                v-model="drawer"
                absolute
                temporary
            >
                <v-list
                nav
                dense
                >
                <v-list-item-group
                    v-model="group"
                    active-class="deep-purple--text text--accent-4"
                >
                    <v-list-item>
                    <v-list-item-icon>
                        <v-icon>mdi-home</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>Home</v-list-item-title>
                    </v-list-item>
        
                    <v-list-item>
                    <v-list-item-icon>
                        <v-icon>mdi-account</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>Account</v-list-item-title>
                    </v-list-item>
                </v-list-item-group>
                </v-list>
            </v-navigation-drawer>
            -->
        </v-card>
    </div>
</template>

<script>
import NavButton from '../components/NavButton.vue';

export default {
    name: 'menu-bar-top',
    components: {
        'nav-button': NavButton,
    },
    data: () => {
        return {
            drawer: false,
            group: null,
            items: { 
                left: [
                    {'route': '/',    'desc': 'Home'},
                    {'route': '/mypolls', 'desc': 'My Polls'},
                    {'route': '/helloworld', 'desc': 'HelloW'},
                ],
                right: [
                    {'route': '/editPoll', 'desc': 'Create Poll'},
                ],
            },
        };
    },
    mounted: () => {
    },
};
</script>

<style scoped>
.nav-button {
    margin-left: 5px;
    margin-right: 5px;
    text-decoration: none;
}
</style>