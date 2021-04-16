<template>
    <v-card
        class="wrapper"
        id="error-card"
        max-width="60%"
        align="center"
        v-if="displayedError"
    >
        <!-- TODO: EXTRACT ERROR CARD OUT -->
        <v-row
            align="center"
        >
            <v-col>
                <v-icon class="pa-2">mdi-alert-circle-outline</v-icon>
                <span class="red--text">{{ displayedError }}</span>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>

export default {
    name: 'error-card',
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
        }
    },
    watch: {
        errorString(error) {
            let combinedError = `${this.errorStringBase}${error}`;
            console.error(combinedError);
            this.displayedError = combinedError;
            clearTimeout(this.errorTimeout);
            this.errorTimeout = setTimeout(() => {
                this.displayedError = null;
            }, this.errorDuration);
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