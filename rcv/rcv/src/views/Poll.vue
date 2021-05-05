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
                                    Updated: {{ pollModel.updated | displayDate }}<br/>
                                    Public Poll: {{ pollModel.publicPoll | titleCase }}<br/>
                                    Public Ballots: {{ pollModel.publicBallots | titleCase }}<br/>
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
                                :disabled="!pollModel.multiBallotsPerUser && pollModel.ballots.length >= 1"
                                icon="mdi-plus"
                            ></nav-button>
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
                                                :ballotContext="ballot.context[pollModel.type]"
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
                                                :ballotContext="ballot.context[pollModel.type]"
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
            pollModel: Common.getEmptyPollContext(),
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