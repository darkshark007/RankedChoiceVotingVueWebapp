<template>
    <div id="editPoll" align="center">
        <v-container>
            <v-card
                class="wrapper"
                max-width="60%"
                align="center"
            >
                <v-card-title>
                    {{ pollModel.id ? 'Edit Poll' : 'Create Poll' }}
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
                        <h4>Candidates</h4>
                    </v-col>
                    <v-col cols=6>
                        <v-btn
                            icon
                            color="indigo"
                            @click="addCandidate"
                        >
                            <v-icon>mdi-plus</v-icon>
                        </v-btn>
                    </v-col>
                </v-row>
                <div v-for="cand, idx in pollModel.candidates" :key="idx">
                    <v-row>
                        <v-col cols=1>
                            <v-btn
                                icon
                                color="indigo"
                                @click="removeCandidate(cand)"
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

export default {
    name: 'edit-poll-component',
    data: () => {
        return {
            pollModel: {
                id: null,
                name: '',
                type: '',
                description: '',
                candidates: [],
            },
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
                candidates: [],
            };
        },
        getEmptyCandidateModel() {
            return {
                name: '',
                description: '',
            };
        },
        addCandidate() {
            let new_cand = this.getEmptyCandidateModel();
            this.pollModel.candidates.push(new_cand);
        },
        removeCandidate(cand) {
            let candIdx = this.pollModel.candidates.indexOf(cand);
            this.pollModel.candidates.splice(candIdx, 1);
        },
        savePoll() {
            let data = this.pollModel;
            this.saving = true;
            Utils.post(`api/create_or_update_poll/`, data)
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    this.saveResult = "Save Successful!";
                })
                .catch((error) => {
                    console.error('Error:', error);
                    this.saveResult = "Error!  Not saved!";
                })
                .finally(() => {
                    this.saving = false;
                    setTimeout(() => {
                        this.saveResult = null;
                    }, 10000);
                });
        },
    },
    mounted: () => {
    },
};
</script>

<style scoped>
.wrapper {
    align: center;
    padding: 15px;
}
</style>
