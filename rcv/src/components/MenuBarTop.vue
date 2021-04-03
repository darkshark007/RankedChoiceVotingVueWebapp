<template>
    <div id="menu-top">
        <!-- -->
        <v-row
            align="center"
            justify="space-around"
        >
            <v-col v-for="item in items" :key="item.route">
                <router-link :to="item.route">
                    <v-btn
                        color="primary"
                    >
                        {{ item.desc }}
                    </v-btn>
                </router-link>
            </v-col>
        </v-row>
        <!--
        <v-card
        class="mx-auto overflow-hidden"
        height="400"
        >
            <v-app-bar
                color="deep-purple"
                dark
            >

            </v-app-bar>
        </v-card>
        <!--
        <v-card
        class="mx-auto overflow-hidden"
        height="400"
        >
        <v-app-bar
            color="deep-purple"
            dark
        >
            <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
    
            <v-toolbar-title>Title</v-toolbar-title>
            <v-toolbar-title v-for="item in items" :key="item.route">
                <router-link :to="item.route">
                    <v-btn
                        color="primary"
                    >
                        {{ item.desc }}
                    </v-btn>
                </router-link>
            </v-toolbar-title>
        </v-app-bar>
    
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
        </v-card>
        -->
    </div>
</template>

<script>
module.exports = {
    name: 'menu-bar-top',
    components: {
    },
    data: () => {
        return {
            drawer: true,
            group: null,
            items: [
                {'route': '/',    'desc': 'Home'},
                {'route': '/foo', 'desc': 'Foo'},
                {'route': '/bar', 'desc': 'Bar'},
            ]
        };
    },
    mounted: () => {
    },
};
</script>

<style scoped>
</style>