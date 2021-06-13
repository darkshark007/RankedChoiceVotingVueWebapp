<template>
    <v-row class="cbrow formPad" align=center>
        <v-col cols=1 v-if="tooltip" class="formPad">
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
        <v-col cols=5 class="formPad">
            <v-menu
                ref="dateMenu"
                v-model="dateMenu"
                :close-on-content-click="false"
                :return-value.sync="localDate"
                transition="scale-transition"
                offset-y
                min-width="auto"
                :disabled="disabled"
            >
                <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                        v-model="localDate"
                        :label="`${label} date`"
                        prepend-icon="mdi-calendar"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                    />
                </template>
                <v-date-picker
                    v-model="localDate"
                    no-title
                    scrollable
                >
                    <v-spacer></v-spacer>
                    <v-btn
                        text
                        color="primary"
                        @click="dateMenu = false"
                    >
                        Cancel
                    </v-btn>
                    <v-btn
                        text
                        color="primary"
                        @click="$refs.dateMenu.save(localDate)"
                    >
                        OK
                    </v-btn>
                </v-date-picker>
            </v-menu>
        </v-col>
        <v-col cols=5 class="formPad">
            <v-menu
                ref="timeMenu"
                v-model="timeMenu"
                :close-on-content-click="false"
                :nudge-right="40"
                :return-value.sync="localTime"
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="290px"
            >
                <template v-slot:activator="{ on, attrs }">
                <v-text-field
                    v-model="localTime"
                    :label="`${label} time`"
                    prepend-icon="mdi-clock-time-four-outline"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                ></v-text-field>
                </template>
                <v-time-picker
                    v-if="timeMenu"
                    v-model="localTime"
                    full-width
                    @click:minute="$refs.timeMenu.save(localTime)"
                ></v-time-picker>
            </v-menu>
        </v-col>
        <v-col cols=1 v-if="this.clearable !== null" class="formPad ma-0 pa-0">
            <v-btn icon color="indigo" @click="clear">
                <v-icon>mdi-close</v-icon>
            </v-btn>
        </v-col>
    </v-row>
</template>

<script>

export default {
    name: 'form-datetime',
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
        clearable: {
            required: false,
            default: null,
        },
        tooltip: {
            type: String,
            required: false,
            default: "",
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
    data: () => {
        return {
            dateMenu: false,
            timeMenu: false,
            lastDate: null,
            localDate: '',
            localTime: '',
        };
    },
    computed: {
    },
    methods: {
        clear() {
            this.localDate = null;
            this.localTime = null;
        },
        dateToUTC(date) {
            if (date === null) return null;
            // https://stackoverflow.com/questions/9756120/how-do-i-get-a-utc-timestamp-in-javascript#:~:text=If%20you%20want%20a%20one,elapsed%20in%20Seconds%20since%20epoch.
            return ~~(+new Date(date) / 1000);
        },
        UTCToDate(utc) {
            if (utc === null) return null;
            return new Date(utc*1000);
        },
        emitValue() {
            let date = this.localDate ? this.localDate : '';
            let time = this.localTime ? this.localTime : '';
            if (!date && !time) {
                this.$emit('input', null);
                return;
            }
            this.$emit('input', this.dateToUTC(`${date} ${time}`));
        }
    },
    watch: {
        value: {
            immediate: true,
            handler(n) {
                if (n === this.lastDate) return;
                this.lastDate = n;
                if (!n) {
                    this.localTime = '';
                    this.localDate = '';
                    return;
                }
                let converted = this.UTCToDate(n);
                let year = `${converted.getFullYear()}`;
                let month = `${+converted.getMonth()+1}`;
                if (month.length == 1) month = `0${month}`;
                let day = `${converted.getDate()}`
                if (day.length == 1) day = `0${day}`;
                this.localDate = `${year}-${month}-${day}`;
                let hour = `${converted.getHours()}`;
                if (hour.length == 1) hour = `0${hour}`;
                let min = `${converted.getMinutes()}`;
                if (min.length == 1) min = `0${min}`;
                this.localTime = `${hour}:${min}`;
            },
        },
        localDate() {
            this.emitValue();
        },
        localTime() {
            if (this.localTime && !this.localDate) {
                // Use Today's date
                let converted = new Date();
                let year = `${converted.getFullYear()}`;
                let month = `${+converted.getMonth()+1}`;
                if (month.length == 1) month = `0${month}`;
                let day = `${converted.getDate()}`
                if (day.length == 1) day = `0${day}`;
                this.localDate = `${year}-${month}-${day}`;
            }
            this.emitValue();
        },
    }
};
</script>

<style scoped>
.cbrow {
    text-align: left;
}

.formPad {
    padding-top: 0px;
    padding-bottom: 0px;
}
</style>