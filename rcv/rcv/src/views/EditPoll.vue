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
                :errorString=loadingErrorString
                errorStringBase="Error loading Poll: "
            ></message-card>
            <v-card
                class="wrapper appWidth"
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
                <v-textarea
                    label="Description"
                    v-model="pollModel.description"
                    rows="1"
                    auto-grow
                ></v-textarea>
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
                    <form-text
                        title="Limit Rank Choices"
                        v-model="pollModel.limitRankChoices"
                        tooltip="If set, limits the number of Choices the Ballot Submitter can rank.  Can be useful for managing Polls with a large number of Choice options.<br/><br/><b>Note:</b> Only applies to some Poll Types"
                        :rules="[validateLimitRankChoices]"
                    />
                    <!-- TODO: Add option for ballots-public-to-creator only? -->
                    <form-select
                        label="When should Ballots be Public?"
                        tooltip="When should Ballots be Public?<br/><br/>• <b>Never</b> - Ballots are always hidden, only the Ballot Submitter can see the contents<br/>• <b>Optionally</b> - Ballot Submitter can decide whether their Ballot is public or hidden<br/>• <b>Always</b> - Ballots are always public, anyone can see the contents of each Ballot<br/>"
                        :items="publicBallotOptions"
                        v-model="pollModel.publicBallots"
                    />
                    <form-checkbox
                        title="Allow Multiple Ballots per User"
                        tooltip="If active, Users will be able to submit multiple ballots.  Otherwise, they will be restricted to a single ballot.<br/><br/>Useful for permitting multiple participants to submit Ballots from a single device."
                        v-model="pollModel.multiBallotsPerUser"
                    />
                </template>
                <!-- TODO: Checkbox: Allow users to see old polls<br/> -->
                <!-- TODO: Add confirmation modal for Recycle<br/> -->
                <!-- TODO: Checkbox: Disallow Users to edit Ballots once submitted<br/> -->
                <!-- TODO: Checkbox: Full Ballot - All Choices must be Ranked/Considered<br/> -->
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
                <poll-choice 
                    v-for="choice, idx in pollModel.choices"
                    :key="idx"
                    :choice="choice"
                    :propEdit="true"
                    @remove="removeChoice(choice)"
                ></poll-choice>
                <template v-if="showAdvanced">
                    <form-checkbox
                        title="Randomize Choices"
                        tooltip="If active, Choices will be listed in a random order."
                        v-model="pollModel.randomizeChoices"
                    />
                    <form-select
                        label="When can Ballot Submitters add choices to the poll?"
                        tooltip="When can Ballot Submitters add choices to the poll?<br/><br/>• <b>Never</b> - Ballot Submitters can never add choices, only the creator<br/>• <b>Before Poll Opens</b> - Ballot Submitters can only add choices before voting opens<br/>• <b>Always</b> - Ballot Submitters can always add new choices<br/>"
                        :items="userAddChoicesOptions"
                        v-model="pollModel.usersCanAddChoices"
                    />
                    <form-text
                        title="Limit number of Choices users can add"
                        v-model="pollModel.limitChoicesAdded"
                        tooltip="If set, limits the maximum number of Choices the Ballot Submitter can contribute to the Poll to the given number."
                        :rules="[validateLimitChoicesAdded]"
                    />
                </template>
                <v-divider class="my-4"/>
                <template v-if="showAdvanced">
                    <v-row>
                        <v-col cols=6>
                            <h4>Poll Settings</h4>
                        </v-col>
                    </v-row>
                    <form-select
                        label="When should Results be Publically Available?"
                        tooltip="When should Results be Publically Available?<br/><br/>• <b>Always</b> - Results are <b>always Available</b> to the Ballot Submitter<br/>• <b>After Voting</b> - Results are <b>unavailable</b> to the Ballot Submitter until after they have submitted a Ballot<br/>• <b>After Poll Closes</b> - Results are <b>unavailable</b> until after Poll Closes or is Locked<br/>• <b>Never</b> - Results are never available Publically, only to Poll creator<br/>"
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
                <message-card
                    :errorString=saveErrorString
                    errorStringBase="Error Saving Poll: "
                    :successString=saveSuccessString
                ></message-card>
                <template v-if="showAdvanced">
                    <v-divider class="my-4"/>
                    <p>
                        Recycle the poll to archive the existing Ballots and Results and reset this Poll for a new round of Ballots.
                    </p>
                    <p>
                        This is useful for creating re-usable or recurring Polls with a static URL.
                    </p>
                    <v-row>
                        <v-col cols=12>
                            <!-- TODO: Refactor button -->
                            <v-btn
                                color="light-green lighten-4"
                                elevation="2"
                                :loading="recycling"
                                @click="recyclePoll"
                            >
                                Recycle Poll
                            </v-btn>
                        </v-col>
                    </v-row>
                    <message-card
                        :errorString=recycleErrorString
                        errorStringBase="Error Saving Poll: "
                        :successString=recycleSuccessString
                    ></message-card>
                </template>
            </v-card>
        </v-container>
    </div>
</template>

<script>
import Common from '../common.js';
import MessageCard from '../components/MessageCard.vue';
import NavButton from '../components/NavButton.vue';
import Choice from '../components/Choice.vue';
import FormCheckbox from '../components/FormCheckbox.vue';
import FormText from '../components/FormText.vue';
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
        'form-text': FormText,
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
            recycling: false,
            recycleErrorString: null,
            recycleSuccessString: null,
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
            userAddChoicesOptions: [
                { name: 'Never',             value: 'never',  hint: 'Ballot Submitters can never add choices, only the creator' },
                { name: 'Before Poll Opens', value: 'open',   hint: 'Ballot Submitters can only add choices before voting opens' },
                { name: 'Always',            value: 'always', hint: 'Ballot Submitters can always add new choices' },
            ],
        };
    },
    computed: {
        pollIsOpen: Common.computed.pollIsOpen,
        pollStatusMessage: Common.computed.pollStatusMessage,
    },
    methods: {
        addChoice() {
            this.pollModel.choices.push({});
        },
        removeChoice(choice) {
            let choiceIdx = this.pollModel.choices.indexOf(choice);
            this.pollModel.choices.splice(choiceIdx, 1);
        },
        validateLimitRankChoices: Common.methods.validateLimitRankChoices,
        validateLimitChoicesAdded: Common.methods.validateLimitChoicesAdded,
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
        recyclePoll() {
            this.recycling = true;
            this.recycleErrorString = null;
            this.recycleSuccessString = null;
            Common.recyclePoll(this.pollModel)
                    .then(data => {
                        this.recycleSuccessString = "Recycle Successful!";
                        this.pollModel = {
                            ...Common.getEmptyPollContext(),
                            ...data,
                        };
                    })
                    .catch((error) => {
                        this.recycleErrorString = error;
                    })
                    .finally(() => {
                        this.recycling = false;
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
