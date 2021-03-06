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
                <form-checkbox
                    title="This Poll is Public"
                    tooltip="If active, this Poll will be searchable and visible to anyone on the Polls page.<br/><br/><b>Note:</b> All polls are automatically visible to anyone with the link."
                    v-model="pollModel.publicPoll"
                />
                <v-select
                    label="Public Ballots"
                    :items="publicBallotOptions"
                    item-text="name"
                    item-value="value"
                    :hint="publicBallotHint"
                    v-model="pollModel.publicBallots"
                    persistent-hint
                ></v-select>
                <form-checkbox
                    title="Allow Multiple Ballots per User"
                    tooltip="If active, Users will be able to submit multiple ballots.  Otherwise, they will be restricted to a single ballot.<br/><br/>Useful for allowing multiple participants to submit Ballots from a single device."
                    v-model="pollModel.multiBallotsPerUser"
                />
                TODO: Checkbox: Allow Users to edit Ballots once submitted
                TODO: Checkbox: All Choices must be Ranked/Considered
                TODO: Checkbox: Show Results Publicly<br/>
                TODO: Checkbox: Show Results While Poll Open<br/>
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
                <v-row>
                    <v-col cols=12>
                        <v-divider class="mx-4"></v-divider>
                    </v-col>
                </v-row>
                <form-checkbox
                    title="Lock Poll"
                    tooltip="If active, Users will not be able to submit or edit ballots."
                    switchColor="red"
                    v-model="pollModel.locked"
                />
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
import FormCheckbox from '../components/FormCheckbox.vue';

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
            publicBallotOptions: [
                { name: 'Never',      value: 'no',    hint: 'No - Ballots are always hidden' },
                { name: 'Optionally', value: 'maybe', hint: 'Maybe - Creator can decide whether their Ballot is hidden' },
                { name: 'Always',     value: 'yes',   hint: 'Yes - Ballots are always public, anyone can see the choices' },
            ],
        };
    },
    computed: {
        publicBallotHint() {
            for (let key in this.publicBallotOptions) {
                if (this.publicBallotOptions[key].value === this.pollModel.publicBallots) {
                    return this.publicBallotOptions[key].hint
                }
            }
            return "";
        }
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
