<template>
    <div id="myPolls" align="center">
        <v-container>
            <v-card
                class="wrapper"
                id="loading-card"
                max-width="500px"
                v-if="loading"
                :loading="loading"
            ></v-card>
            <message-card
                :errorString=errorString
                errorStringBase="Error loading Results: "
            ></message-card>
            <v-card
                max-width="500px"
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
                                    Ballots: {{ pollModel.results.count }}
                                </p>
                            </v-card-text>
                        </v-col>
                        <v-col class="mt-4" cols=3>
                            <nav-button
                                :route="pollModel.pollRoute"
                                title="Back"
                                v-if="pollModel.pollRoute"
                            ></nav-button><!-- TODO: Add confirmation modal if changes? -->
                        </v-col>
                    </v-row>
                    <v-divider class="mx-4"></v-divider>
                    <v-row class="ma-2">
                        <v-col cols=8>
                            <v-select
                                label="Result Style"
                                :items="pollTypeList"
                                item-text="name"
                                item-value="id"
                                v-model="type"
                            ></v-select>
                        </v-col>
                    </v-row>
                    <v-container class="wrapper">
                        <!-- Single-Choice Popular Vote -->
                        <v-container v-if="type === 'fptp'" class="wrapper">
                            <result-fptp
                                :pollModel="pollModel"
                                :resultContext="pollModel.results"
                            />
                        </v-container>
                        <!-- Classic Ranked Choice Voting -->
                        <v-container v-if="type === 'classic_rcv'" class="wrapper">
                            <result-rcv
                                :pollModel="pollModel"
                                :resultContext="pollModel.results"
                            />
                        </v-container>
                        <!-- Ranked Cumulative Approval Voting -->
                        <v-container v-if="type === 'ranked_cumulative_approval'" class="wrapper">
                            <result-rca
                                :pollModel="pollModel"
                                :resultContext="pollModel.results"
                            />
                        </v-container>
                    </v-container>
                </v-card>
            </v-card>
        </v-container>
    </div>
</template>

<script>
import MessageCard from '../components/MessageCard.vue';
import Common from '../common.js';
import ResultFPTP from '../components/ResultFPTP.vue';
import ResultRCV from '../components/ResultRCV.vue';
import ResultRankedCumulativeApproval from '../components/ResultRankedCumulativeApproval.vue';
import NavButton from '../components/NavButton.vue';

export default {
    name: 'my-polls',
    props: {
        id: {
            type: String,
            required: false,
        },
    },
    components: {
        'message-card': MessageCard,
        'nav-button': NavButton,
        'result-fptp': ResultFPTP,
        'result-rcv': ResultRCV,
        'result-rca': ResultRankedCumulativeApproval,
    },
    data: () => {
        return {
            ...Common.data,
            errorString: null,
            loading: false,
            type: null,
            pollModel: Common.getEmptyPollContext(),
        };
    },
    methods: {
        setPollModel(id) {
            this.pollModel = Common.getEmptyPollContext()
            if (id) {
                this.loading = true;
                Common.getPollData({'id': id, includeResults: true})
                    .then(data => {
                        this.pollModel = data;
                        this.type = this.pollModel.type;
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
    filters: {
        ...Common.filters,
    },
    mounted() {
        this.setPollModel(this.id);
    },
};
</script>

<style scoped>
</style>