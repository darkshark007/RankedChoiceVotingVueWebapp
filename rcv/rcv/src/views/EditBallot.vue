<template>
    <div id="editPoll" align="center">
        <v-container>
            <v-card
                class="wrapper"
                id="loading-card"
                max-width="500px"
                align="center"
                v-if="loading > 0"
                :loading="loading > 0"
            ></v-card>
            <message-card
                :errorString=errorString
                errorStringBase="Error loading Poll: "
            ></message-card>
            <v-card
                class="wrapper"
                max-width="500px"
                align="center"
                v-if="!loading > 0"
            >
                <div v-if="!pollModel.id"> Poll with that ID was not found.</div>
                <div v-else>
                    <v-card-title>
                        {{ pollModel.name }}
                        <v-spacer></v-spacer>
                        <nav-button
                            :route="pollModel.pollRoute"
                            title="Back"
                            v-if="pollModel.pollRoute"
                        ></nav-button><!-- TODO: Add confirmation modal if changes? -->
                    </v-card-title>
                    <v-card-subtitle align=left>
                        {{ pollModel.description }}
                    </v-card-subtitle>
                    <div><v-divider class="ma-4"></v-divider></div>
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
                    </v-row>
                    <div><v-divider class="ma-4"></v-divider></div>
                    <v-row>
                        <v-col class="subheader" cols=8>
                            <h4>Add new Choices</h4>
                        </v-col>
                        <v-col cols=2>
                            <v-btn
                                fab
                                small
                                color="light-green lighten-4"
                                :disabled="pollModel.locked"
                                @click="addChoice"
                            >
                                <v-icon color="indigo">mdi-plus</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>
                    <poll-choice 
                        v-for="choice, idx in newChoices"
                        :key="idx"
                        :choice="choice"
                        :edit="true"
                        @remove="removeChoice(choice)"
                    ></poll-choice>
                    <v-row v-if="newChoices.length > 0">
                        <v-col cols=12>
                            <v-spacer></v-spacer>
                            <!-- TODO: Refactor button -->
                            <v-btn
                                color="light-green lighten-4"
                                elevation="2"
                                :loading="savingChoices"
                                @click="saveChoices"
                            >
                                Save New Choices
                            </v-btn>
                        </v-col>
                    </v-row>
                    <message-card
                        :errorString=saveChoicesErrorString
                        errorStringBase="Error Saving New Choices: "
                        :successString=saveChoicesSuccessString
                    ></message-card>
                    <div><v-divider class="ma-4"></v-divider></div>
                    <v-row>
                        <v-col class="subheader" cols=8>
                            <h4>Ballot</h4>
                        </v-col>
                        <v-col cols=2 v-if="generated">
                            <v-tooltip bottom max-width="300px">
                                <template v-slot:activator="{ on, attrs }">
                                    <v-icon
                                        color="red"
                                        v-bind="attrs"
                                        v-on="on"
                                        class="ma-2"
                                    >
                                    mdi-hammer-wrench
                                    </v-icon>
                                </template>
                                <span>This <i>{{ this.selectedType | displayPollType }}</i>-style Ballot was pre-filled using data from your other filled-out similar-style ballot(s).<br/><br/>Selections on this ballot form may change to reflect changes made to the selections in other forms.  Modify the values in this form to lock them in and clear the 'Generated'-Ballot status.</span>
                            </v-tooltip>
                        </v-col>
                    </v-row>
                    <v-text-field
                        label="Name"
                        v-model="ballotContext.name"
                    ></v-text-field>
                    <v-select
                        label="Ballot Style"
                        :items="pollTypeList"
                        item-text="name"
                        item-value="id"
                        v-model="selectedType"
                    ></v-select>
                    <form-checkbox
                        title="This Ballot is Public"
                        tooltip="If Selected, this Ballot and its choices will be visible to anyone on the Poll page.<br/><br/><b>Note:</b> If switch cannot be toggled, this means that this Poll's creator set <b><i>all</i></b> Ballots to either public or private."
                        :disabled="pollModel.publicBallots !== 'maybe'"
                        v-model="ballotContext.publicBallot"
                    />
                    <ballot
                        :ballotContext="getContextForType()"
                        :choices="pollModel.choices"
                        :type="selectedType"
                        :edit="true"
                        @onChange="onBallotChange"
                    />
                    <v-row>
                        <v-col cols=12>
                            <v-spacer></v-spacer>
                            <!-- TODO: Refactor button -->
                            <v-btn
                                color="light-green lighten-4"
                                elevation="2"
                                :loading="savingBallot"
                                :disabled="pollModel.locked"
                                @click="saveBallot"
                            >
                                Save Ballot
                            </v-btn>
                        </v-col>
                    </v-row>
                    <message-card
                        :errorString="saveBallotErrorString"
                        errorStringBase="Error Saving Ballot: "
                        :successString="saveBallotSuccessString"
                    ></message-card>
                </div>
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
                    <v-row>
                        <v-col cols=9>
                            <v-card-text align=left>
                                <p>
                                    Your ballot is <b>{{ ballotSimilarity(ballotContext.stats, selectedType) }}%</b> similar to other ballots.<br/>
                                </p>
                            </v-card-text>
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
        </v-container>
    </div>
