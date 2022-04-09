<template>
    <router-link :to="route" class="nav-button" :event="disabled ? ['none'] : ['click']">
        <v-btn
            v-if="isTile"
            :disabled=disabled
            tile
            small
            color="light-green lighten-4"
        >
            <v-icon left color="indigo">{{icon}}</v-icon>
            {{title}}
        </v-btn>
        <v-btn
            v-if="isIcon"
            :disabled=disabled
            fab
            small
            color="light-green lighten-4"
        >
            <v-icon color="indigo">{{icon}}</v-icon>
        </v-btn>
        <v-btn
            v-if="isButton"
            :disabled=disabled
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
            type: [Object, String],
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
        disabled: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    computed: {
        isTile() {
            return this.icon && this.title;
        },
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
    text-decoration: none;
}
</style>