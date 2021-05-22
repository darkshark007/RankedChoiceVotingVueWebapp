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
                @onChange="onChange"
            />
        </v-container>

        <!-- Classic RCV -->
        <v-container v-if="type === 'classic_rcv' || type === 'ranked_cumulative_approval'" class="wrapper">
            <ballot-rcv
                :ballotContext="ballotContext"
                :pollModel="pollModel"
                :choices="choices"
                :isDisplay="isDisplay"
                :isEdit="isEdit"
                :isPreview="isPreview"
                @onChange="onChange"
            />
        </v-container>

        <!-- STAR Vote -->
        <v-container v-if="type === 'star_vote'" class="wrapper">
            <ballot-star
                :ballotContext="ballotContext"
                :choices="choices"
                :isDisplay="isDisplay"
                :isEdit="isEdit"
                :isPreview="isPreview"
                @onChange="onChange"
            />
        </v-container>
    </v-container>
</template>

<script>
import BallotFPTP from './BallotFPTP.vue';
import BallotRCV from './BallotRCV.vue';
import BallotSTAR from './BallotSTAR.vue';

export default {
    name: 'poll-ballot',
    props: {
        ballotContext: {
            type: Object,
            required: true,
        },
        pollModel: {
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
        'ballot-fptp': BallotFPTP,
        'ballot-rcv': BallotRCV,
        'ballot-star': BallotSTAR,
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
    methods: {
        onChange() {
            this.$emit('onChange');
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