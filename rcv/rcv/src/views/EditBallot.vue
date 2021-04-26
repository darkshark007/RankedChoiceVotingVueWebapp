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
                :errorString=errorString
                errorStringBase="Error loading Poll: "
            ></message-card>
            <v-card
                class="wrapper"
                max-width="60%"
                align="center"
                v-if="!loading"
            >
                <div v-if="!pollModel.id"> Poll with that ID was not found.</div>
                <div v-else>
                    <v-card-title>
                        {{ pollModel.name }}
                    </v-card-title>
                    <v-card-subtitle align=left>
                        {{ pollModel.description }}
                    </v-card-subtitle>
                    <v-divider class="mx-4"></v-divider>
                    <v-row>
                        <v-col cols=9>
                            <v-card-text align=left>
                                <p>
                                    Type: {{ pollModel.type | displayPollType }}<br/>
                                    Created: {{ pollModel.created | displayDate }}<br/>
                                    Updated: {{ pollModel.updated | displayDate }}
                                </p>
                            </v-card-text>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols=12>
                            <v-divider class="mx-4"></v-divider>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col class="subheader" cols=8>
                            <h4>Add new Choices</h4>
                        </v-col>
                        <v-col cols=2>
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
                        v-for="cand, idx in newCandidates"
                        :key="idx"
                        :choice="cand"
                        :edit="true"
                        @remove="removeChoice(cand)"
                    ></poll-choice>
                    <v-row v-if="newCandidates.length > 0">
                        <v-col cols=12>
                            <v-spacer></v-spacer>
                            <!-- TODO: Refactor button -->
                            <v-btn
                                color="light-green lighten-4"
                                elevation="2"
                                :loading="savingChoices"
                                @click="saveChoices"
                            >
                                Save New Choices
                            </v-btn>
                        </v-col>
                    </v-row>
                    <message-card
                        :errorString=saveChoicesErrorString
                        errorStringBase="Error Saving New Choices: "
                        :successString=saveChoicesSuccessString
                    ></message-card>
                    <v-row>
                        <v-col cols=12>
                            <v-divider class="mx-4"></v-divider>
                        </v-col>
                    </v-row>
                    <v-divider class="mx-4"></v-divider>
                    <v-row>
                        <v-col class="subheader">
                            <h4>Ballot</h4>
                        </v-col>
                    </v-row>
                    <v-text-field
                        label="Name"
                        v-model="ballotContext.name"
                    ></v-text-field>
                    <v-select
                        label="Ballot Style"
                        :items="pollTypeList"
                        item-text="name"
                        item-value="id"
                        v-model="selectedType"
                    ></v-select>
                    <ballot
                        :ballotContext="getChoicesForType(selectedType)"
                        :choices="pollModel.choices"
                        :type="selectedType"
                        :edit="true"
                    />
                    <v-row>
                        <v-col cols=12>
                            <v-spacer></v-spacer>
                            <!-- TODO: Refactor button -->
                            <v-btn
                                color="light-green lighten-4"
                                elevation="2"
                                :loading="savingBallot"
                                @click="saveBallot"
                            >
                                Save Ballot
                            </v-btn>
                        </v-col>
                    </v-row>
                    <message-card
                        errorString="a"
                        errorStringBase="Error Saving New Choices: "
                        successString="a"
                    ></message-card>
                </div>
            </v-card>
        </v-container>
    </div>
</template>

<script>
import Common from '../common.js';
import MessageCard from '../components/MessageCard.vue';
// import NavButton from '../components/NavButton.vue';
import Choice from '../components/Choice.vue';
import Ballot from '../components/Ballot.vue';


export default {
    name: 'edit-ballot-component',
    props: {
        pollid: {
            type: String,
            required: false,
        },
    },
    components: {
        'message-card': MessageCard,
        // 'nav-button': NavButton,
        'poll-choice': Choice,
        'ballot': Ballot,
    },
    data: () => {
        return {
            ...Common.data,
            pollModel: Common.getEmptyPollContext(),
            ballotContext: Common.emptyBallotContext(),
            selectedType: '',
            newCandidates: [],
            loading: false,
            errorString: null,
            savingChoices: false,
            saveChoicesSuccessString: null,
            saveChoicesErrorString: null,
            savingBallot: false,
            saveBallotSuccessString: null,
            saveBallotErrorString: null,
        };
    },
    filters: {
        ...Common.filters,
    },
    computed: {
    },
    methods: {
        addChoice() {
            let new_cand = Common.emptyBallotContext();
            this.newCandidates.push(new_cand);
        },
        removeChoice(cand) {
            let candIdx = this.newCandidates.indexOf(cand);
            this.newCandidates.splice(candIdx, 1);
        },
        getChoicesForType(type) {
            if (!this.ballotContext.choices[type]) {
                this.ballotContext.choices[type] = {};
            }
            return this.ballotContext.choices[type];
        },
        saveChoices() {
            let data = {
                ...this.pollModel,
                choices: [
                    ...this.pollModel.choices,
                    ...this.newCandidates,
                ],
            };
            console.log(data);
            this.savingChoices = true;
            this.saveChoicesErrorString = null;
            this.saveChoicesSuccessString = null;
            Common.savePoll(data)
                    .then(data => {
                        this.saveChoicesSuccessString = "New Choices Saved!";
                        this.pollModel = data;
                        this.newCandidates = [];
                    })
                    .catch((error) => {
                        this.saveChoicesErrorString = error;
                    })
                    .finally(() => {
                        this.savingChoices = false;
                    });
        },
        saveBallot() {
        },
        setPollModel(id) {
            this.pollModel = Common.getEmptyPollContext()
            if (id) {
                this.loading = true;
                Common.getPollData(id)
                    .then(data => {
                        this.pollModel = data;
                        this.selectedType = this.pollModel.type;
                    })
                    .catch((error) => {
                        this.errorString = error;
                    })
                    .finally(() => {
                        this.loading = false;
                    });
            }
        },
    },
    mounted() {
        this.setPollModel(this.pollid);
    },
    watch: {
        "$route.params.pollid"(newId) {
            this.setPollModel(newId);
        },
    }
};
</script>

<style scoped>
</style>
