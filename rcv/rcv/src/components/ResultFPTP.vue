<template>
    <div>
        <!-- Single-Choice Popular Vote (FPTP) -->
        <div align=center>
            <highcharts :options="chartOptions"></highcharts>
        </div>
    </div>
</template>

<script>

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
        choiceIdToNameMap() {
            let idToNameMap = {};
            for (let choiceKey in this.pollModel.choices) {
                let choice = this.pollModel.choices[choiceKey];
                idToNameMap[choice['id']] = choice['name'];
            }
            return idToNameMap;
        },
        choiceList() {
            let results = [];
            for (let choiceKey in this.resultContext['fptp']) {
                results.push(this.choiceIdToNameMap[choiceKey]);
            }

            return results
        },
        choiceData() {
            let results = [];
            let total = this.resultContext.count;
            for (let choiceKey in this.resultContext['fptp']) {
                results.push({
                    'y': this.resultContext['fptp'][choiceKey] * 100.0 / total,
                    'votes': this.resultContext['fptp'][choiceKey],
                });
            }

            return results
        },
    },
    mounted() {
        this.chartOptions.xAxis = {
            ...this.chartOptions.xAxis,
            categories: this.choiceList,
        };
        this.chartOptions.yAxis = {
            ...this.chartOptions.yAxis,
            max: 100,
        };
        this.chartOptions.series[0] = {
            ...this.chartOptions.series[0],
            data: this.choiceData,
        };
    },
    data: () => {
        return {
            chartOptions: {
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
                    categories: [],
                    // title: {
                    //     text: 'Choices',
                    // }
                },
                yAxis: {
                    title: null,
                },
                series: [{
                    showInLegend: false,
                    colorByPoint: true,
                    name: "Votes",
                    data: [],
                    max: 0,
                }]
            }
        }
    },
};
</script>

<style scoped>
</style>