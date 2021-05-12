<template>
    <v-container class="wrapper">
        <!-- Classic RCV -->
        <v-container v-if="isEdit" align=center class="wrapper">
            <v-simple-table dense v-if="update">
                <template v-slot:default>
                <thead>
                    <tr>
                        <th><!-- Empty Col --></th>
                        <th :colspan=choices.length class="text-center">
                            Score
                        </th>
                    </tr>
                    <tr>
                        <th><!-- Empty Col --></th>
                        <th
                            v-for="choice, idx in scoreList"
                            :key="idx"
                            class="text-left ballot-rank-text"
                        >
                            {{ choice }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="choice1, idx1 in choices"
                        :key="idx1"
                    >
                        <th>{{ choice1.name }}</th>
                        <th
                            v-for="choice2, idx2 in scoreList"
                            :key="idx2"
                            class="text-center ballot-rank-text"
                        >
                            <v-radio-group v-model="ballotMatrix[idx1][idx2].val">
                                <v-radio
                                    class="choiceRadioLabel"
                                    :value="true"
                                    @change="select(idx1, idx2, choice2)"
                                />
                            </v-radio-group>
                        </th>
                        <th>
                            <v-btn icon color="indigo" @click="clearBallotMatrixRow(idx1, true)">
                                <v-icon>mdi-close</v-icon>
                            </v-btn>
                        </th>
                    </tr>
                </tbody>
                </template>
            </v-simple-table>
        </v-container>
        <v-container v-if="isPreview" align=center class="wrapper">
            <v-chip-group
                multiple
                active-class="primary--text"
            >
                <v-chip
                    v-for="choice, idx in getSortedChoiceList"
                    :key="idx"
                >
                    {{ getChoiceNameFromId(choice.id) }} ({{ choice.score }})
                </v-chip>
            </v-chip-group>
        </v-container>
        <v-container v-if="isDisplay" align=center class="wrapper">
            TODO:
        </v-container>
    </v-container>
</template>

<script>
// import Choice from './Choice.vue';

export default {
    name: 'rcv-poll-ballot',
    props: {
        ballotContext: {
            type: Object,
            required: true,
        },
        choices: {
            type: Array,
            required: true,
        },
        isDisplay: {
            type: Boolean,
            required: false,
            default: false,
        },
        isEdit: {
            type: Boolean,
            required: false,
            default: false,
        },
        isPreview: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    components: {
        // 'poll-choice': Choice,
    },
    data() {
        return {
            ballotMatrix: [[]],
            scoreList: [5,4,3,2,1,0],
            update: 1,
        }
    },
    computed: {
      getSortedChoiceList() {
          return this.ballotContext.selected
            .filter((s) => !s.auto)
            .map((item, index) => {
                return {item, index};
            })
            .sort((a, b) => (b.item.score - a.item.score) || (a.index - b.index))
            .map(({item}) => item);
      },
    },
    methods: {
        getChoiceNameFromId(id) {
            for (let choiceIdx = 0; choiceIdx < this.choices.length; choiceIdx++) {
                if (this.choices[choiceIdx].id === id) {
                    return this.choices[choiceIdx].name;
                }
            }
            return null;
        },
        select(idx1, idx2, score) {
            // Clear other selections in this row
            this.clearBallotMatrixRow(idx1);

            let choice = this.choices[idx1];
            let selIdx = 0;
            for (; selIdx < this.ballotContext.selected.length; selIdx++) {
                if (this.ballotContext.selected[selIdx].id === choice.id) {
                    if (!this.ballotContext.selected[selIdx].auto) {
                        this.ballotContext.selected[selIdx].score = score;
                        break;
                    } else {
                        this.ballotContext.selected.splice(selIdx, 1);
                    }
                }
            }
            if (selIdx >= this.ballotContext.selected.length) {
                this.ballotContext.selected.push({
                    'id': choice.id,
                    'score': score,
                });
            }

            this.ballotMatrix[idx1][idx2].val = true;

            this.onChange();
        },
        clearBallotMatrixRow(rowIdx, clearSelected) {
            for (let colIter = 0; colIter < this.scoreList.length; colIter++) {
                this.ballotMatrix[rowIdx][colIter].val = false;
            }

            if (clearSelected) {
                let choice = this.choices[rowIdx];
                for (let selIdx = 0; selIdx < this.ballotContext.selected.length; selIdx++) {
                    if (this.ballotContext.selected[selIdx].id === choice.id) {
                        this.ballotContext.selected.splice(selIdx, 1);
                        break;
                    }
                }
            }

            this.onChange();
        },
        getBallotMatrix() {
            function getObj() {
                return {
                    val: false,
                }
            }

            let oldTable = this.ballotMatrix;
            let newTable = [];
            for (let idx1 = 0; idx1 < this.choices.length; idx1++) {
                newTable.push([]);
                for (let idx2 = 0; idx2 < this.scoreList.length; idx2++) {
                    let newVal = getObj();
                    if (oldTable.length > idx1 && oldTable[idx1].length > idx2) {
                        newVal = oldTable[idx1][idx2];
                    }
                    newVal.val = false;
                    if (this.ballotContext.selected) {
                        let choice = this.choices[idx1];
                        for (let selIdx = 0; selIdx < this.ballotContext.selected.length; selIdx++) {
                            if (this.ballotContext.selected[selIdx].id === choice.id && 
                                this.ballotContext.selected[selIdx].score === this.scoreList[idx2] &&
                                !this.ballotContext.selected[selIdx].auto) {
                                newVal.val = true;
                            }
                        }
                    }
                    newTable[idx1].push(newVal);
                }
            }
            return newTable;
        },
        onChange() {
            this.$emit('onChange');
        },
    },
    created() {
        this.ballotMatrix = this.getBallotMatrix();
    },
    mounted() {
        // Create the default selections
        for (let choiceIdx in this.choices) {
            let choice = this.choices[choiceIdx];
            let selIdx = 0;
            for (; selIdx < this.ballotContext.selected.length; selIdx++) {
                if (this.ballotContext.selected[selIdx].id === choice.id) {
                    break;
                }
            }
            if (selIdx === this.ballotContext.selected.length) {
                this.ballotContext.selected.push({
                    'id': choice.id,
                    'score': 0,
                    'auto': true,
                });
            }
        }
    },
    watch: {
        choices() {
            this.ballotMatrix = this.getBallotMatrix();
        },
        ballotContext() {
            this.ballotMatrix = this.getBallotMatrix();
        },
    }
};
</script>

<style scoped>
.wrapper {
    padding: 0px;
}
</style>