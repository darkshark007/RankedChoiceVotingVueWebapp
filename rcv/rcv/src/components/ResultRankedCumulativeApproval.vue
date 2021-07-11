<template>
    <div>
        <!-- Ranked Cumulative Approval (Bucklin) -->
        <v-card 
            class="pa-2 ma-0"
            elevation=2
            align=center
        >
            <div>
                    <p align=left>
                        Votes Required for Majority: {{ majority }}<br/>
                        Round: {{ this.explainStages[this.currentExplainStage].round }} / {{ this.rounds }}
                    </p>
            </div>
            <v-row>
                <v-col cols=1>
                    <v-btn
                        v-if="this.currentExplainStage !== this.explainStages.length-1"
                        icon
                        color="indigo"
                        :disabled="currentExplainStage === 0"
                        @click="currentExplainStage--"
                    >
                        <v-icon>mdi-page-previous-outline</v-icon>
                    </v-btn>
                </v-col>
                <v-col cols=9>
                    <div v-html="this.explainStages[this.currentExplainStage].message" class="text-center explain-message">
                        {{ this.explainStages[this.currentExplainStage].message }}
                    </div>
                </v-col>
                <v-col cols=1>
                    <v-btn
                        v-if="this.currentExplainStage !== this.explainStages.length-1"
                        icon
                        color="indigo"
                        @click="currentExplainStage++"
                    >
                        <v-icon>mdi-page-next-outline</v-icon>
                    </v-btn>
                </v-col>
            </v-row>
            <highcharts :options="chartOptions"></highcharts>
        </v-card>
        <v-divider class="mx-4"></v-divider>
        <div class="ma-4">
            <v-btn
                color="light-green lighten-4"
                elevation="2"
                :disabled="this.currentExplainStage !== this.explainStages.length-1"
                @click="currentExplainStage = 0"
            >
                Show me how it works!
            </v-btn>
        </div>
    </div>
</template>

<script>

