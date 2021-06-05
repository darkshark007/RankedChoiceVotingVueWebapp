<template>
    <v-container class="wrapper">
        <!-- Classic RCV -->
        <v-container v-if="isEdit" align=center class="wrapper">
            <div class="pa-4">
                <p align=left>
                    <b>Instructions:</b>  Rank each Choice in order of preference.
                </p>
            </div>
            <v-simple-table dense v-if="update">
                <template v-slot:default>
                <thead>
                    <tr>
                        <th><!-- Empty Col --></th>
                        <th :colspan=1 class="text-center">
                            Best
                        </th>
                        <th v-if="ranks.length > 2" :colspan=ranks.length-2 class="text-center"></th>
                        <th :colspan=1 class="text-center">
                            Worst
                        </th>
                    </tr>
                    <tr>
                        <th><!-- Empty Col --></th>
                        <th 
                            v-for="_, idx in ranks"
                            :key="idx"
                            class="text-center ballot-rank-text"
                        >
                            {{ idx+1 }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="choice, rowIdx in choices"
                        :key="rowIdx"
                    >
                        <th>{{ choice.name }}</th>
                        <th 
                            v-for="_, colIdx in ranks"
                            :key="colIdx"
                            class="text-center ballot-rank-text"
                        >
                            <v-radio-group v-model="ballotMatrix[rowIdx][colIdx].val">
                                <v-radio
                                    class="choiceRadioLabel"
                                    :value="true"
                                    @change="select(rowIdx, colIdx)"
                                />
                            </v-radio-group>
                        </th>
                        <th>
                            <v-btn icon color="indigo" @click="clearBallotMatrixRow(rowIdx)">
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
                    v-for="choice, idx in ballotContext.selected"
                    :key="idx"
                >
                    {{ getChoiceNameFromId(choice) }}
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
        pollModel: {
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
            update: 1,
        }
    },
    computed: {
        ranks() {
            let count = this.choices.length;
            if (this.pollModel.limitRankChoices !== null) count = this.pollModel.limitRankChoices;
            return [...Array(count).keys()]
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
        select(idx1, idx2) {
            let checkColumnRecursive = function(colIdx) {
                if (colIdx >= this.ranks.length) return;
                for (let rowIter = 0; rowIter < this.choices.length; rowIter++) {
                    if (rowIter === idx1) continue;
                    if (this.ballotMatrix[rowIter][colIdx].val) {
                        checkColumnRecursive(colIdx+1);
                        this.ballotMatrix[rowIter][colIdx].val = false;
                        if (colIdx+1 < this.ranks.length) {
                            this.ballotMatrix[rowIter][colIdx+1].val = true;
                        }
                        return
                    }
                }
            }.bind(this);

            // Clear other selections in this row
            this.clearBallotMatrixRow(idx1);

            // Shift the columns down
            checkColumnRecursive(idx2);

            this.ballotMatrix[idx1][idx2].val = true;

            this.calculateSelected();

            this.onChange();
        },
        clearBallotMatrixRow(rowIdx) {
            for (let colIter = 0; colIter < this.ranks.length; colIter++) {
                this.ballotMatrix[rowIdx][colIter].val = false;
            }
            this.calculateSelected();
            this.onChange();
        },
        calculateSelected() {
            // Calculate selected ranking
            this.ballotContext.selected = [];
            for (let colIter = 0; colIter < this.ranks.length; colIter++) {
                for (let rowIter = 0; rowIter < this.choices.length; rowIter++) {
                    if (this.ballotMatrix[rowIter][colIter].val) {
                        this.ballotContext.selected.push(this.choices[rowIter].id);
                    }
                }
            }
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
                for (let idx2 = 0; idx2 < this.ranks.length; idx2++) {
                    let newVal = getObj();
                    if (oldTable.length > idx1 && oldTable[idx1].length > idx2) {
                        newVal = oldTable[idx1][idx2];
                    }
                    newVal.val = false;
                    if (this.ballotContext.selected && 
                        this.ballotContext.selected.length > idx2) {
                        if (this.ballotContext.selected[idx2] === this.choices[idx1].id) {
                            newVal.val = true;
                        } else {
                            newVal.val = false;
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
/* .ballot-rank-text {
    -webkit-transform: rotate(90deg);
    -webkit-transform-origin: left top;
    -moz-transform: rotate(90deg);
    -moz-transform-origin: left top;
    -ms-transform: rotate(90deg);
    -ms-transform-origin: left top;
    -o-transform: rotate(90deg);
    -o-transform-origin: left top;
    transform: rotate(90deg);
    transform-origin: left top;

    position: block;
    top: 0;
    left: 100%;
    white-space: nowrap;    
    font-size: 48px;
    writing-mode: tb-rl;
    transform: rotate(-90deg);
} */

.wrapper {
    padding: 0px;
}
</style>