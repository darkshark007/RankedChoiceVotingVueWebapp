<template>
    <v-container class="wrapper">
        <!-- Single-Choice Popular Vote (FPTP) -->
        <v-container v-if="isEdit" align=center class="wrapper">
            <v-radio-group v-model="ballotContext.selected">
                <v-radio
                    v-for="choice, idx in choices"
                    :key="idx"
                    :value="choice.id"
                    class="choiceRadioLabel"
                    @change="onChange"
                >
                    <template 
                        v-slot:label
                        class="choiceRadioLabel"
                    >
                        <poll-choice
                            :choice="choice"
                            :preview="true"
                            class="choiceRadioLabel"
                        ></poll-choice>
                    </template>
                </v-radio>
            </v-radio-group>
        </v-container>
        <v-container v-if="isPreview" align=center class="wrapper">
            <v-chip-group
                multiple
                active-class="primary--text"
            >
                <v-chip>
                    {{ getChoiceNameFromId(ballotContext.selected) }}
                </v-chip>
            </v-chip-group>
        </v-container>
        <v-container v-if="isDisplay" align=center class="wrapper">
            TODO:
        </v-container>
    </v-container>
</template>

<script>
import Choice from '../components/Choice.vue';

export default {
    name: 'fptp-poll-ballot',
    props: {
        ballotContext: {
            type: Object,
            required: true,
        },
        choices: {
            type: Array,
            required: true,
        },
        isDisplay: {
            type: Boolean,
            required: false,
            default: false,
        },
        isEdit: {
            type: Boolean,
            required: false,
            default: false,
        },
        isPreview: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    components: {
        'poll-choice': Choice,
    },
    methods: {
        getChoiceNameFromId(id) {
            for (let choiceIdx = 0; choiceIdx < this.choices.length; choiceIdx++) {
                if (this.choices[choiceIdx].id === id) {
                    return this.choices[choiceIdx].name;
                }
            }
            return null;
        },
        onChange() {
            this.$emit('onChange');
        },
    },
};
</script>

<style scoped>
.wrapper {
    padding: 0px;
}


::v-deep label {
    display: block !important; /* Hate it. */
}
</style>