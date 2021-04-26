<template>
    <v-container class="wrapper">

        <!-- Single-Choice Popular Vote -->
        <v-container v-if="type === 'fptp'" class="wrapper">
            <ballot-fptp
                :ballotContext="ballotContext"
                :choices="choices"
                :isDisplay="isDisplay"
                :isEdit="isEdit"
                :isPreview="isPreview"
            />
        </v-container>
    </v-container>
</template>

<script>
import BallotFPTPVue from './BallotFPTP.vue';

export default {
    name: 'poll-ballot',
    props: {
        ballotContext: {
            type: Object,
            required: true,
        },
        choices: {
            type: Array,
            required: true,
        },
        type: {
            type: String,
            required: true,
        },
        edit: {
            type: Boolean,
            required: false,
            default: false,
        },
        preview: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    components: {
        'ballot-fptp': BallotFPTPVue,
    },
    computed: {
        // Render Type
        isDisplay() {
            return !this.edit && !this.preview;
        },
        isEdit() {
            return this.edit && !this.preview;
        },
        isPreview() {
            return !this.edit && this.preview;
        },
    },
    mounted() {
    },
    data: () => {
        return {}
    },
};
</script>

<style scoped>
.wrapper {
    padding: 0px;
}
</style>