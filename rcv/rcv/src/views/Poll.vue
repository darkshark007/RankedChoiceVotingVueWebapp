<template>
    <div id="editPoll" align="center">
        <v-container>
            <v-card
                class="wrapper appWidth"
                id="loading-card"
                align="center"
                v-if="loading"
                :loading="loading"
            ></v-card>
            <message-card
                :errorString=errorString
                errorStringBase="Error loading Poll: "
            ></message-card>
            <div
                v-if="!loading"
            >
                <v-card
                    class="wrapper appWidth"
                    v-if="!pollModel.id"
                >
                    Poll with that ID was not found.
                </v-card>
                <v-card
                    class="wrapper appWidth"
                    v-else
                >
                    <v-card-title>
                        {{ pollModel.name }}
                    </v-card-title>
                    <v-card-subtitle class="descriptionText" align=left>
                        {{ pollModel.description }}
                    </v-card-subtitle>
                    <v-divider class="mx-4"></v-divider>
                    <v-row class="mb-0 pb-0">
                        <v-col cols=9 class="mb-0 pb-0">
                            <v-card-text align=left class="mb-0 pb-0">
                                <p class="mb-0 pb-0">
                                    <b>Type:</b> {{ pollModel.type | displayPollType }}<br/>
                                    <b>Created:</b> {{ pollModel.created | displayDate }}<br/>
                                    <b>Updated:</b> {{ pollModel.updated | displayDate }}<br/>
                                </p>
                            </v-card-text>
                        </v-col>
                        <v-col class="mt-4 mb-0 pb-0" cols=3 v-if=pollModel.canEdit>
                            <nav-button
                                :route="pollModel.editRoute"
                                title="Edit"
                            ></nav-button>
                        </v-col>
                    </v-row>
                    <v-row class="mt-0 pt-0">
                        <v-col cols=12 class="mt-0 pt-0">
                            <v-card-text align=left class="mt-0 pt-0">
                                <p class="mt-0 pt-0">
                                    <b>Public Poll:</b> {{ pollModel.publicPoll | titleCase }}<br/>
                                    <b>Public Ballots:</b> {{ pollModel.publicBallots | titleCase }}<br/>
                                    <b>Public Results:</b> {{ pollModel.publicResults | titleCase }}<br/>
                                    <b>Multiple Ballots Per User:</b> {{ pollModel.multiBallotsPerUser | titleCase }}<br/>
                                    <b>Randomize Choices:</b> {{ pollModel.randomizeChoices | titleCase }}<br/>
                                </p>
                                <p>
                                    <font :color="pollModel.locked ? 'red' : ''"><b>Poll Locked:</b> {{ pollModel.locked | titleCase }}</font><br/>
                                    <font :color="!pollIsOpen ? 'red' : ''"><b>Poll Status:</b> {{ pollStatusMessage | titleCase }}</font><br/>
                                    <template v-if="pollModel.ballotStart">
                                        <b class="pl-4">Voting Opens:</b> {{ new Date(pollModel.ballotStart*1000).toLocaleString() }}<br/>
                                    </template>
                                    <template v-if="pollModel.ballotEnd">
                                        <b class="pl-4">Voting Closes:</b> {{ new Date(pollModel.ballotEnd*1000).toLocaleString() }}<br/>
                                    </template>
                                </p>
                            </v-card-text>
                        </v-col>
                    </v-row>
                    <v-divider class="mx-4"></v-divider>
                    <v-row>
                        <v-col class="subheader" cols=6>
                            <h4>Choices</h4>
                        </v-col>
                        <v-spacer/>
                        <v-col class="subheader" cols=4>
                            <v-btn
                                fab
                                small
                                color="light-green lighten-4"
                                :disabled="pollModel.locked"
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
                        :propEdit="true"
                        @remove="removeChoice(choice)"
                    ></poll-choice>
                    <v-row v-if="choiceEdited || newChoices.length > 0">
                        <v-col cols=12>
                            <v-spacer></v-spacer>
                            <!-- TODO: Refactor button -->
                            <v-btn
                                color="light-green lighten-4"
                                elevation="2"
                                :loading="savingChoices"
                                @click="saveChoices"
                            >
                                Save Choices
                            </v-btn>
                        </v-col>
                    </v-row>
                    <message-card
                        :errorString=saveChoicesErrorString
                        errorStringBase="Error Saving Choices: "
                        :successString=saveChoicesSuccessString
                    ></message-card>
                    <poll-choice
                        v-for="choice, idx in pollModel.choices" 
                        :key="'choice-'+idx"
                        :choice="choice"
                        :editable="choice.created"
                        @onEdit="choiceEdited = true"
                        @remove="removeChoice(choice)"
                    ></poll-choice>
                    <v-divider class="mx-4"></v-divider>
                    <v-row align=center>
                        <v-col class="subheader" cols=6>
                            <h4>{{ pollModel.ballots.length > 1 ? 'My Ballots' : 'My Ballot'}}</h4>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col class="subheader" cols=4>
                            <nav-button
                                :route="pollModel.editBallots"
                                :disabled="(!pollModel.multiBallotsPerUser && pollModel.ballots.length >= 1) || (pollModel.locked) || (!pollIsOpen)"
                                icon="mdi-plus"
                            ></nav-button>
                        </v-col>
                    </v-row>
                    <v-row v-if="pollModel.ballots.length === 0" class="pt-0 mt-0">
                        <v-col cols=12 class="pt-0 mt-0">
                            <v-card-text align=left class="pt-0 mt-0">
                                <p class="pt-0 mt-0">
                                    You haven't created any Ballots yet!
                                </p>
                                <p class="pt-0 mt-0">
                                    Click the (+) button to get started!
                                </p>
                            </v-card-text>
                        </v-col>
                    </v-row>
                    <div v-for="ballot, idx in pollModel.ballots" :key="'ballot-'+idx">
                        <router-link :to="ballot.route" class="route-item">
                            <v-card
                                class="ma-4"
                                elevation=2
                            >
                                <v-row align=center class="ma-2">

                                    <!-- Icon -->
                                    <v-col cols=1>
                                        <v-icon color="indigo" class="ma-2">mdi-ballot-outline</v-icon>
                                    </v-col>

                                    <v-spacer></v-spacer>
                                    <v-col cols=10 align=left>

                                        <!-- Name -->
                                        <div>
                                            <b>{{ ballot.name }}</b>
                                        </div>

                                        <!-- Description -->
                                        <div>
                                            <ballot
                                                :ballotContext="ballot.context[pollModel.type] || getEmptyPollContext()"
                                                :pollModel="pollModel"
                                                :choices="pollModel.choices"
                                                :type="pollModel.type"
                                                :preview="true"
                                            />
                                        </div>
                                    </v-col>
                                </v-row>
                            </v-card>
                        </router-link>
                    </div>
                    <div v-if="pollModel.ballotsPublic.length > 0">
                        <v-divider class="mx-4"></v-divider>
                        <v-row align=center>
                            <v-col class="subheader" cols=6>
                                <h4>Public Ballots</h4>
                            </v-col>
                        </v-row>
                        <div v-for="ballot, idx in pollModel.ballotsPublic" :key="'ballot-'+idx">
                            <v-card
                                class="ma-4"
                                elevation=2
                            >
                                <v-row align=center class="ma-2">

                                    <!-- Icon -->
                                    <v-col cols=1>
                                        <v-icon color="indigo" class="ma-2">mdi-ballot-outline</v-icon>
                                    </v-col>

                                    <v-spacer></v-spacer>
                                    <v-col cols=10 align=left>

                                        <!-- Name -->
                                        <div>
                                            <b>{{ ballot.name }}</b>
                                        </div>

                                        <!-- Description -->
                                        <div>
                                            <ballot
                                                :ballotContext="ballot.context[pollModel.type] || getEmptyPollContext()"
                                                :pollModel="pollModel"
                                                :choices="pollModel.choices"
                                                :type="pollModel.type"
                                                :preview="true"
                                            />
                                        </div>
                                    </v-col>
                                </v-row>
                            </v-card>
                        </div>
                    </div>
                    <v-divider class="my-4"></v-divider>
                    <v-row align=center>
                        <v-col class="subheader" cols=6>
                            <h4>Total Ballots: {{ pollModel.totalBallots }} </h4>
                        </v-col>
                    </v-row>
                    <v-row justify=center>
                        <v-col class="text-center">
                        <nav-button
                            :route="{ name: 'results', params: {'id': id, 'fromRoute': `/poll/${id}`}}"
                            title="Results"
                            :disabled="!shouldShowResultButton"
                        ></nav-button>
                        </v-col>
                    </v-row>
                    <v-row justify=center>
                        <span class="text-center">{{ pollStatusMessage }}</span>
                    </v-row>
                </v-card>
            </div>
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
    name: 'poll',
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
        'ballot': Ballot,
    },
    data: () => {
        return {
            ...Common.data,
            pollModel: Common.getEmptyPollContext(),
            newChoices: [],
            savingChoices: false,
            choiceEdited: false,
            saveChoicesErrorString: null,
            saveChoicesSuccessString: null,
            loading: false,
            errorString: null,
        };
    },
    filters: {
        ...Common.filters,
    },
    computed: {
        shouldShowResultButton: Common.computed.shouldShowResultButton,
        pollStatusMessage: Common.computed.pollStatusMessage,
        pollIsOpen: Common.computed.pollIsOpen,
    },
    methods: {
        getEmptyPollContext: Common.getEmptyPollContext,
        addChoice() {
            let newChoice = Common.getEmptyChoiceContext();
            this.newChoices.push(newChoice);
        },
        removeChoice(choice) {
            let choiceIdx = this.newChoices.indexOf(choice);
            if (choiceIdx !== -1) this.newChoices.splice(choiceIdx, 1);
            choiceIdx = this.pollModel.choices.indexOf(choice);
            if (choiceIdx !== -1) this.pollModel.choices.splice(choiceIdx, 1);
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
                        this.saveChoicesSuccessString = "Choices Saved!";
                        this.choiceEdited = false;
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
        setPollModel(id) {
            this.pollModel = Common.getEmptyPollContext()
            if (id) {
                this.loading = true;
                Common.getPollData({'id': id, includeMyBallots: true})
                    .then(data => {
                        this.pollModel = data;
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
        this.setPollModel(this.id);
    },
};
</script>

<style scoped>
</style>