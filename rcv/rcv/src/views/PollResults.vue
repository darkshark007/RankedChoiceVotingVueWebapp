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
                                :route="backRoute"
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
                        <!-- STAR Voting -->
                        <v-container v-if="type === 'star_vote'" class="wrapper">
                            <result-star
                                :pollModel="pollModel"
                                :resultContext="pollModel.results"
                            />
                        </v-container>
                    </v-container>
                    <template v-if="statsList.length > 0">
                        <div><v-divider class="ma-4"></v-divider></div>
                        <v-row>
                        </v-row>

                        <v-row>
                            <v-col class="subheader">
                                <h4>Statistics</h4>
                            </v-col>
                            <v-spacer/>
                            <v-col>
                                <v-btn
                                    fab
                                    small
                                    color="light-green lighten-4"
                                    @click="nextStats"
                                >
                                    <v-icon color="indigo">mdi-refresh</v-icon>
                                </v-btn>
                            </v-col>
                        </v-row>
                        <v-row justify=center>
                            <v-col cols=9 align=center>
                                <v-card
                                    v-for="stat, idx in displayStats"
                                    :key="idx"
                                    v-html="stat.message"
                                    elevation=2
                                    class="pa-4 ma-2"
                                    :class="{ 'stat-seen': stat.seen }"
                                >
                                    {{ stat.message }}
                                </v-card>
                            </v-col>
                        </v-row>
                    </template>
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
import ResultSTAR from '../components/ResultSTAR.vue';
import NavButton from '../components/NavButton.vue';