</template>

<script>
import Common from '../common.js';
import MessageCard from '../components/MessageCard.vue';
import NavButton from '../components/NavButton.vue';
import Choice from '../components/Choice.vue';
import Ballot from '../components/Ballot.vue';
import FormCheckbox from '../components/FormCheckbox.vue';


export default {
    name: 'edit-ballot-component',
    props: {
        pollid: {
            type: String,
            required: false,
        },
        ballotid: {
            type: String,
            required: false,
        },
    },
    components: {
        'message-card': MessageCard,
        'nav-button': NavButton,
        'form-checkbox': FormCheckbox,
        'poll-choice': Choice,
        'ballot': Ballot,
    },
    data: () => {
        return {
            pollTypeList: Common.data.pollTypeList,
            pollModel: Common.getEmptyPollContext(),
            ballotContext: Common.getEmptyBallotContext(),
            selectedType: '',
            newChoices: [],
            statsList: [],
            displayStats: [],
            loading: 0,
            errorString: null,
            savingChoices: false,
            saveChoicesSuccessString: null,
            saveChoicesErrorString: null,
            savingBallot: false,
            saveBallotSuccessString: null,
            saveBallotErrorString: null,
            generated: false,
        };
    },
    filters: {
        displayPollType: Common.filters.displayPollType,
        displayDate: Common.filters.displayDate,
    },
    computed: {
        choiceIdToNameMap: Common.computed.choiceIdToNameMap,
    },
    methods: {
        ballotSimilarity: Common.methods.ballotSimilarity,
        processStats() {
            this.statsList = [];
            if (!this.pollModel || !this.ballotContext || !this.ballotContext.stats) return;
            let total = this.ballotContext.stats.ballotCount-1;
            if (total <= 0) return;
            let getNewStat = function(getMessage, count, extra) {
                count = count-1;
                let percent = Math.floor(10000.0*(count/total))/100;
                let baseInterest = Math.abs(count-(total/2)); // Balance high counts and low counts?
                // let baseInterest = count;
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

            let stats = this.ballotContext['stats'][this.selectedType];
            if (stats) {
                if (stats.included) {
                    let includedFactory = function(stat) {
                        stat.interest *= 0.75;
                        if (stat.count === 0) {
                            stat.interest *= 0.5;
                            return `<b>No</b> other voters included <b>${stat.choice}</b> as a pick!`;
                        } else if (stat.percent > 25.0) {
                            return `<b>${stat.percent}%</b> of other voters also included <b>${stat.choice}</b> as a pick!`;
                        } else {
                            return `Only <b>${stat.percent}</b>% of other voters also included <b>${stat.choice}</b> as a pick!`;
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
                        if (stat.count === 0) {
                            return `<b>No</b> other voters picked <b>${stat.choice}</b> as their #${stat.rank} pick!`;
                        } else if (stat.percent > 66.65) {
                            return `<b>${stat.percent}%</b> of other voters agree with you, and also picked <b>${stat.choice}</b> as their #${stat.rank} pick!`;
                        } else if (stat.percent > 25.0) {
                            return `<b>${stat.percent}%</b> of other voters also picked <b>${stat.choice}</b> as their #${stat.rank} pick!`;
                        } else {
                            return `Only <b>${stat.percent}</b>% of other voters also picked <b>${stat.choice}</b> as their #${stat.rank} pick!`;
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

                if (stats.top_n_picks) {
                    let topNPicksFactory = function(stat) {
                        if (stat.count === 0) {
                            return `<b>No</b> other voters ranked <b>${stat.choice}</b> among their Top-${stat.rank} picks!`;
                        } else if (stat.percent > 25.0) {
                            return `<b>${stat.percent}%</b> of other voters also ranked <b>${stat.choice}</b> among their Top-${stat.rank} picks!`;
                        } else {
                            return `Only <b>${stat.percent}</b>% of other voters also ranked <b>${stat.choice}</b> among their Top-${stat.rank} picks!`;
                        }
                    }.bind(this);
                    for (let statKey in stats.top_n_picks) {
                        if (statKey === 'total') continue;
                        let spl = statKey.split('-');
                        let rank = (1*spl[0])+1;
                        let count = stats.top_n_picks[statKey];
                        let choice = this.choiceIdToNameMap[spl[1]];
                        if (count/total < 0.5 && rank >= 4) continue;
                        let newStat = getNewStat(topNPicksFactory, count, {'type': 'pick', rank, choice, });
                        this.statsList.push(newStat);
                    }
                }

                if (stats.preferences) {
                    let prefsFactory = function(stat) {
                        if (stat.operator === '>') {
                            if (stat.count === 0) {
                                stat.interest *= 0.5;
                                return `<b>No</b> other voters ranked <b>${stat.choice1}</b> above <b>${stat.choice2}</b>!`;
                            } else if (stat.percent < 10.0) {
                                return `Merely <b>${stat.percent}%</b> of other voters also ranked <b>${stat.choice1}</b> above <b>${stat.choice2}</b>!`;
                            } else if (stat.percent < 30.0) {
                                return `Only <b>${stat.percent}%</b> of other voters preferred <b>${stat.choice1}</b> to <b>${stat.choice2}</b>!`;
                            } else if (stat.percent < 66.65) {
                                return `<b>${stat.percent}%</b> of other voters also preferred <b>${stat.choice1}</b> to <b>${stat.choice2}</b>!`;
                            } else {
                                return `Overwhelmingly, <b>${stat.percent}%</b> of other voters agreed with you, preferring <b>${stat.choice1}</b> over <b>${stat.choice2}</b>!`;
                            }
                        } else if (stat.operator === '=') {
                            // TODO: Implement
                        }
                    }.bind(this);
                    for (let statKey in stats.preferences) {
                        if (statKey === 'total') continue;
                        let spl = statKey.split('>');
                        let choice1, choice2, operator;
                        if (spl.length === 2) {
                            choice1 = this.choiceIdToNameMap[spl[0]];
                            choice2 = this.choiceIdToNameMap[spl[1]];
                            operator = '>'
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
        addChoice() {
            let new_choice = Common.getEmptyChoiceContext();
            this.newChoices.push(new_choice);
        },
        removeChoice(choice) {
            let choiceIdx = this.newChoices.indexOf(choice);
            this.newChoices.splice(choiceIdx, 1);
        },
        getContextForType() {
            this.updateGeneratedBallots();

            if (this.ballotContext && 
                this.ballotContext.context[this.selectedType] && 
                this.ballotContext.context[this.selectedType].generated) {
                this.generated = true;
            } else {
                this.generated = false;
            }

            if (this.selectedType) {
                return this.ballotContext.context[this.selectedType];
            }
            return Common.getEmptyBallotContext();
        },
        saveChoices() {
            let data = {
                ...this.pollModel,
                choices: [
                    ...this.pollModel.choices,
                    ...this.newChoices,
                ],
            };
            this.savingChoices = true;
            this.saveChoicesErrorString = null;
            this.saveChoicesSuccessString = null;
            Common.savePoll(data)
                    .then(data => {
                        this.saveChoicesSuccessString = "New Choices Saved!";
                        this.pollModel = data;
                        this.newChoices = [];
                    })
                    .catch((error) => {
                        this.saveChoicesErrorString = error;
                    })
                    .finally(() => {
                        this.savingChoices = false;
                    });
        },
        saveBallot() {
            // Validate
            let errors = false;
            this.saveBallotErrorString = null;
            if (!this.ballotContext.name) {
                errors = true;
                setTimeout(function() {
                    // Hate this.
                    this.saveBallotErrorString = 'Name is required!';
                }.bind(this), 0);
            }
            if (errors) return;

            // Save
            this.updateGeneratedBallots();
            let data = {
                'pollId': this.pollModel.id,
                'ballot': this.ballotContext,
                'includeStats': true,
            };
            this.savingBallot = true;
            this.saveBallotErrorString = null;
            this.saveBallotSuccessString = null;
            Common.saveBallot(data)
                    .then((data) => {
                        this.saveBallotSuccessString = "Ballot Saved!";
                        this.ballotContext = data;
                        if (!this.ballotid) {
                            this.$router.push({name: 'editBallotsWithId', params: { pollid: this.pollid, ballotid: data.id } });
                        }
                    })
                    .catch((error) => {
                        this.saveBallotErrorString = error;
                    })
                    .finally(() => {
                        this.savingBallot = false;
                        this.syncPollBallotSettings();
                    });
        },
        setPollModel(id) {
            this.pollModel = Common.getEmptyPollContext()
            if (id) {
                this.loading += 1;
                Common.getPollData({'id': id})
                    .then(data => {
                        this.pollModel = data;
                        this.selectedType = this.pollModel.type;
                    })
                    .catch((error) => {
                        this.errorString = error;
                    })
                    .finally(() => {
                        this.loading -= 1;
                        this.syncPollBallotSettings();
                    });
            }
        },
        setBallotModel(pollId, ballotId) {
            this.ballotContext = Common.getEmptyBallotContext()
            if (pollId && ballotId) {
                this.loading += 1;
                Common.getBallotData(pollId, ballotId, true)
                    .then(data => {
                        this.ballotContext = data;
                    })
                    .catch((error) => {
                        this.errorString = error;
                    })
                    .finally(() => {
                        this.loading -= 1;
                        this.syncPollBallotSettings();
                    });
            }
        },
        syncPollBallotSettings() {
            if (this.loading > 0) {
                return                
            }
            if (this.pollModel.publicBallots === 'yes') {
                this.ballotContext.publicBallot = true;
            } else if (this.pollModel.publicBallots === 'no') {
                this.ballotContext.publicBallot = false;
            }

            this.processStats();
        },
        updateGeneratedBallots() {
            const fptp = 'fptp';
            const rcv = 'classic_rcv';
            const rca = 'ranked_cumulative_approval';
            const star = 'star_vote';

            function getRankFromScore(arr) {
                return arr
                    .filter((s) => !s.auto)
                    .map((item, index) => ({item, index}))
                    .sort((a, b) => (b.item.score - a.item.score) || (a.index - b.index))
                    .map(({item}) => item.id)
            }

            // FPTP
            if (!this.ballotContext.context[fptp]) {
                this.ballotContext.context[fptp] = {
                    'generated': true,
                    'selected': null,
                };
            }
            if (this.ballotContext.context[fptp].generated) {
                let tempSelected = null;
                if (!tempSelected && this.ballotContext.context[rcv] && !this.ballotContext.context[rcv].generated) {
                    tempSelected = this.ballotContext.context[rcv].selected[0];
                }
                if (!tempSelected && this.ballotContext.context[rca] && !this.ballotContext.context[rca].generated) {
                    tempSelected = this.ballotContext.context[rca].selected[0];
                }
                if (!tempSelected && this.ballotContext.context[star] && !this.ballotContext.context[star].generated) {
                    tempSelected = getRankFromScore(this.ballotContext.context[star].selected)[0];
                }
                if (this.ballotContext.context[fptp].selected !== tempSelected) {
                    this.ballotContext.context[fptp].selected = tempSelected;
                }
            }

            // RCV
            if (!this.ballotContext.context[rcv]) {
                this.ballotContext.context[rcv] = {
                    'generated': true,
                    'selected': [],
                };
            }
            if (this.ballotContext.context[rcv].generated) {
                let tempSelected = [];
                if (tempSelected.length === 0 && this.ballotContext.context[rca] && !this.ballotContext.context[rca].generated) {
                    tempSelected = [...this.ballotContext.context[rca].selected];
                }
                if (tempSelected.length === 0 && this.ballotContext.context[star] && !this.ballotContext.context[star].generated) {
                    tempSelected = getRankFromScore(this.ballotContext.context[star].selected);
                }
                if (tempSelected.length === 0 && this.ballotContext.context[fptp] && !this.ballotContext.context[fptp].generated) {
                    tempSelected = [this.ballotContext.context[fptp].selected];
                }
                if (this.ballotContext.context[rcv].selected.join('_') !== tempSelected.join('_')) {
                    this.ballotContext.context[rcv].selected = tempSelected;
                }
            }

            // RCA
            if (!this.ballotContext.context[rca]) {
                this.ballotContext.context[rca] = {
                    'generated': true,
                    'selected': [],
                };
            }
            if (this.ballotContext.context[rca].generated) {
                let tempSelected = [];
                if (tempSelected.length === 0 && this.ballotContext.context[rcv] && !this.ballotContext.context[rcv].generated) {
                    tempSelected = [...this.ballotContext.context[rcv].selected];
                }
                if (tempSelected.length === 0 && this.ballotContext.context[star] && !this.ballotContext.context[star].generated) {
                    tempSelected = getRankFromScore(this.ballotContext.context[star].selected);
                }
                if (tempSelected.length === 0 && this.ballotContext.context[fptp] && !this.ballotContext.context[fptp].generated) {
                    tempSelected = [this.ballotContext.context[fptp].selected];
                }
                if (this.ballotContext.context[rca].selected.join('_') !== tempSelected.join('_')) {
                    this.ballotContext.context[rca].selected = tempSelected;
                }
            }

            // STAR Vote
            let context = this.ballotContext.context[star];
            if (!context) {
                this.ballotContext.context[star] = {
                    'generated': true,
                    'selected': [],
                };
                context = this.ballotContext.context[star];
            }
            if (context.generated) {
                let tempSelected = [];
                if (tempSelected.length === 0 && this.ballotContext.context[rcv] && !this.ballotContext.context[rcv].generated) {
                    tempSelected = [...this.ballotContext.context[rcv].selected];
                }
                if (tempSelected.length === 0 && this.ballotContext.context[rca] && !this.ballotContext.context[rca].generated) {
                    tempSelected = [...this.ballotContext.context[rca].selected];
                }
                if (tempSelected.length === 0 && this.ballotContext.context[fptp] && !this.ballotContext.context[fptp].generated) {
                    tempSelected = [this.ballotContext.context[fptp].selected];
                }
                let count = 5;
                tempSelected = tempSelected.map(function(id) {
                    return {
                        'id': id,
                        'score': Math.max(count--,0),
                    };
                });
                for (let choiceIdx in this.pollModel.choices) {
                    let choice = this.pollModel.choices[choiceIdx];
                    let selIdx = 0;
                    for (; selIdx < tempSelected.length; selIdx++) {
                        if (tempSelected[selIdx].id === choice.id) {
                            break;
                        }
                    }
                    if (selIdx === tempSelected.length) {
                        tempSelected.push({
                            'id': choice.id,
                            'score': 0,
                            'auto': true,
                        });
                    }
                }
                if (JSON.stringify(context.selected) !== JSON.stringify(tempSelected)) {
                    context.selected = tempSelected;
                }
            }
        },
        onBallotChange() {
            this.ballotContext.context[this.selectedType].generated = false;
            this.generated = false;
        },
    },
    mounted() {
        this.setPollModel(this.pollid);
        if (this.ballotid) {
            this.setBallotModel(this.pollid, this.ballotid);
        }
        // TOOD: Make conditional/Query Param?
        window.editBallotContext = this;
    },
    watch: {
        "$route.params.pollid"(newId) {
            this.setPollModel(newId);
        },
        selectedType() {
            this.processStats();
        },
    }
};
</script>

<style scoped>
.stat-seen {
    color: #A0A0A0;
}
</style>