export default {
    name: 'result-rca',
    props: {
        resultContext: {
            type: Object,
            required: true,
        },
        pollModel: {
            type: Object,
            required: true,
        },
    },
    components: {
    },
    computed: {
        choiceIdToNameMap() {
            let idToNameMap = {};
            for (let choiceKey in this.pollModel.activeChoices) {
                let choice = this.pollModel.activeChoices[choiceKey];
                idToNameMap[choice['id']] = choice['name'];
            }
            return idToNameMap;
        },
        majority() {
            return Math.floor(this.resultContext.count * 0.50)+1;
        },
        chartOptions() {
            return {
                chart: {
                    type: 'bar'
                },
                title: null,
                plotOptions: {
                    series: {
                        borderWidth: 0,
                        dataLabels: {
                            enabled: true,
                            format: '{point.y:.1f}%'
                        }
                    }
                },
                tooltip: {
                    // headerFormat: '<span style="font-size:11px">{point.name}</span><br>',
                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>: <b>{point.votes}</b> votes<br/>'
                },
                xAxis: {
                    categories: this.explainStages[this.currentExplainStage].choiceList,
                    // title: {
                    //     text: 'Choices',
                    // }
                },
                yAxis: {
                    title: null,
                    max: 100,
                },
                series: [{
                    showInLegend: false,
                    colorByPoint: true,
                    name: "Votes",
                    data: this.explainStages[this.currentExplainStage].choiceData,
                    max: 0,
                }]
            };
        },
    },
    methods: {
        processResults() {
            // ============================================================
            // Ranked Cumulative Approval
            // ============================================================
            this.explainStages = [];
            let results = {...this.resultContext['ranked_cumulative_approval']};
            delete results['stats'];
            let total = this.resultContext.count;
            let majority = this.majority;
            let addExplainStage = function(message, scoreMap, round) {
                let data = {
                    'message': message,
                    'round': round,
                };
                data['choiceData'] = [];
                for (let choiceKey in scoreMap) {
                    data['choiceData'].push({
                        'y': scoreMap[choiceKey] * 100.0 / total,
                        'votes': scoreMap[choiceKey],
                    });
                }

                data['choiceList'] = [];
                for (let choiceKey in scoreMap) {
                    data['choiceList'].push(this.choiceIdToNameMap[choiceKey]);
                }

                this.explainStages.push(data);
            }.bind(this);

            let choiceScoresMap = null;
            let choiceScoresByRoundMap = {};
            let topN = 1;
            let calculateScores = function() {
                choiceScoresMap = {};
                for (let choiceKey in this.pollModel.activeChoices) {
                    let choice = this.pollModel.activeChoices[choiceKey];
                    choiceScoresMap[choice.id] = 0;
                }

                function _calculateScoresRecursive(current, depth) {
                    if (depth >= topN) return;
                    for (let choiceKey in current) {
                        if (choiceKey === 'count') continue;
                        choiceScoresMap[choiceKey] += current[choiceKey]['count'];
                        _calculateScoresRecursive(current[choiceKey], depth+1);
                    }
                }
                _calculateScoresRecursive(results, 0);
                choiceScoresByRoundMap[topN] = choiceScoresMap;
            }.bind(this);

            // Get initial Score Distribution
            calculateScores();

            addExplainStage('Ranked Cumulative Approval Voting is an iterative Runoff process that continues until one Choice has more than 50% of the total vote. (Absolute majority)', choiceScoresMap, topN);
            addExplainStage('First, we tally up all of the First-Rank choices...', choiceScoresMap, topN);
            let winner = [];
            let lastScoresCalculated = JSON.stringify(choiceScoresMap);
            let result = "";
            while (topN <= this.pollModel.activeChoices.length) {
                winner = [];
                addExplainStage(`Then we check again to see if any of the Choices have more than 50% of the total vote...`, choiceScoresMap, topN)
                for (let choiceKey in choiceScoresMap) {
                    if (winner.length > 0) {
                        if (choiceScoresMap[choiceKey] > choiceScoresMap[winner[0]]) {
                            winner = [choiceKey];
                        } else if (choiceScoresMap[choiceKey] === choiceScoresMap[winner[0]]) {
                            winner.push(choiceKey);
                        }
                    } else {
                        winner.push(choiceKey);
                    }
                }
                if (winner.length > 0 && choiceScoresMap[winner[0]] >= majority) {
                    result = 'Absolute Majority';
                    break;
                }

                addExplainStage(`It looks like there is no majority yet!`, choiceScoresMap, topN);

                topN++;
                calculateScores();
                addExplainStage(`We'll sum up the scores again, but including the Top-${topN} Ranked choices from each ballot...`, choiceScoresMap, topN);
                let tempScoresCalculated = JSON.stringify(choiceScoresMap);
                if (tempScoresCalculated === lastScoresCalculated) {
                    addExplainStage(`It looks like there are no more Ballot rankings to count, but we still don't have a Choice with an Absolute Majority!`, choiceScoresMap, topN);
                    addExplainStage(`In this case, the winner is simply the choice with the most votes.`, choiceScoresMap, topN);
                    result = 'Simple Majority after exhausting the count';
                    break;
                }
                lastScoresCalculated = tempScoresCalculated;
            }
            this.rounds = topN;
            if (winner.length === 1) {
                // Single Winner
                addExplainStage(`It looks like ${this.choiceIdToNameMap[winner[0]]} has a Majority!`, choiceScoresMap, topN);
                addExplainStage(`Result:<br/>Winner, by ${result}: ${this.choiceIdToNameMap[winner[0]]}`, choiceScoresMap, topN);
            } else {
                // Tie
                let message = `It looks multiple choices are tied!<br/>`;
                for (let choiceKey in winner) {
                    message += `${this.choiceIdToNameMap[winner[choiceKey]]}</br>`;
                }
                addExplainStage(message, choiceScoresMap, topN);

                // Can we break the tie?
                let best = true;
                let bestWinner = null;
                let bestRound = 1;
                addExplainStage(`We may be able to resolve the tie by looking at previous rounds.  Did any of the choices defeat all the other tie choices outright at higher rankings?`, choiceScoresMap, topN);
                for (; bestRound <= topN; bestRound++) {
                    choiceScoresMap = {};
                    for (let choiceKey in choiceScoresByRoundMap[bestRound]) {
                        if (winner.includes(choiceKey)) {
                            choiceScoresMap[choiceKey] = choiceScoresByRoundMap[bestRound][choiceKey];
                        }
                    }
                    addExplainStage(`Let's check Rank-${bestRound}, comparing only those choices which tied...`, choiceScoresMap, bestRound+"*");
                    for (bestWinner in winner) {
                        best = true;
                        for (let otherChoiceKey in winner) {
                            if (bestWinner === otherChoiceKey) continue;
                            if (choiceScoresMap[winner[otherChoiceKey]] >= choiceScoresMap[winner[bestWinner]]) {
                                best = false;
                                addExplainStage(`It looks like ${this.choiceIdToNameMap[winner[bestWinner]]} was not more popular than all the other tied choices...`, choiceScoresMap, bestRound+"*");
                                break;
                            }
                        }
                        if (best) break;
                    }
                    if (best) break;
                }
                if (best) {
                    addExplainStage(`It looks like in Round #${bestRound}, including only each ballots Top-${bestRound} choices, ${this.choiceIdToNameMap[winner[bestWinner]]} was the most popular choice!`, choiceScoresMap, bestRound+"*");
                    addExplainStage(`Result:<br/>Winner, by ${result} after Tie Resolution: ${this.choiceIdToNameMap[winner[bestWinner]]}`, choiceScoresByRoundMap[this.rounds], this.rounds);
                } else {
                    let message = `Result:<br/>Tie<br/>`;
                    for (let choiceKey in winner) {
                        message += `${this.choiceIdToNameMap[winner[choiceKey]]}</br>`;
                    }
                    addExplainStage(message, choiceScoresMap, this.rounds+"*");
                }
            }
        },
    },
    mounted() {
        // this.chartOptions.xAxis = {
        //     ...this.chartOptions.xAxis,
        //     categories: this.choiceList,
        // };
        // this.chartOptions.yAxis = {
        //     ...this.chartOptions.yAxis,
        //     max: 100,
        // };
        this.chartOptions.series[0] = {
            ...this.chartOptions.series[0],
            data: this.choiceData,
        };
    },
    data: () => {
        return {
            explainStages: [],
            currentExplainStage: 0,
            rounds: 0,
        };
    },
    watch: {
        resultContext: {
            immediate: true,
            handler() {
                this.processResults();
                this.currentExplainStage = this.explainStages.length-1;
            },
        }
    }
};
</script>

<style scoped>
.explain-message {
    height: 130px;
}
</style>