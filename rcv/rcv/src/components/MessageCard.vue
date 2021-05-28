<template>
    <div ref="target">
        <v-card
            class="wrapper appWidth message-card"
            align="center"
            v-if="displayedError"
        >
            <v-row
                align="center"
            >
                <v-col>
                    <v-icon class="pa-2">mdi-alert-circle-outline</v-icon>
                    <span class="red--text">{{ displayedError }}</span>
                </v-col>
            </v-row>
        </v-card>
        <v-card
            class="wrapper appWidth message-card"
            align="center"
            v-if="displayedSuccess"
        >
            <v-row
                align="center"
            >
                <v-col>
                    <v-icon class="pa-2">mdi-check-circle-outline</v-icon>
                    <span class="green--text">{{ displayedSuccess }}</span>
                </v-col>
            </v-row>
        </v-card>
    </div>
</template>

<script>

export default {
    name: 'message-card',
    props: {
        errorString: {
            type: String,
            required: false,
            default: null,
        },
        errorStringBase: {
            type: String,
            required: false,
            default: null,
        },
        successString: {
            type: String,
            required: false,
            default: null,
        },
        errorDuration: {
            type: Number,
            required: false,
            default: 10000,
        },
    },
    data: () => {
        return {
            errorTimeout: null,
            displayedError: null,
            displayedSuccess: null,
        }
    },
    methods: {
        updateMessages() {
            this.displayedError = null;
            if (this.errorString) {
                let combinedError = `${this.errorStringBase}${this.errorString}`;
                console.error(combinedError);
                this.displayedError = combinedError;
            }

            this.displayedSuccess = null;
            if (this.successString) {
                this.displayedSuccess = this.successString;
            }

            this.$vuetify.goTo(this.$refs.target);
            clearTimeout(this.errorTimeout);
            this.errorTimeout = setTimeout(() => {
                this.displayedError = null;
                this.displayedSuccess = null;
            }, this.errorDuration);
        },
    },
    watch: {
        errorString() {
            this.updateMessages();
        },
        successString() {
            this.updateMessages();
        },
    }
};
</script>

<style scoped>
.wrapper {
    align: center;
    padding: 15px;
}
</style>