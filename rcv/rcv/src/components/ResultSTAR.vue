<template>
    <div>
        <!-- STAR Vote -->
        <v-card
            class="pa-2 ma-0"
            elevation=2
            align=center
        >
            <div>
                    <p align=left>
                        <!-- Votes Required for Majority: {{ majority }}<br/> -->
                        Round: {{ this.explainStages[this.currentExplainStage].round }}
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
            for (let choiceKey in this.pollModel.choices) {
                let choice = this.pollModel.choices[choiceKey];
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
                            format: '{point.y}{point.unit}'
                        }
                    }
                },
                tooltip: {
                    // headerFormat: '<span style="font-size:11px">{point.name}</span><br>',
                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b>{point.unit}<br/>'
                },
                xAxis: {
                    categories: this.explainStages[this.currentExplainStage].choiceList,
                    // title: {
                    //     text: 'Choices',
                    // }
                },
                yAxis: {
                    title: null,
                    max: this.explainStages[this.currentExplainStage].yMax,
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
            let results = {...this.resultContext['star_vote']};
            delete results['stats'];
            let addChoiceScoringExplainStage = function(choiceKey) {
                let data = {
                    'message': `These are the scores that ${this.choiceIdToNameMap[choiceKey]} got on the ballots:<br/><br/>Total Score: ${results[choiceKey]['score']}`,
                    'round': 'Scoring',
                    'yMax': this.resultContext.count,
                };
                data['choiceData'] = [];
                data['choiceList'] = [];
                for (let scoreIdx in this.scoreList) {
                    let scoreKey = this.scoreList[scoreIdx];
                    data['choiceData'].push({
                        'y': results[choiceKey][`score-${scoreKey}`] || 0,
                        'unit': 'x',
                    });
                    data['choiceList'].push(`Score ${scoreKey}`);
                }
                this.explainStages.push(data);
            }.bind(this);

            // Build Score Explain Stage
            let score_stage = {
                'message': 'Score Then Automatic Runoff (STAR) is a Score based system that runs in two stages.  Each choice is scored 0-5, and then their score is added up across all Ballots',
                'round': 'Scoring',
                'yMax': this.resultContext.count*5,
            };
            score_stage['choiceData'] = [];
            score_stage['choiceList'] = [];
            for (let choiceIdx in this.pollModel.choices) {
                let choiceKey = this.pollModel.choices[choiceIdx].id;
                score_stage['choiceData'].push({
                    'y': results[choiceKey]['score'],
                    'unit': 'pts',
                });
                score_stage['choiceList'].push(this.choiceIdToNameMap[choiceKey]);
            }
            this.explainStages.push(score_stage);

            for (let choiceIdx in this.pollModel.choices) {
                addChoiceScoringExplainStage(this.pollModel.choices[choiceIdx].id);
            }

            let select2Stage = {
                ...score_stage,
                'message': 'Next, we select 2 choices with the highest scores to go to the Runoff round.',
            }
            this.explainStages.push(select2Stage);
            let sortedByScore = Object.keys(results)
                .map((item, index) => {
                    results[item]['id'] = item;
                    return {item: results[item], index};
                })
                .sort((a, b) => (b.item.score - a.item.score) || (a.index - b.index))
                .map(({item}) => item)

            let scoring_stage_sorted = {
                'round': 'Scoring',
                'yMax': this.resultContext.count*5,
            };
            scoring_stage_sorted['choiceData'] = [];
            scoring_stage_sorted['choiceList'] = [];
            for (let choiceKey in sortedByScore) {
                scoring_stage_sorted['choiceData'].push({
                    'y': sortedByScore[choiceKey]['score'],
                    'unit': 'pts',
                });
                scoring_stage_sorted['choiceList'].push(this.choiceIdToNameMap[sortedByScore[choiceKey].id]);
            }

            let runoffChoices = [];
            if (sortedByScore.length === 1) {
                let winner = this.choiceIdToNameMap[sortedByScore[0].id];
                this.explainStages.push({
                    ...scoring_stage_sorted,
                    'message': `It looks like ${winner} is the only choice!`,
                });
                this.explainStages.push({
                    ...scoring_stage_sorted,
                    'message': `Result:<br/>Winner, un-opposed: ${winner}`,
                });
                return;
            } else if (sortedByScore.length > 2 && sortedByScore[1].score === sortedByScore[2].score) {
                let tiedChoices = [sortedByScore[1]];
                for (let choiceKey in sortedByScore) {
                    let choice = sortedByScore[choiceKey]
                    if (choice.id === tiedChoices[0].id) continue;
                    if (choice.score === tiedChoices[0].score) {
                        tiedChoices.push(choice);
                    }
                }
                if (tiedChoices.length > 2) {
                    this.explainStages.push({
                        ...scoring_stage_sorted,
                        'message': `It looks like there's a ${tiedChoices.length}-way tie before the Runoff round!`,
                    });
                    if (sortedByScore[0].score > sortedByScore[1].score) {
                        // THIS MULTI-CHOICE HIGH-SCORE TIE (with a dominant choice) IS UNDEFINED BEHAVIOR, but I'm calling it a resolvable tie
                        this.explainStages.push({
                            ...scoring_stage_sorted,
                            'message': `However, the highest-scoring choice, ${this.choiceIdToNameMap[sortedByScore[0].id]}, is not a part of the tie.`,
                        });
                        this.explainStages.push({
                            ...scoring_stage_sorted,
                            'message': `Result:<br/>Winner, by Dominant Choice amidst an unresolvable Runoff-Tie: ${this.choiceIdToNameMap[sortedByScore[0].id]}`,
                        });
                        return
                    } else {
                        // THIS MULTI-CHOICE HIGH-SCORE TIE IS UNDEFINED BEHAVIOR
                        this.explainStages.push({
                            ...scoring_stage_sorted,
                            'message': `Result:<br/>Tie`,
                        });
                        return;
                    }
                }
                this.explainStages.push({
                    ...scoring_stage_sorted,
                    'message': `It looks like there's a tie before the Runoff round!`,
                });
                runoffChoices.push(sortedByScore[0]);

                let tie_runoff_stage = {
                    'round': 'Tiebreaker Runoff',
                    'yMax': this.resultContext.count,
                };
                tie_runoff_stage['choiceData'] = [];
                tie_runoff_stage['choiceList'] = [];
                let gt_key = `>${tiedChoices[1].id}`;
                let lt_key = `<${tiedChoices[1].id}`;
                let eq_key = `=${tiedChoices[1].id}`;
                tie_runoff_stage['choiceData'].push({
                    'y': tiedChoices[0][gt_key] || 0,
                    'unit': ' ballots',
                });
                tie_runoff_stage['choiceList'].push(`${this.choiceIdToNameMap[tiedChoices[0].id]} Preferred`);
                tie_runoff_stage['choiceData'].push({
                    'y': tiedChoices[0][lt_key] || 0,
                    'unit': ' ballots',
                });
                tie_runoff_stage['choiceList'].push(`${this.choiceIdToNameMap[tiedChoices[1].id]} Preferred`);
                tie_runoff_stage['choiceData'].push({
                    'y': tiedChoices[0][eq_key] || 0,
                    'unit': ' ballots',
                });
                tie_runoff_stage['choiceList'].push(`Equally Preferred`);
                this.explainStages.push({
                    ...tie_runoff_stage,
                    'message': `To break the tie, we can re-examine the ballots and calculate the number of votes that preferred ${this.choiceIdToNameMap[tiedChoices[0].id]}, preferred ${this.choiceIdToNameMap[tiedChoices[1].id]}, or preferred both equally.`,
                });
                if ((tiedChoices[0][gt_key] || 0) > (tiedChoices[0][lt_key] || 0)) {
                    let winner = this.choiceIdToNameMap[tiedChoices[0].id];
                    this.explainStages.push({
                        ...tie_runoff_stage,
                        'message': `It looks like ${winner} is the more preferred choice, and breaks the tie!`,
                    });
                    runoffChoices.push(tiedChoices[0]);
                } else if ((tiedChoices[0][gt_key] || 0) < (tiedChoices[0][lt_key] || 0)) {
                    let winner = this.choiceIdToNameMap[tiedChoices[1].id];
                    this.explainStages.push({
                        ...tie_runoff_stage,
                        'message': `It looks like ${winner} is the more preferred choice, and breaks the tie!`,
                    });
                    runoffChoices.push(tiedChoices[1]);
                } else {
                    this.explainStages.push({
                        ...scoring_stage_sorted,
                        'message': `It looks like neither of the tied choices is more preferred than the other.  However, the highest-scoring choice, ${this.choiceIdToNameMap[sortedByScore[0].id]}, is not a part of the tie.`,
                    });
                    this.explainStages.push({
                        ...scoring_stage_sorted,
                        'message': `Result:<br/>Winner, by Dominant Choice amidst an unresolvable Runoff-Tie: ${this.choiceIdToNameMap[sortedByScore[0].id]}`,
                    });
                    return
                }
                this.explainStages.push({
                    ...scoring_stage_sorted,
                    'message': `After resolving the tie, we have ${this.choiceIdToNameMap[runoffChoices[0].id]} and ${this.choiceIdToNameMap[runoffChoices[1].id]} going to the Runoff round!`,
                });
            } else {
                runoffChoices.push(sortedByScore[0]);
                runoffChoices.push(sortedByScore[1]);
                this.explainStages.push({
                    ...scoring_stage_sorted,
                    'message': `It looks like ${this.choiceIdToNameMap[runoffChoices[0].id]} and ${this.choiceIdToNameMap[runoffChoices[1].id]} are the Top-2 highest scoring choices and will go to the Runoff round!`,
                });
            }

            let runoff_stage = {
                'round': 'Runoff',
                'yMax': this.resultContext.count,
            };
            runoff_stage['choiceData'] = [];
            runoff_stage['choiceList'] = [];
            let gt_key = `>${runoffChoices[1].id}`;
            let lt_key = `<${runoffChoices[1].id}`;
            let eq_key = `=${runoffChoices[1].id}`;
            runoff_stage['choiceData'].push({
                'y': runoffChoices[0][gt_key] || 0,
                'unit': ' ballots',
            });
            runoff_stage['choiceList'].push(`${this.choiceIdToNameMap[runoffChoices[0].id]} Preferred`);
            runoff_stage['choiceData'].push({
                'y': runoffChoices[0][lt_key] || 0,
                'unit': ' ballots',
            });
            runoff_stage['choiceList'].push(`${this.choiceIdToNameMap[runoffChoices[1].id]} Preferred`);
            runoff_stage['choiceData'].push({
                'y': runoffChoices[0][eq_key] || 0,
                'unit': ' ballots',
            });
            runoff_stage['choiceList'].push(`Equally Preferred`);
            this.explainStages.push({
                ...runoff_stage,
                'message': `Finally, during the Automatic Runoff round, we re-examine the ballots and calculate the number of votes that preferred ${this.choiceIdToNameMap[runoffChoices[0].id]}, preferred ${this.choiceIdToNameMap[runoffChoices[1].id]}, or preferred both equally.`,
            });
            if ((runoffChoices[0][gt_key] || 0) > (runoffChoices[0][lt_key] || 0)) {
                let winner = this.choiceIdToNameMap[runoffChoices[0].id];
                this.explainStages.push({
                    ...runoff_stage,
                    'message': `It looks like ${winner} is the more preferred choice!`,
                });
                this.explainStages.push({
                    ...runoff_stage,
                    'message': `Result:<br/>Winner, by Preferred Choice in the Runoff: ${winner}`,
                });
                return;
            } else if ((runoffChoices[0][gt_key] || 0) < (runoffChoices[0][lt_key] || 0)) {
                let winner = this.choiceIdToNameMap[runoffChoices[1].id];
                this.explainStages.push({
                    ...runoff_stage,
                    'message': `It looks like ${winner} is the more preferred choice!`,
                });
                this.explainStages.push({
                    ...runoff_stage,
                    'message': `Result:<br/>Winner, by Preferred Choice in the Runoff: ${winner}`,
                });
                return;
            } else {
                this.explainStages.push({
                    ...runoff_stage,
                    'message': `It looks like neither of the Runoff choices is more preferred than the other.`,
                });

                let tied_scoring_stage = {
                    'round': 'Tiebreaker Scoring',
                    'yMax': this.resultContext.count*5,
                };
                tied_scoring_stage['choiceData'] = [];
                tied_scoring_stage['choiceList'] = [];
                for (let choiceKey in runoffChoices) {
                    tied_scoring_stage['choiceData'].push({
                        'y': runoffChoices[choiceKey]['score'],
                        'unit': 'pts',
                    });
                    tied_scoring_stage['choiceList'].push(this.choiceIdToNameMap[sortedByScore[choiceKey].id]);
                }
                this.explainStages.push({
                    ...tied_scoring_stage,
                    'message': `We may be able to break the tie by comparing the scores of the tied choices.`,
                });
                if (runoffChoices[0]['score'] > runoffChoices[1]['score']) {
                    let winner = this.choiceIdToNameMap[runoffChoices[0].id];
                    this.explainStages.push({
                        ...tied_scoring_stage,
                        'message': `It looks like ${winner} is the higher-scoring choice, and breaks the tie!`,
                    });
                    this.explainStages.push({
                        ...tied_scoring_stage,
                        'message': `Result:<br/>Winner, by Runoff Tiebreak: ${winner}`,
                    });
                    return;
                } else if (runoffChoices[0]['score'] < runoffChoices[1]['score']) {
                    let winner = this.choiceIdToNameMap[runoffChoices[1].id];
                    this.explainStages.push({
                        ...tied_scoring_stage,
                        'message': `It looks like ${winner} is the higher-scoring choice, and breaks the tie!`,
                    });
                    this.explainStages.push({
                        ...tied_scoring_stage,
                        'message': `Result:<br/>Winner, by Runoff Tiebreak: ${winner}`,
                    });
                    return;
                } else {
                    this.explainStages.push({
                        ...tied_scoring_stage,
                        'message': `It looks like both choices have the same score, and we can't resolve the tie.`,
                    });
                    this.explainStages.push({
                        ...tied_scoring_stage,
                        'message': `Result:<br/>Tie`,
                    });
                    return;
                }
            }
        },
    },
    mounted() { },
    data: () => {
        return {
            explainStages: [],
            currentExplainStage: 0,
            rounds: 0,
            scoreList: [5,4,3,2,1,0],
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
    height: 140px;
}
</style>