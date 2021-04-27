<template>
    <div id="editPoll" align="center">
        <v-container>
            <v-card
                class="wrapper"
                id="loading-card"
                max-width="500px"
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
                max-width="500px"
                align="center"
                v-if="!loading"
            >
                <div v-if="!pollModel.id"> Poll with that ID was not found.</div>
                <div v-else>
                    <v-card-title>
                        {{ pollModel.name }}
                        <v-spacer></v-spacer>
                        <nav-button
                            :route="pollModel.pollRoute"
                            title="Back"
                            v-if="pollModel.pollRoute"
                        ></nav-button><!-- TODO: Add confirmation modal if changes? -->
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
                        v-for="choice, idx in newChoices"
                        :key="idx"
                        :choice="choice"
                        :edit="true"
                        @remove="removeChoice(choice)"
                    ></poll-choice>
                    <v-row v-if="newChoices.length > 0">
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
                        :errorString="saveBallotErrorString"
                        errorStringBase="Error Saving New Choices: "
                        :successString="saveBallotSuccessString"
                    ></message-card>
                </div>
            </v-card>
        </v-container>
    </div>
</template>

<script>
import Common from '../common.js';
import MessageCard from '../components/MessageCard.vue';
import NavButton from '../components/NavButton.vue';
import Choice from '../components/Choice.vue';
import Ballot from '../components/Ballot.vue';


export default {
    name: 'edit-ballot-component',
    props: {
        pollid: {
            type: String,
            required: false,
        },
        ballotid: {
            type: String,
            required: false,
        },
    },
    components: {
        'message-card': MessageCard,
        'nav-button': NavButton,
        'poll-choice': Choice,
        'ballot': Ballot,
    },
    data: () => {
        return {
            ...Common.data,
            pollModel: Common.getEmptyPollContext(),
            ballotContext: Common.getEmptyBallotContext(),
            selectedType: '',
            newChoices: [],
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
            let new_choice = Common.emptyChoiceContext();
            this.newChoices.push(new_choice);
        },
        removeChoice(choice) {
            let choiceIdx = this.newChoices.indexOf(choice);
            this.newChoices.splice(choiceIdx, 1);
        },
        getChoicesForType(type) {
            if (!this.ballotContext.context[type]) {
                this.ballotContext.context[type] = {};
            }
            return this.ballotContext.context[type];
        },
        saveChoices() {
            let data = {
                ...this.pollModel,
                choices: [
                    ...this.pollModel.choices,
                    ...this.newChoices,
                ],
            };
            this.savingChoices = true;
            this.saveChoicesErrorString = null;
            this.saveChoicesSuccessString = null;
            Common.savePoll(data)
                    .then(data => {
                        this.saveChoicesSuccessString = "New Choices Saved!";
                        this.pollModel = data;
                        this.newChoices = [];
                    })
                    .catch((error) => {
                        this.saveChoicesErrorString = error;
                    })
                    .finally(() => {
                        this.savingChoices = false;
                    });
        },
        saveBallot() {
            let data = {
                'pollId': this.pollModel.id,
                'ballot': this.ballotContext,
            };
            this.savingBallot = true;
            this.saveBallotErrorString = null;
            this.saveBallotSuccessString = null;
            Common.saveBallot(data)
                    .then((data) => {
                        this.saveBallotSuccessString = "Ballot Saved!";
                        this.ballotContext = data;
                        if (!this.ballotid) {
                            this.$router.push({name: 'editBallotsWithId', params: { pollid: this.pollid, ballotid: data.id } });
                        }
                    })
                    .catch((error) => {
                        this.saveBallotErrorString = error;
                    })
                    .finally(() => {
                        this.savingBallot = false;
                    });
        },
        setPollModel(id) {
            this.pollModel = Common.getEmptyPollContext()
            if (id) {
                this.loading = true;
                Common.getPollData({'id': id})
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
        setBallotModel(pollId, ballotId) {
            this.ballotContext = Common.getEmptyBallotContext()
            if (pollId && ballotId) {
                this.loading = true;
                Common.getBallotData(pollId, ballotId)
                    .then(data => {
                        this.ballotContext = data;
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
        console.log(this.ballotid);
        if (this.ballotid) {
            this.setBallotModel(this.pollid, this.ballotid);
        }
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
