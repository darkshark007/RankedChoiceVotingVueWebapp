<template>
    <div id="editPoll" align="center">
        <v-container>
            <v-card
                class="wrapper"
                id="loading-card"
                max-width="60%"
                align="center"
                v-if="loading"
                :loading="loading"
            ></v-card>
            <message-card
                :errorString=loadingErrorString
                errorStringBase="Error loading Poll: "
            ></message-card>
            <v-card
                class="wrapper"
                max-width="60%"
                align="center"
                v-if="!loading"
            >
                <v-card-title>
                    {{ pollModel.id ? 'Edit Poll' : 'Create Poll' }}
                    <v-spacer></v-spacer>
                    <nav-button
                        :route="pollModel.pollRoute"
                        title="Back"
                        v-if="pollModel.pollRoute"
                    ></nav-button><!-- TODO: Add confirmation modal if changes? -->
                </v-card-title>
                <v-divider class="mx-4"></v-divider>
                <v-text-field
                    label="Title"
                    v-model="pollModel.name"
                ></v-text-field>
                <v-text-field
                    label="Description"
                    v-model="pollModel.description"
                ></v-text-field>
                <v-select
                    label="Poll Type"
                    :items="pollTypeList"
                    item-text="name"
                    item-value="id"
                    v-model="pollModel.type"
                ></v-select>
                <v-row>
                    <v-col cols=12>
                        <v-divider class="mx-4"></v-divider>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols=6>
                        <h4>Choices</h4>
                    </v-col>
                    <v-col cols=6>
                        <v-btn
                            icon
                            color="indigo"
                            @click="addChoice"
                        >
                            <v-icon>mdi-plus</v-icon>
                        </v-btn>
                    </v-col>
                </v-row>
                <poll-choice 
                    v-for="cand, idx in pollModel.choices"
                    :key="idx"
                    :choice="cand"
                    :edit="true"
                    @remove="removeChoice(cand)"
                ></poll-choice>
                <v-row>
                    <v-col cols=12>
                        <v-divider class="mx-4"></v-divider>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols=12>
                        <v-spacer></v-spacer>
                        <!-- TODO: Refactor button -->
                        <v-btn
                            color="light-green lighten-4"
                            elevation="2"
                            :loading="saving"
                            @click="savePoll"
                        >
                            Save Poll
                        </v-btn>
                    </v-col>
                </v-row>
            </v-card>
            <message-card
                :errorString=saveErrorString
                errorStringBase="Error Saving Poll: "
                :successString=saveSuccessString
            ></message-card>
        </v-container>
    </div>
</template>

<script>
import Common from '../common.js';
import MessageCard from '../components/MessageCard.vue';
import NavButton from '../components/NavButton.vue';
import Choice from '../components/Choice.vue';

export default {
    name: 'edit-poll-component',
    props: {
        id: {
            type: String,
            required: false,
        },
    },
    components: {
        'message-card': MessageCard,
        'nav-button': NavButton,
        'poll-choice': Choice,
    },
    data: () => {
        return {
            ...Common.data,
            pollModel: Common.getEmptyPollContext(),
            loading: false,
            loadingErrorString: null,
            saving: false,
            saveErrorString: null,
            saveSuccessString: null,
        };
    },
    computed: {
    },
    methods: {
        addChoice() {
            this.pollModel.choices.push({});
        },
        removeChoice(cand) {
            let candIdx = this.pollModel.choices.indexOf(cand);
            this.pollModel.choices.splice(candIdx, 1);
        },
        savePoll() {
            this.saving = true;
            this.saveErrorString = null;
            this.saveSuccessString = null;
            Common.savePoll(this.pollModel)
                    .then(data => {
                        this.saveSuccessString = "Save Successful!";
                        this.pollModel = data;
                    })
                    .catch((error) => {
                        this.saveErrorString = error;
                    })
                    .finally(() => {
                        this.saving = false;
                    });
        },
        setPollModel(id) {
            this.pollModel = Common.getEmptyPollContext()
            if (id) {
                this.loading = true;
                this.loadingErrorString = null;
                Common.getPollData(id)
                    .then(data => {
                        this.pollModel = data;
                    })
                    .catch((error) => {
                        this.loadingErrorString = error;
                    })
                    .finally(() => {
                        this.loading = false;
                    });
            }
        },
    },
    mounted() {
        this.setPollModel(this.id);
    },
    watch: {
        "$route.params.id"(newId) {
            this.setPollModel(newId);
        },
    }
};
</script>

<style scoped>
</style>
