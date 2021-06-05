<template>
    <v-row class="cbrow" align=center>
        <v-col cols=1>
            <v-tooltip bottom max-width="300px" v-if="tooltip">
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
            <v-text-field
                v-model=local
                :disabled="disabled"
                :label="title"
                :rules="rules"
            ></v-text-field>
        </v-col>
    </v-row>
</template>

<script>

export default {
    name: 'form-text',
    model: {
        prop: 'value',
        event: 'input'
    },
    props: {
        title: {
            type: String,
            required: false,
            default: "",
        },
        tooltip: {
            type: String,
            required: false,
            default: "",
        },
        value: {
            validator: prop => typeof prop === 'number' || typeof prop === 'string' || prop === null,
            required: true,
        },
        disabled: {
            type: Boolean,
            required: false,
            default: false,
        },
        rules: {
            type: Array,
            required: false,
            default: () => [],
        },
    },
    methods: {
    },
    mounted() {
        this.local = this.value;
    },
    computed: {
    },
    data: () => {
        return {
            local: null,
        };
    },
    watch: {
        value(n) {
            this.local = n;
        },
        local(n) {
            this.$emit('input', n || null);
        },
    }
};
</script>

<style scoped>
.cbrow {
    text-align: left;
}
</style>