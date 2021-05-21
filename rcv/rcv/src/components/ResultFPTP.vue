<template>
    <div>
        <!-- Single-Choice Popular Vote (FPTP) -->
        <v-card
            class="pa-2 ma-0"
            elevation=2
            align=center
        >
            <div>
                    <p align=left>
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
    name: 'result-fptp',
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
            this.explainStages = [];
            let results = {...this.resultContext['fptp']};
            delete results['stats'];
            let total = this.resultContext.count;
            let addExplainStage = function(message, scoreMap) {
                let data = {
                    'message': message,
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
                    let choiceName = this.choiceIdToNameMap[choiceKey];
                    data['choiceList'].push(choiceName);
                }
                this.explainStages.push(data);
            }.bind(this);

            // Get initial Score Distribution
            let choiceScoresMap = {};
            for (let choiceKey in this.pollModel.choices) {
                let choice = this.pollModel.choices[choiceKey];
                choiceScoresMap[choice.id] = 0;
            }
            choiceScoresMap = {
                ...choiceScoresMap,
                ...results,
            };

            addExplainStage('Single-Choice Popular Vote (Also known as First-Past-The-Post) is a single-vote single-round system, where the winner is the Choice with the highest number of votes.', choiceScoresMap);
            addExplainStage('First, we tally up all of votes cast...', choiceScoresMap);
            addExplainStage('Then we check to see which choice has the highest raw number of votes.', choiceScoresMap);

            let winners = [];
            for (let choiceKey in choiceScoresMap) {
                if (winners.length === 0 || choiceScoresMap[choiceKey] === choiceScoresMap[winners[0]]) {
                    winners.push(choiceKey);
                } else if (choiceScoresMap[choiceKey] > choiceScoresMap[winners[0]]) {
                    winners = [choiceKey];
                }
            }
            let percent = Math.floor(choiceScoresMap[winners[0]] * 1000.0 / total)/10.0;
            if (winners.length === 1) {
                if (percent > 50) {
                    addExplainStage(`It looks like the largest total is ${percent}%, from ${this.choiceIdToNameMap[winners[0]]}!`, choiceScoresMap);
                    addExplainStage(`Result:<br/>Winner, by Absolute Majority: ${this.choiceIdToNameMap[winners[0]]}`, choiceScoresMap);
                    return;
                } else {
                    addExplainStage(`It looks like the largest total is ${percent}%, from ${this.choiceIdToNameMap[winners[0]]}, but it didn't get more than half the votes.`, choiceScoresMap);
                    addExplainStage(`Result:<br/>Winner, by Simple Majority: ${this.choiceIdToNameMap[winners[0]]}`, choiceScoresMap);
                    return;
                }
            } else if (winners.length > 1) {
                addExplainStage(`It looks like there is a ${winners.length}-way tie for largest total, which is ${percent}%!`, choiceScoresMap);
                addExplainStage(`Result:<br/>Tie: ${winners.map(w => this.choiceIdToNameMap[w]).join(", ")}`, choiceScoresMap);
                return;
            }
        },
    },
    data: () => {
        return {
            explainStages: [],
            currentExplainStage: 0,
        }
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
</style>