export default {
    name: 'my-polls',
    props: {
        id: {
            type: String,
            required: false,
        },
        fromRoute: {
            type: String,
            required: false,
        }
    },
    components: {
        'message-card': MessageCard,
        'nav-button': NavButton,
        'result-fptp': ResultFPTP,
        'result-rcv': ResultRCV,
        'result-rca': ResultRankedCumulativeApproval,
        'result-star': ResultSTAR,
    },
    data: () => {
        return {
            ...Common.data,
            errorString: null,
            loading: false,
            type: null,
            statsList: [],
            displayStats: [],
            pollModel: Common.getEmptyPollContext(),
        };
    },
    computed: {
        choiceIdToNameMap: Common.computed.choiceIdToNameMap,
        backRoute() {
            if (this.fromRoute) return this.fromRoute;
            return this.pollModel.pollRoute;
        }
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
                        this.processStats();
                    })
                    .catch((error) => {
                        this.errorString = error;
                    })
                    .finally(() => {
                        this.loading = false;
                    });
            }
        },
        processStats() {
            this.statsList = [];
            if (!this.pollModel || !this.pollModel.results || !this.type) return;
            let total = this.pollModel.results.count;
            let getNewStat = function(getMessage, count, extra) {
                let percent = Math.floor(10000.0*(count/total))/100;
                // let baseInterest = Math.abs(count-(total/2)); // Balance high counts and low counts?
                let baseInterest = count;
                let stat = {
                    count,
                    percent,
                    baseInterest,
                    interest: baseInterest,
                    ...extra,
                };
                stat.message = getMessage(stat);
                return stat;
            }.bind(this);

            let stats = this.pollModel.results[this.type]['stats'];
            if (stats) {
                if (stats.included) {
                    let includedFactory = function(stat) {
                        stat.interest *= 0.25;
                        if (stat.count === 0) {
                            stat.interest *= 0.5;
                            return `<b>No</b> ballots included <b>${stat.choice}</b> as a pick!`;
                        } else if (stat.percent > 25.0) {
                            return `<b>${stat.percent}%</b> of ballots included <b>${stat.choice}</b> as a pick!`;
                        } else {
                            return `Only <b>${stat.percent}</b>% of ballots included <b>${stat.choice}</b> as a pick!`;
                        }
                    }.bind(this);
                    for (let statKey in stats.included) {
                        if (statKey === 'total') continue;
                        let count = stats.included[statKey];
                        let choice = this.choiceIdToNameMap[statKey];
                        let newStat = getNewStat(includedFactory, count, {'type': 'included', choice, });
                        this.statsList.push(newStat);
                    }
                }

                if (stats.picks) {
                    let picksFactory = function(stat) {
                        stat.interest *= 0.5;
                        if (stat.count === 0) {
                            stat.interest *= 0.25;
                            return `<b>No</b> ballots picked <b>${stat.choice}</b> as their #${stat.rank} pick!`;
                        } else if (stat.percent > 25.0) {
                            return `<b>${stat.percent}%</b> of ballots picked <b>${stat.choice}</b> as their #${stat.rank} pick!`;
                        } else {
                            return `Only <b>${stat.percent}</b>% of ballots picked <b>${stat.choice}</b> as their #${stat.rank} pick!`;
                        }
                    }.bind(this);
                    for (let statKey in stats.picks) {
                        if (statKey === 'total') continue;
                        let spl = statKey.split('-');
                        let rank = (1*spl[0])+1;
                        let count = stats.picks[statKey];
                        let choice = this.choiceIdToNameMap[spl[1]];
                        if (count/total < 0.34 && rank >= 4) continue;
                        let newStat = getNewStat(picksFactory, count, {'type': 'pick', rank, choice, });
                        this.statsList.push(newStat);
                    }
                }

                if (stats.score_picks) {
                    let scorePicksFactory = function(stat) {
                        stat.interest *= 0.5;
                        if (stat.count === 0) {
                            stat.interest *= 0.25;
                            return `<b>No</b> ballots scored <b>${stat.choice}</b> as a <b>${stat.score}</b>!`;
                        } else if (stat.percent > 15.0) {
                            return `<b>${stat.percent}%</b> of ballots scored <b>${stat.choice}</b> as a <b>${stat.score}</b>!`;
                        } else {
                            return `Only <b>${stat.percent}</b>% of ballots scored <b>${stat.choice}</b> as a <b>${stat.score}</b>!`;
                        }
                    }.bind(this);
                    for (let statKey in stats.score_picks) {
                        if (statKey === 'total') continue;
                        let spl = statKey.split('-');
                        let score = (1*spl[0]);
                        let count = stats.score_picks[statKey];
                        let choice = this.choiceIdToNameMap[spl[1]];
                        if (count/total < 0.34) continue;
                        let newStat = getNewStat(scorePicksFactory, count, {'type': 'pick', score, choice, });
                        this.statsList.push(newStat);
                    }
                }

                if (stats.top_n_picks) {
                    let topNPicksFactory = function(stat) {
                        if (stat.count === 0) {
                            return `<b>No</b> ballots ranked <b>${stat.choice}</b> among their Top-${stat.rank} picks!`;
                        } else if (stat.percent > 25.0) {
                            return `<b>${stat.percent}%</b> of ballots ranked <b>${stat.choice}</b> among their Top-${stat.rank} picks!`;
                        } else {
                            return `Only <b>${stat.percent}</b>% of ballots ranked <b>${stat.choice}</b> among their Top-${stat.rank} picks!`;
                        }
                    }.bind(this);
                    for (let statKey in stats.top_n_picks) {
                        if (statKey === 'total') continue;
                        let spl = statKey.split('-');
                        let rank = (1*spl[0])+1;
                        let count = stats.top_n_picks[statKey];
                        let choice = this.choiceIdToNameMap[spl[1]];
                        if (rank >= (this.pollModel.choices.length)/2+1) continue;
                        if (count/total < 0.5 && rank >= 4) continue;
                        let newStat = getNewStat(topNPicksFactory, count, {'type': 'pick', rank, choice, });
                        this.statsList.push(newStat);
                    }
                }

                if (stats.preferences) {
                    let prefsFactory = function(stat) {
                        if (stat.operator === '>') {
                            if (stat.count === 0) {
                                return `No ballots ranked <b>${stat.choice1}</b> above <b>${stat.choice2}</b>!`;
                            } else if (stat.percent < 10.0) {
                                return `Merely <b>${stat.percent}%</b> of ballots ranked <b>${stat.choice1}</b> above <b>${stat.choice2}</b>!`;
                            } else if (stat.percent < 30.0) {
                                return `Only <b>${stat.percent}%</b> of ballots preferred <b>${stat.choice1}</b> to <b>${stat.choice2}</b>!`;
                            } else if (stat.percent < 66.65) {
                                return `<b>${stat.percent}%</b> of ballots preferred <b>${stat.choice1}</b> to <b>${stat.choice2}</b>!`;
                            } else {
                                return `Overwhelmingly, <b>${stat.percent}%</b> of ballots preferred <b>${stat.choice1}</b> over <b>${stat.choice2}</b>!`;
                            }
                        } else if (stat.operator === '=') {
                            let ord = Math.random();
                            let c1, c2;
                            if (ord > 0.5) {
                                c1 = stat.choice1;
                                c2 = stat.choice2;
                            } else {
                                c1 = stat.choice2;
                                c2 = stat.choice1;
                            }
                            if (stat.count === 0) {
                                return `No ballots ranked <b>${c1}</b> equal to <b>${c2}</b>!`;
                            } else if (stat.percent < 10.0) {
                                return `Merely <b>${stat.percent}%</b> of ballots ranked <b>${c1}</b> equal to <b>${c2}</b>!`;
                            } else if (stat.percent < 30.0) {
                                return `Only <b>${stat.percent}%</b> of ballots ranked <b>${c1}</b> equal to <b>${c2}</b>!`;
                            } else if (stat.percent < 66.65) {
                                return `<b>${stat.percent}%</b> of ballots ranked <b>${c1}</b> equal to <b>${c2}</b>!`;
                            } else {
                                return `Overwhelmingly, <b>${stat.percent}%</b> of ballots ranked <b>${c1}</b> equal to <b>${c2}</b>!`;
                            }
                        }
                    }.bind(this);
                    for (let statKey in stats.preferences) {
                        if (statKey === 'total') continue;
                        let spl = statKey.split('>');
                        let choice1, choice2, operator;
                        if (spl.length === 2) {
                            choice1 = this.choiceIdToNameMap[spl[0]];
                            choice2 = this.choiceIdToNameMap[spl[1]];
                            operator = '>';
                        } else {
                            spl = statKey.split('=');
                            choice1 = this.choiceIdToNameMap[spl[0]];
                            choice2 = this.choiceIdToNameMap[spl[1]];
                            operator = '=';
                        }
                        let newStat = getNewStat(prefsFactory, stats.preferences[statKey], {'type': 'pref', choice1, choice2, operator});
                        this.statsList.push(newStat);
                    }
                }

                Common.shuffle(this.statsList);
                this.statsList.sort((a,b) => b.interest-a.interest);
                this.nextStats();
            }
        },
        nextStats: Common.methods.nextStats,
    },
    filters: {
        ...Common.filters,
    },
    mounted() {
        this.setPollModel(this.id);
    },
    watch: {
        type: {
            immediate: true,
            handler() {
                this.processStats();
            },
        }
    }
};
</script>

<style scoped>
.stat-seen {
    color: #A0A0A0;
}
</style>