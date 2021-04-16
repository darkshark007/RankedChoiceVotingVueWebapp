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
            <error-card
                :errorString=errorString
                errorStringBase="Error loading Poll: "
            ></error-card>
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
                <div v-for="cand, idx in pollModel.choices" :key="idx">
                    <v-row>
                        <v-col cols=1>
                            <v-btn
                                icon
                                color="indigo"
                                @click="removeChoice(cand)"
                            >
                                <v-icon>mdi-close</v-icon>
                            </v-btn>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col cols=10>
                            <v-text-field
                                label="Name"
                                v-model="cand.name"
                            ></v-text-field>
                            <v-text-field
                                label="Description"
                                v-model="cand.description"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                </div>
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
                            Save
                        </v-btn>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols=12>
                        <span v-if="saveResult">
                            {{ saveResult }}
                        </span>
                    </v-col>
                </v-row>
            </v-card>
        </v-container>
    </div>
</template>

<script>
import Utils from '../utils.js';
import ErrorCard from '../components/ErrorCard.vue';
import NavButton from '../components/NavButton.vue';

export default {
    name: 'edit-poll-component',
    props: {
        id: {
            type: String,
            required: false,
        },
    },
    components: {
        'error-card': ErrorCard,
        'nav-button': NavButton,
    },
    data: () => {
        return {
            pollModel: {
                id: null,
                name: '',
                type: '',
                description: '',
                choices: [],
            },
            loading: false,
            errorString: null,
            saving: false,
            saveResult: null,
        };
    },
    computed: {
        pollTypeList() {
            let mapping = window.POLL_TYPES.map((typ) => {
                return {
                    'id': typ[0],
                    'name': typ[1],
                };
            });
            return mapping;
        },
    },
    methods: {
        getEmptyPollModel() {
            return {
                id: null,
                name: '',
                type: '',
                description: '',
                choices: [],
            };
        },
        getEmptyChoiceModel() {
            return {
                name: '',
                description: '',
            };
        },
        addChoice() {
            let new_cand = this.getEmptyChoiceModel();
            this.pollModel.choices.push(new_cand);
        },
        removeChoice(cand) {
            let candIdx = this.pollModel.choices.indexOf(cand);
            this.pollModel.choices.splice(candIdx, 1);
        },
        savePoll() {
            let data = this.pollModel;
            this.saving = true;
            Utils.post(window['API'].create_or_update_poll, data)
                .then(response => response.json())
                .then(data => {
                    console.log('Save Successful:', data);
                    this.saveResult = "Save Successful!";
                    if (!this.pollModel.id) {
                        this.$router.push({ name: 'editPollWithId', params: { id: data.id } });
                    }
                    this.pollModel = data;
                    this.pollModel.pollRoute = `/poll/${this.pollModel.id}`
                })
                .catch((error) => {
                    console.error('Save Error:', error);
                    this.saveResult = "Error!  Not saved!";
                })
                .finally(() => {
                    this.saving = false;
                    setTimeout(() => {
                        this.saveResult = null;
                    }, 10000);
                });
        },
        setPollModel(id) {
            this.pollModel = this.getEmptyPollModel();
            if (id) {
                let data = {
                    'id': id,
                };
                this.loading = true;
                Utils.get(window['API'].get_poll_data, data)
                    .then(response => {
                        if (response.status === 200) {
                            return response.json()
                                .then(data => {
                                    this.pollModel = data;
                                    this.pollModel.pollRoute = `/poll/${this.pollModel.id}`
                                });
                        } else {
                            return response.text()
                                .then(text => {
                                    this.errorString = text;
                                });
                        }
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
    watch: {
        "$route.params.id"(newId) {
            this.setPollModel(newId);
        },
    }
};
</script>

<style scoped>
.wrapper {
    align: center;
    padding: 15px;
}
</style>
