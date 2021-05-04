<template>
    <div id="editPoll" align="center">
        <v-container>
            <v-card
                class="wrapper"
                id="loading-card"
                max-width="500px"
                align="center"
                v-if="loading > 0"
                :loading="loading > 0"
            ></v-card>
            <message-card
                :errorString=errorString
                errorStringBase="Error loading Poll: "
            ></message-card>
            <v-card
                class="wrapper"
                max-width="500px"
                align="center"
                v-if="!loading > 0"
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
                    <v-divider class="mx-4"></v-divider>
                    <v-row>
                        <v-col class="subheader" cols=8>
                            <h4>Add new Choices</h4>
                        </v-col>
                        <v-col cols=2>
                            <v-btn
                                fab
                                small
                                color="light-green lighten-4"
                                @click="addChoice"
                            >
                                <v-icon color="indigo">mdi-plus</v-icon>
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
                    <v-divider class="mx-4"></v-divider>
                    <v-row>
                        <v-col class="subheader" cols=8>
                            <h4>Ballot</h4>
                        </v-col>
                        <v-col cols=2 v-if="generated">
                            <v-tooltip bottom max-width="300px">
                                <template v-slot:activator="{ on, attrs }">
                                    <v-icon
                                        color="red"
                                        v-bind="attrs"
                                        v-on="on"
                                        class="ma-2"
                                    >
                                    mdi-hammer-wrench
                                    </v-icon>
                                </template>
                                <span>This <i>{{ this.selectedType | displayPollType }}</i>-style Ballot was pre-filled using data from your other filled-out similar-style ballot(s).</span>
                            </v-tooltip>
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
                    <form-checkbox
                        title="This Ballot is Public"
                        tooltip="If Selected, this Ballot and its choices will be visible to anyone on the Poll page.<br/><br/><b>Note:</b> If switch cannot be toggled, this means that this Poll's creator set <b><i>all</i></b> Ballots to either public or private."
                        :disabled="pollModel.publicBallots !== 'maybe'"
                        v-model="ballotContext.publicBallot"
                    />
                    <ballot
                        :ballotContext="getContextForType()"
                        :choices="pollModel.choices"
                        :type="selectedType"
                        :edit="true"
                        @onChange="onBallotChange"
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
                        errorStringBase="Error Saving Ballot: "
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
import FormCheckbox from '../components/FormCheckbox.vue';


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
        'form-checkbox': FormCheckbox,
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
            loading: 0,
            errorString: null,
            savingChoices: false,
            saveChoicesSuccessString: null,
            saveChoicesErrorString: null,
            savingBallot: false,
            saveBallotSuccessString: null,
            saveBallotErrorString: null,
            generated: false,
        };
    },
    filters: {
        ...Common.filters,
    },
    computed: {
    },
    methods: {
        addChoice() {
            let new_choice = Common.getEmptyChoiceContext();
            this.newChoices.push(new_choice);
        },
        removeChoice(choice) {
            let choiceIdx = this.newChoices.indexOf(choice);
            this.newChoices.splice(choiceIdx, 1);
        },
        getContextForType() {
            this.updateGeneratedBallots();

            if (this.ballotContext && 
                this.ballotContext.context[this.selectedType] && 
                this.ballotContext.context[this.selectedType].generated) {
                this.generated = true;
            } else {
                this.generated = false;
            }

            if (this.selectedType) {
                return this.ballotContext.context[this.selectedType];
            }
            return Common.getEmptyBallotContext();
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
            // Validate
            let errors = false;
            this.saveBallotErrorString = null;
            if (!this.ballotContext.name) {
                errors = true;
                setTimeout(function() {
                    // Hate this.
                    this.saveBallotErrorString = 'Name is required!';
                }.bind(this), 0);
            }
            if (errors) return;

            // Save
            this.updateGeneratedBallots();
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
                        this.syncPollBallotSettings();
                    });
        },
        setPollModel(id) {
            this.pollModel = Common.getEmptyPollContext()
            if (id) {
                this.loading += 1;
                Common.getPollData({'id': id})
                    .then(data => {
                        this.pollModel = data;
                        this.selectedType = this.pollModel.type;
                    })
                    .catch((error) => {
                        this.errorString = error;
                    })
                    .finally(() => {
                        this.loading -= 1;
                        this.syncPollBallotSettings();
                    });
            }
        },
        setBallotModel(pollId, ballotId) {
            this.ballotContext = Common.getEmptyBallotContext()
            if (pollId && ballotId) {
                this.loading += 1;
                Common.getBallotData(pollId, ballotId)
                    .then(data => {
                        this.ballotContext = data;
                    })
                    .catch((error) => {
                        this.errorString = error;
                    })
                    .finally(() => {
                        this.loading -= 1;
                        this.syncPollBallotSettings();
                    });
            }
        },
        syncPollBallotSettings() {
            if (this.loading > 0) {
                return                
            }
            if (this.pollModel.publicBallots === 'yes') {
                this.ballotContext.publicBallot = true;
            } else if (this.pollModel.publicBallots === 'no') {
                this.ballotContext.publicBallot = false;
            }
        },
        updateGeneratedBallots() {
            const fptp = 'fptp';
            const rcv = 'classic_rcv';
            const rca = 'ranked_cumulative_approval';
            // FPTP
            if (!this.ballotContext.context[fptp]) {
                this.ballotContext.context[fptp] = {
                    'generated': true,
                    'selected': null,
                };
            }
            if (this.ballotContext.context[fptp].generated) {
                let tempSelected = null;
                if (!tempSelected && this.ballotContext.context[rcv] && !this.ballotContext.context[rcv].generated) {
                    tempSelected = this.ballotContext.context[rcv].selected[0];
                }
                if (!tempSelected && this.ballotContext.context[rca] && !this.ballotContext.context[rca].generated) {
                    tempSelected = this.ballotContext.context[rca].selected[0];
                }
                if (this.ballotContext.context[fptp].selected !== tempSelected) {
                    this.ballotContext.context[fptp].selected = tempSelected;
                }
            }

            // RCV
            if (!this.ballotContext.context[rcv]) {
                this.ballotContext.context[rcv] = {
                    'generated': true,
                    'selected': [],
                };
            }
            if (this.ballotContext.context[rcv].generated) {
                let tempSelected = [];
                if (tempSelected.length === 0 && this.ballotContext.context[rca] && !this.ballotContext.context[rca].generated) {
                    tempSelected = [...this.ballotContext.context[rca].selected];
                }
                if (tempSelected.length === 0 && this.ballotContext.context[fptp] && !this.ballotContext.context[fptp].generated) {
                    tempSelected = [this.ballotContext.context[fptp].selected];
                }
                if (this.ballotContext.context[rcv].selected.join('_') !== tempSelected.join('_')) {
                    this.ballotContext.context[rcv].selected = tempSelected;
                }
            }

            // RCA
            if (!this.ballotContext.context[rca]) {
                this.ballotContext.context[rca] = {
                    'generated': true,
                    'selected': [],
                };
            }
            if (this.ballotContext.context[rca].generated) {
                let tempSelected = [];
                if (tempSelected.length === 0 && this.ballotContext.context[rcv] && !this.ballotContext.context[rcv].generated) {
                    tempSelected = [...this.ballotContext.context[rcv].selected];
                }
                if (tempSelected.length === 0 && this.ballotContext.context[fptp] && !this.ballotContext.context[fptp].generated) {
                    tempSelected = [this.ballotContext.context[fptp].selected];
                }
                if (this.ballotContext.context[rca].selected.join('_') !== tempSelected.join('_')) {
                    this.ballotContext.context[rca].selected = tempSelected;
                }
            }
        },
        onBallotChange() {
            this.ballotContext.context[this.selectedType].generated = false;
            this.generated = false;
        },
    },
    mounted() {
        this.setPollModel(this.pollid);
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
