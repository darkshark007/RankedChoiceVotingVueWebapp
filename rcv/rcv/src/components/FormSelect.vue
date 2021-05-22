<template>
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
            <v-tooltip bottom max-width="300px">
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
        </template>
    </v-select>
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
        items: {
            type: Array,
            required: true,
        },
        value: {
            type: [Object, String],
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
</style>