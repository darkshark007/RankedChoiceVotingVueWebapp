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
            <div
                v-if="!loading"
            >
                <v-card
                    class="wrapper"
                    max-width="500px"
                    v-if="!pollModel.id"
                >
                    Poll with that ID was not found.
                </v-card>
                <v-card
                    class="wrapper"
                    max-width="500px"
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
                        <v-col cols=9>
                            <v-card-text align=left>
                                <p>
                                    Type: {{ pollModel.type | displayPollType }}<br/>
                                    Created: {{ pollModel.created | displayDate }}<br/>
                                    Updated: {{ pollModel.updated | displayDate }}
                                </p>
                            </v-card-text>
                        </v-col>
                        <v-col class="mt-4" cols=3 v-if=pollModel.canEdit>
                            <nav-button
                                :route="pollModel.editRoute"
                                title="Edit"
                            ></nav-button>
                        </v-col>
                    </v-row>
                    <v-divider class="mx-4"></v-divider>
                    <v-row>
                        <v-col class="subheader">
                            <h4>Choices</h4>
                        </v-col>
                    </v-row>
                    <!--
                    <v-card
                        v-for="cand, idx in pollModel.choices" 
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
                                <div v-if="cand.name">
                                    <b>{{ cand.name }}</b>
                                </div>
                                <div v-if="cand.description">
                                    <i>{{ cand.description }}</i>
                                </div>
                            </v-col>
                        </v-row>
                    </v-card>
                    -->
                    <poll-choice
                        v-for="cand, idx in pollModel.choices" 
                        :key="'choice-'+idx"
                        :choice="cand"
                    ></poll-choice>
                    <v-divider class="mx-4"></v-divider>
                    <v-row align=center>
                        <v-col class="subheader" cols=6>
                            <h4>My Ballots</h4>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col class="subheader" cols=4>
                            <nav-button
                                :route="pollModel.editBallots"
                                icon="mdi-plus"
                            ></nav-button>
                        </v-col>
                    </v-row>
                    <div v-for="ballot, idx in pollModel.ballots" :key="'ballot-'+idx">
                        <router-link :to="ballot.route" class="route-item">
                            <v-row align=center>
                                <v-col cols=1>
                                    <v-icon class="ma-3">mdi-ballot-outline</v-icon>
                                </v-col>
                                <v-col cols=10>
                                    <v-card-text>{{ ballot.name }}</v-card-text>
                                </v-col>
                            </v-row>
                        </router-link>
                    </div>
                    <v-divider class="mx-4"></v-divider>
                    <v-row align=center>
                        <v-col class="subheader" cols=6>
                        <nav-button
                            :route="'/results/'+id"
                            title="Results"
                        ></nav-button>
                        </v-col>
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
        };
    },
    filters: {
        ...Common.filters,
    },
    methods: {
        setPollModel(id) {
            this.pollModel = Common.getEmptyPollContext()
            if (id) {
                this.loading = true;
                Common.getPollData({'id': id, includeMyBallots: true})
                    .then(data => {
                        this.pollModel = data;
                        for (let ballotKey in data.ballots) {
                            let ballot = data.ballots[ballotKey];
                            ballot.route = `/editBallots/${data.id}/${ballot.id}`;
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
</style>