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
                :errorString=loadingErrorString
                errorStringBase="Error loading Poll: "
            ></message-card>
            <v-card
                class="wrapper"
                max-width="500px"
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
                Open: {{ pollStatusMessage }}
                <v-divider class="my-4"/>
                <v-text-field
                    label="Title"
                    v-model="pollModel.name"
                ></v-text-field>
                <form-checkbox
                    title="Show Advanced Settings"
                    tooltip="Show and modify Advanced Poll controls"
                    v-model="showAdvanced"
                />
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
                <template v-if="showAdvanced">
                    <v-divider class="my-4"/>
                    <v-row>
                        <v-col cols=6>
                            <h4>Ballot Settings</h4>
                        </v-col>
                    </v-row>
                    <form-select
                        label="Limit Rank Choices"
                        :items="getRankLimitChoices"
                        v-model="pollModel.limitRankChoices"
                        tooltip="If set, limits the number of Choices the Ballot Submitter can rank.  Can be useful for managing Polls with a large number of Choice options.<br/><br/><b>Note:</b> Only applies to some Poll Types"
                    ></form-select>
                    <form-select
                        label="When should Ballots be Public?"
                        tooltip="When should Ballots be Public?"
                        :items="publicBallotOptions"
                        v-model="pollModel.publicBallots"
                    />
                    <form-checkbox
                        title="Allow Multiple Ballots per User"
                        tooltip="If active, Users will be able to submit multiple ballots.  Otherwise, they will be restricted to a single ballot.<br/><br/>Useful for permitting multiple participants to submit Ballots from a single device."
                        v-model="pollModel.multiBallotsPerUser"
                    />
                </template>
                <p
                    v-if="showAdvanced"
                >
                    TODO: Checkbox: Disallow Users to edit Ballots once submitted<br/>
                    TODO: Checkbox: Full Ballot - All Choices must be Ranked/Considered<br/>
                    TODO: Checkbox: Disallow users to add new Choices<br/>
                </p>
                <v-divider class="my-4"/>
                <v-row>
                    <v-col cols=6>
                        <h4>Choice Settings</h4>
                    </v-col>
                    <v-col cols=6>
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
                <form-checkbox
                    v-if="showAdvanced"
                    title="Randomize Choices"
                    tooltip="If active, Choices will be listed in a random order."
                    v-model="pollModel.randomizeChoices"
                />
                <poll-choice 
                    v-for="cand, idx in pollModel.choices"
                    :key="idx"
                    :choice="cand"
                    :edit="true"
                    @remove="removeChoice(cand)"
                ></poll-choice>
                <v-divider class="my-4"/>
                <template v-if="showAdvanced">
                    <v-row>
                        <v-col cols=6>
                            <h4>Poll Settings</h4>
                        </v-col>
                    </v-row>
                    <form-select
                        label="When should Results be Publically Available?"
                        tooltip="When should Results be Publically Available?"
                        :items="publicResultsOptions"
                        v-model="pollModel.publicResults"
                    />
                    <form-checkbox
                        :title="pollModel.publicPoll ? 'This Poll is Public' : 'This Poll is Private'"
                        tooltip="If active, this Poll will be searchable and visible to anyone on the Polls page.<br/><br/><b>Note:</b> All polls are automatically visible to anyone with the link."
                        v-model="pollModel.publicPoll"
                    />
                    <form-datetime
                        label="Ballot Start"
                        tooltip="If set, this is the date/time <b>AFTER</b> which Ballots will be able to be created/edited."
                        v-model="pollModel.ballotStart"
                        clearable
                    />
                    <form-datetime
                        label="Ballot End"
                        tooltip="If set, this is the date/time <b>AFTER</b> which Ballots will <b>NO LONGER</b> be able to be created/edited."
                        v-model="pollModel.ballotEnd"
                        clearable
                    />
                </template>
                <form-checkbox
                    :title="pollModel.locked ? 'Poll Voting is Locked' : 'Poll Voting is Open'"
                    tooltip="If active, Users will not be able to submit or edit ballots."
                    switchColor="red"
                    v-model="pollModel.locked"
                />
                <v-row>
                    <v-col cols=12>
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
import FormCheckbox from '../components/FormCheckbox.vue';
import FormSelect from '../components/FormSelect.vue';
import FormDatetime from '../components/FormDatetime.vue';

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
        'form-checkbox': FormCheckbox,
        'form-select': FormSelect,
        'form-datetime': FormDatetime,
    },
    data: () => {
        return {
            ...Common.data,
            pollModel: Common.getEmptyPollContext(),
            loading: false,
            showAdvanced: false,
            loadingErrorString: null,
            saving: false,
            saveErrorString: null,
            saveSuccessString: null,
            publicBallotOptions: [
                { name: 'Never',      value: 'no',    hint: 'Ballots are always hidden, only the Ballot Submitter can see the contents' },
                { name: 'Optionally', value: 'maybe', hint: 'Ballot Submitter can decide whether their Ballot is public or hidden' },
                { name: 'Always',     value: 'yes',   hint: 'Ballots are always public, anyone can see the contents of each Ballot' },
            ],
            publicResultsOptions: [
                { name: 'Always',            value: 'always', hint: 'Results are <b>always Available</b> to the Ballot Submitter' },
                { name: 'After Voting',      value: 'voting', hint: 'Results are <b>unavailable</b> to the Ballot Submitter until after they have submitted a Ballot' },
                { name: 'After Poll Closes', value: 'closed', hint: 'Results are <b>unavailable</b> until after Poll Closes or is Locked' },
                { name: 'Never',             value: 'never',  hint: 'Results are never available Publically, only to Poll creator' },
            ],
        };
    },
    computed: {
        pollIsOpen: Common.computed.pollIsOpen,
        pollStatusMessage: Common.computed.pollStatusMessage,
        getRankLimitChoices() {
            let numChoices = Math.max(2, this.pollModel.choices.length-1);
            let arr = [...Array(numChoices).keys()];
            let noLimit = { name: 'No Limit', value: -1 };
            let mapped = arr.map(i => { return { name: `Top-${(i+2)}`, value: +i+2 }; });
            return [noLimit, ...mapped];
        },
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
                        this.pollModel = {
                            ...Common.getEmptyPollContext(),
                            ...data,
                        };
                        if (!this.id) {
                            this.$router.push({name: 'editPollWithId', params: { id: data.id } });
                        }
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
                Common.getPollData({'id': id})
                    .then(data => {
                        this.pollModel = {
                            ...Common.getEmptyPollContext(),
                            ...data,
                        };
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
