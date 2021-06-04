<template>
    <div>
        <!-- Classic RCV -->
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
import Common from '../common.js';

export default {
    name: 'result-rcv',
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
        choiceIdToNameMap: Common.computed.choiceIdToNameMap,
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
        // choiceList() {
        //     let results = [];
        //     for (let choiceKey in this.resultContext['fptp']) {
        //         results.push(this.choiceIdToNameMap[choiceKey]);
        //     }

        //     return results
        // },
        // choiceData() {
        //     let results = [];
        //     let total = this.resultContext.count;
        //     for (let choiceKey in this.resultContext['fptp']) {
        //         results.push({
        //             'y': this.resultContext['fptp'][choiceKey] * 100.0 / total,
        //             'votes': this.resultContext['fptp'][choiceKey],
        //         });
        //     }

        //     return results
        // },
    },
    methods: {
        processResults() {
            this.explainStages = [];
            let results = {...this.resultContext['classic_rcv']};
            delete results['stats'];
            let total = this.resultContext.count;
            let majority = Math.floor(total * 0.50)+1;
            let addExplainStage = function(message, scoreMap, round) {
                scoreMap = {...scoreMap};
                let data = {
                    'message': message,
                    'round': round,
                };

                scoreMap['Exhausted'] = total;
                data['choiceData'] = [];
                for (let choiceKey in scoreMap) {
                    data['choiceData'].push({
                        'y': scoreMap[choiceKey] * 100.0 / total,
                        'votes': scoreMap[choiceKey],
                    });
                    scoreMap['Exhausted'] -= scoreMap[choiceKey];
                }

                data['choiceList'] = [];
                for (let choiceKey in scoreMap) {
                    let choiceName =
                        (choiceKey === 'Exhausted') ?
                            'Exhausted' : this.choiceIdToNameMap[choiceKey]
                    data['choiceList'].push(choiceName);
                }
                this.explainStages.push(data);
            }.bind(this);

            // Get initial Score Distribution
            let choiceEliminationMap = {};
            let choiceScoresMap = {};
            for (let choiceKey in this.pollModel.choices) {
                let choice = this.pollModel.choices[choiceKey];
                choiceScoresMap[choice.id] = 0;
            }
            for (let choiceKey in results) {
                choiceEliminationMap[choiceKey] = true;
                choiceScoresMap[choiceKey] = results[choiceKey]['count'];
            }

            let round = 1;
            addExplainStage('Ranked Choice Voting is an iterative Runoff process that continues until one Choice has more than 50% of the total vote. (Absolute majority)', choiceScoresMap, round);
            addExplainStage('First, we tally up all of the First-Rank choices...', choiceScoresMap, round);
            let winner = null;
            while (!winner) {
                addExplainStage(`Then we check again to see if any of the Choices have more than 50% of the total vote...`, choiceScoresMap, round)
                for (let choiceKey in choiceScoresMap) {
                    if (choiceScoresMap[choiceKey] >= majority) {
                        winner = this.choiceIdToNameMap[choiceKey];
                        addExplainStage(`It looks like ${winner} has a Majority!`, choiceScoresMap, round);
                        addExplainStage(`Result:<br/>Winner, by Absolute Majority: ${winner}`, choiceScoresMap, round);
                        break;
                    }
                }
                if (winner) break;

                addExplainStage(`It looks like there is no majority yet!`, choiceScoresMap, round);

                let lowestScore = Number.POSITIVE_INFINITY;
                let highestScore = Number.NEGATIVE_INFINITY;
                for (let choiceKey in choiceScoresMap) {
                    if (!choiceEliminationMap[choiceKey]) continue;
                    if (choiceScoresMap[choiceKey] < lowestScore) {
                        lowestScore = choiceScoresMap[choiceKey];
                    }
                    if (choiceScoresMap[choiceKey] > highestScore) {
                        highestScore = choiceScoresMap[choiceKey];
                    }
                }
                let lowestChoices = [];
                for (let choiceKey in choiceScoresMap) {
                    if (choiceScoresMap[choiceKey] === lowestScore) {
                        choiceEliminationMap[choiceKey] = false;
                        lowestChoices.push(this.choiceIdToNameMap[choiceKey]);
                    }
                }
                if (lowestScore === highestScore) {
                    if (lowestChoices.length === 1) {
                        if (lowestScore < majority) {
                            addExplainStage(`It looks like there is only one choice left, ${lowestChoices[0]}, but it got less than a majority of the votes.`, choiceScoresMap, round);
                            addExplainStage(`Result:<br/>Winner, by Simple Majority: ${lowestChoices[0]}`, choiceScoresMap, round);
                            break;
                        } else {
                            addExplainStage(`It looks like ${lowestChoices[0]} has a Majority!`, choiceScoresMap, round);
                            addExplainStage(`Result:<br/>Winner, by Absolute Majority: ${lowestChoices[0]}`, choiceScoresMap, round);
                            break;
                        }
                    } else {
                        addExplainStage(`It looks all the remaining choices are tied!`, choiceScoresMap, round);
                        addExplainStage(`Result:<br/>Tie`, choiceScoresMap, round);
                        break;
                    }
                }

                let message = `We will look for the lowest-voted Choice(s).  Those choices will be eliminated:<br/>`;
                for (let choiceKey in lowestChoices) {
                    message += `${lowestChoices[choiceKey]}</br>`;
                }
                addExplainStage(message, choiceScoresMap, round);

                let sumQueue = [results];
                round++;
                choiceScoresMap = {};
                for (let choiceKey in this.pollModel.choices) {
                    let choice = this.pollModel.choices[choiceKey];
                    choiceScoresMap[choice.id] = 0;
                }
                while (sumQueue.length > 0) {
                    let next = sumQueue.splice(0,1)[0];
                    for (let choiceKey in next) {
                        if (choiceEliminationMap[choiceKey]) {
                            choiceScoresMap[choiceKey] += next[choiceKey]['count'];
                        } else {
                            sumQueue.push(next[choiceKey]);
                        }
                    }
                }
                addExplainStage(`Then, Ballots which supported those choices will shift to support their next Choice.`, choiceScoresMap, round);
            }
            this.rounds = round;
            this.currentExplainStage = this.explainStages.length-1;
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