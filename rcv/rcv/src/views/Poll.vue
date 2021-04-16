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
            <div
                v-if="!loading"
            >
                <v-card
                    class="wrapper"
                    max-width="60%"
                    v-if="!pollModel.id"
                >
                    Poll with that ID was not found.
                </v-card>
                <v-card
                    class="wrapper"
                    max-width="60%"
                    v-else
                >
                    <v-card-title>
                        {{ pollModel.name }}
                    </v-card-title>
                    <v-card-subtitle align=left>
                        {{ pollModel.description }}
                    </v-card-subtitle>
                    <v-divider class="mx-4"></v-divider>
                    <v-row>
                        <v-col class="subheader" cols=6>
                            <h4>Details</h4>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col class="subheader" cols=4>
                            <nav-button
                                :route="pollModel.editRoute"
                                title="Edit"
                            ></nav-button>
                        </v-col>
                    </v-row>
                    <v-card-text align=left>
                        <p>
                            Type: {{ pollModel.type | displayPollType }}<br/>
                            Created: {{ pollModel.created | displayDate }}<br/>
                            Updated: {{ pollModel.updated | displayDate }}
                        </p>
                    </v-card-text>
                    <v-divider class="mx-4"></v-divider>
                    <v-row>
                        <v-col class="subheader">
                            <h4>Candidates</h4>
                        </v-col>
                    </v-row>
                    <v-card 
                        v-for="cand, idx in pollModel.candidates" 
                        :key="idx"
                        class="ma-4"
                        elevation=2
                    >
                        <v-row align=center class="ma-2">
                            <v-col cols=1>
                                <v-icon color="indigo" class="ma-2">mdi-star-outline</v-icon>
                            </v-col>
                            <v-spacer></v-spacer>
                            <v-col cols=10 align=left>
                                    Name: {{ cand.name }}<br/>
                                    Description: {{ cand.description }}
                            </v-col>
                        </v-row>
                    </v-card>
                    <v-divider class="mx-4"></v-divider>
                    <v-row>
                        <v-col class="subheader" cols=6>
                            <h4>Ballots</h4>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col class="subheader" cols=4>
                            <nav-button
                                :route="pollModel.editBallots"
                                title="Edit"
                            ></nav-button>
                        </v-col>
                    </v-row>

                </v-card>
            </div>
        </v-container>
    </div>
</template>

<script>
import Utils from '../utils.js';
import ErrorCard from '../components/ErrorCard.vue';
import NavButton from '../components/NavButton.vue';

export default {
    name: 'poll',
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
                candidates: [],
            },
            loading: false,
            errorString: null,
        };
    },
    filters: {
        displayDate(date) {
            let dt = new Date(date);
            let hour = ""+dt.getHours();
            if (hour.length === 1) {
                hour = "0"+hour;
            }
            let min = ""+dt.getMinutes();
            if (min.length === 1) {
                min = "0"+min;
            }
            return `${dt.getMonth()}/${dt.getDate()}/${dt.getYear()} ${hour}:${min}`;
        },
        displayPollType(type) {
            let item = window['POLL_TYPES'].find((t) => {
                return t[0] === type;
            });
            if (item)
                return item[1];
            return null;
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
                                    this.pollModel.editRoute = `/editPoll/${this.pollModel.id}`;
                                    this.pollModel.editBallots = `/editBallots/${this.pollModel.id}`;
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
};
</script>

<style scoped>
.subheader {
    text-align: left;
    padding: 20px;
    padding-left: 50px;
}

.nav-button {
    margin-left: 5px;
    margin-right: 5px;
    text-decoration: none;
}

</style>