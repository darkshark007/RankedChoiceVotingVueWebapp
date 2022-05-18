<template>
    <v-container class="wrapper">
        <!-- Classic RCV -->
        <v-container v-if="isEdit" align=center class="wrapper">
            <form-checkbox
                title="Use Classic RCV Ballot Style"
                tooltip="If selected, this Ballot and its choices will be formatted in a classic RCV table-style.<br/>If not selected, then this Ballot and its choices will be formatted in a modern way more optimized for screen/device constraints."
                v-model="isClassicEdit"
            />
            <div v-if="isClassicEdit">
                <div class="pa-4">
                    <p align=left>
                        <b>Instructions:</b>  Rank each Choice in order of preference.
                    </p>
                    <p align=left v-if="pollModel.limitRankChoices">
                        * A maximum of <b>{{ pollModel.limitRankChoices }}</b> choices can be ranked.
                    </p>
                    <p align=left v-if="pollModel.ballotsMustBeFull">
                        * Ballot must be fully ranked!
                    </p>
                </div>
                <v-simple-table 
                    fixed-header 
                    height="600px" 
                    dense 
                    v-if="update"
                >
                    <template v-slot:default>
                    <thead>
                        <tr>
                            <th class="sticky-col first-col first-col-header"><!-- Empty Col --></th>
                            <th :colspan=1 class="text-center">
                                Best
                            </th>
                            <th v-if="ranks.length > 2" :colspan=ranks.length-2 class="text-center"></th>
                            <th :colspan=1 class="text-center">
                                Worst
                            </th>
                            <th class="sticky-col last-col"><!-- Empty Col --></th>
                        </tr>
                        <tr>
                            <th class="sticky-col first-col first-col-header"><!-- Empty Col --></th>
                            <th 
                                v-for="_, idx in ranks"
                                :key="idx"
                                class="text-center ballot-rank-text"
                            >
                                {{ idx+1 }}
                            </th>
                            <th class="sticky-col last-col"><!-- Empty Col --></th>                        
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="choice, rowIdx in choices"
                            :key="rowIdx"
                        >
                            <v-tooltip top>
                                <template v-slot:activator="{ on, attrs }">
                                    <th
                                        v-bind="attrs"
                                        v-on="on"
                                        class="sticky-col first-col"
                                    >
                                        {{ choice.name }}
                                    </th>
                                </template>
                                <template>
                                    <span><b>{{ choice.name }}</b></span><br/>
                                    <span>{{ choice.description }}</span>
                                </template>
                            </v-tooltip>
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
                            <th class="sticky-col last-col">
                                <v-btn icon color="indigo" @click="clearBallotMatrixRow(rowIdx)">
                                    <v-icon>mdi-close</v-icon>
                                </v-btn>
                            </th>
                        </tr>
                    </tbody>
                    </template>
                </v-simple-table>
            </div>
            <div v-else>
                <div class="pa-4">
                    <p align=left>
                        <b>Instructions:</b>  Rank each Choice in order of preference.  Click/tap a choice to rank it next or to un-rank it.  Drag choices to re-order.
                    </p>
                    <p align=left v-if="pollModel.limitRankChoices">
                        * A maximum of <b>{{ pollModel.limitRankChoices }}</b> choices can be ranked.
                    </p>
                    <p align=left v-if="pollModel.ballotsMustBeFull">
                        * Ballot must be fully ranked!
                    </p>
                    <v-list rounded dense align=center>
                        <draggable v-model="selected" @change="dragChoiceBox()">
                            <div 
                                v-for="element in selected"
                                :key="element.id" 
                                class="d-flex"
                                :style="{
                                    'width': '90%',
                                }"
                            >
                                <v-list-item
                                    :style="{
                                        'background-color': getColorForSelectionBox(element),
                                        'width': '90%',
                                    }"
                                    class="choiceBoxItem mb-1"
                                    :disabled="element.disabled"
                                    @click="selectChoiceBox(element)"
                                >
                                    <v-avatar v-if="element.selected" left size="25" class="green darken-3 white--text mr-2">{{element.rank}}</v-avatar>
                                    <div
                                        text-align=left
                                        :style="{
                                            'overflow': 'hidden',
                                            'white-space': 'nowrap',
                                            'text-overflow': 'ellipsis',
                                        }"
                                    >
                                        {{element.name}}
                                    </div>
                                </v-list-item>
                                <v-tooltip top>
                                    <template v-slot:activator="{ on, attrs }" right>
                                        <v-icon 
                                            v-bind="attrs" 
                                            v-on="on"
                                            :disabled=false
                                        >
                                            mdi-information-outline
                                        </v-icon>
                                    </template>
                                    <template>
                                        <span><b>{{ element.name }}</b></span><br/>
                                        <span>{{ element.description }}</span>
                                    </template>
                                </v-tooltip>
                            </div>
                        </draggable>
                    </v-list>
                </div>
            </div>
        </v-container>
        <v-container v-if="isPreview" align=center class="wrapper">
                <div
                    v-for="choice, idx in ballotContext.selected"
                    :key="idx"
                >
                    <v-chip-group
                        active-class="primary--text"
                    >
                        <v-chip>
                            {{ getChoiceNameFromId(choice) }}
                        </v-chip>
                    </v-chip-group>
                </div>
        </v-container>
        <v-container v-if="isDisplay" align=center class="wrapper">
            TODO:
        </v-container>
    </v-container>
    
