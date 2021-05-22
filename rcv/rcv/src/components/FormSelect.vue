<template>
    <v-row class="cbrow" align=center>
        <v-col cols=1 v-if="tooltip">
            <v-tooltip bottom max-width="300px">
                <template v-slot:activator="{ on, attrs }">
                    <v-icon
                        color="gray"
                        v-bind="attrs"
                        v-on="on"
                        class="ma-2"
                    >
                    mdi-information-outline
                    </v-icon>
                </template>
                <span v-html="tooltip">{{ tooltip }}</span>
            </v-tooltip>
        </v-col>
        <v-col>
            <v-select
                :label="label"
                :items="items"
                item-text="name"
                item-value="value"
                :hint="selectedItemHint"
                v-model="local"
                :disabled=disabled
                return-object
                persistent-hint
            >
                <template v-slot:item="{ item }">
                    <v-tooltip bottom max-width="300px" v-if="itemHint(item)">
                        <template v-slot:activator="{ on, attrs }">
                            <div
                                class="v-list-item"
                                v-bind="attrs"
                                v-on="on"
                            >
                                <div class="v-list-item__content">
                                    <div class="v-list-item__title">
                                        {{ item.name }}
                                    </div>
                                </div>
                            </div>
                        </template>
                        <span v-html="itemHint(item)">{{ itemHint(item) }}</span>
                    </v-tooltip>
                    <div
                        v-else
                        class="v-list-item"
                    >
                        <div class="v-list-item__content">
                            <div class="v-list-item__title">
                                {{ item.name }}
                            </div>
                        </div>
                    </div>

                </template>
            </v-select>
        </v-col>
    </v-row>
</template>

<script>

export default {
    name: 'form-select',
    model: {
        prop: 'value',
        event: 'input'
    },
    props: {
        label: {
            type: String,
            required: false,
            default: "",
        },
        tooltip: {
            type: String,
            required: false,
            default: "",
        },
        items: {
            type: Array,
            required: true,
        },
        value: {
            required: true,
        },
        disabled: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    mounted() {
        this.local = this.items.find((i) => i.value === this.value)
    },
    computed: {
        selectedItemHint() {
            if (this.local && this.local.hint) {
                const strippedString = this.local.hint.replace(/(<([^>]+)>)/gi, "");
                return strippedString;
            }
            return null;
        },
    },
    methods: {
        itemHint(item) {
            if (item && item.hint) return item.hint;
            return null;
        },
    },
    data: () => {
        return {
            local: null,
        };
    },
    watch: {
        value(n) {
            this.local = this.items.find((i) => i.value === n);
        },
        local(n) {
            this.$emit('input', n ? n.value : null );
        },
    }
};
</script>

<style scoped>
.cbrow {
    text-align: left;
}
</style>