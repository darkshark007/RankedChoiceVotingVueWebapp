<template>
    <router-link :to="route" class="nav-button">
        <v-btn
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
            required: true,
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