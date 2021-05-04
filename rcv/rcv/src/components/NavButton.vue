<template>
    <router-link :to="route" class="nav-button">
        <v-btn
            v-if="isIcon"
            fab
            small
            color="light-green lighten-4"
            class="ma-3"
        >
            <v-icon color="indigo">{{icon}}</v-icon>
        </v-btn>
        <v-btn
            v-if="isButton"
            color="light-green lighten-4"
            elevation="2"
        >
            {{ title }}
        </v-btn>
    </router-link>

</template>

<script>

export default {
    name: 'nav-button',
    props: {
        route: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            required: false,
            default: "",
        },
        icon: {
            type: String,
            required: false,
            default: "",
        },
    },
    computed: {
        isIcon() {
            return this.icon && !this.title;
        },
        isButton() {
            return !this.icon && this.title;
        },
    },
    data: () => {
        return {}
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