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
                <span>{{ tooltip }}</span>
            </v-tooltip>
        </v-col>
        <v-col >
            <v-switch
                v-model=local
                inset
                :label="title"
            ></v-switch>
        </v-col>
    </v-row>
</template>

<script>

export default {
    name: 'form-checkbox',
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
            type: Boolean,
            required: true,
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
            local: false,
        };
    },
    watch: {
        value(n) {
            this.local = n;
        },
        local(n) {
            this.$emit('input', n || false);
        },
    }
};
</script>

<style scoped>
.cbrow {
    text-align: left;
}
</style>