</template>

<script>
// import Choice from './Choice.vue';
import FormCheckbox from '../components/FormCheckbox.vue';
import draggable from 'vuedraggable'

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
        classicEdit: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    components: {
        // 'poll-choice': Choice,
        'form-checkbox': FormCheckbox,
        draggable,
    },
    data() {
        return {
            ballotMatrix: [[]],
            update: 1,
            selected: [],
            isClassicEdit: this.classicEdit,
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
        updateChoiceBoxSelectionsFromBallot() {
            let selectedChoices = this.ballotContext.selected;
            this.selected = this.choices.map(function buildSelected(choice) {
                let index = selectedChoices.indexOf(choice.id);
                let isSelected = index !== -1;
                let rank = isSelected ? index+1 : Number.POSITIVE_INFINITY
                return {
                    'name': choice.name,
                    'id': choice.id,
                    'description': choice.description,
                    'selected': isSelected,
                    'rank': rank,
                };
            }).sort((a,b) => a.rank-b.rank);
            this.updateChoiceBoxList();
        },
        selectChoiceBox(element) {
            if (element.selected) {
                // Unselect it
                element.selected = false;
                element.rank = Number.POSITIVE_INFINITY;
            } else {
                // Select it next
                element.selected = true;
                element.rank = this.selected.filter((e) => e.selected).length;
            }
            this.updateChoiceBoxList();
            this.onChange();
        },
        dragChoiceBox() {
            // Select all intermingled options
            let found = false;
            for (let choiceIdx = this.selected.length-1; choiceIdx >= 0; choiceIdx--) {
                let choice = this.selected[choiceIdx];
                if (found) {
                    choice.selected = true;
                } else {
                    if (choice.selected) found = true;
                }
            }

            this.updateChoiceBoxList();
            this.onChange();
        },
        updateChoiceBoxList() {
            // Re-assign ranks
            let newRank = 1;
            let ranked = this.selected.filter((e) => e.selected);
            ranked.forEach((e) => e.rank = newRank++);

            // Re-sort list by rank
            this.selected.sort((a,b) => a.rank-b.rank);

            // Validate Limits
            this.selected.forEach((e) => e.disabled = false);
            if (ranked.length >= this.ranks.length) {
                for (let rankIdx = this.ranks.length; rankIdx < ranked.length; rankIdx++) {
                    let element = ranked[rankIdx];
                    element.selected = false;
                    element.rank = Number.POSITIVE_INFINITY;
                }
                this.selected.filter((e) => !e.selected).forEach((e) => e.disabled = true);
            }

            // Update Ballot
            ranked = this.selected.filter((e) => e.selected);
            this.ballotContext.selected = ranked.map((e) => e.id);
        },
        getColorForSelectionBox(element) {
            if (element.selected) return '#A5D6A7';
            if (element.disabled) return '#EF9A9A';
            return '#EEEEEE';
        },
        onChange() {
            this.$emit('onChange');
        },
    },
    created() {
        this.ballotMatrix = this.getBallotMatrix();
        this.updateChoiceBoxSelectionsFromBallot();
    },
    watch: {
        choices() {
            this.ballotMatrix = this.getBallotMatrix();
        },
        ballotContext() {
            this.ballotMatrix = this.getBallotMatrix();
            this.updateChoiceBoxSelectionsFromBallot();
        },
        isClassicEdit() {
            if (this.isClassicEdit) {
                // Switched to Classic mode
                this.ballotMatrix = this.getBallotMatrix();
            } else {
                // Switched to Regular mode
                this.updateChoiceBoxSelectionsFromBallot();
            }
            
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

.choiceRadioLabel {
    align-content: center;
    justify-content: center;
}

.wrapper {
    padding: 0px;
}

.sticky-col {
  position: -webkit-sticky;
  position: sticky;
  background-color: white !important;
  background: white !important;
}

.first-col {
  width: 100px;
  min-width: 100px;
  max-width: 100px;
  left: 0px;
  z-index: 4 !important;
}

.first-col-header {
  z-index: 5 !important;
}

.last-col {
  right: 0px;
  padding: 0px !important;
}

.choiceBoxItem {
    text-align: left;
    color: '#424242',
}
</style>