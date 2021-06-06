<template>
    <v-dialog
        v-model="active"
        persistent
        max-width="290"
    >
        <v-card>
            <v-card-title class="text-h5">
                {{ context.title }}
            </v-card-title>
            <v-card-text>{{ context.text }}</v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    :color="`${context.button1Color} darken-1`"
                    text
                    @click=context.button1Handler
                >
                    {{ context.button1Text }}
                </v-btn>
                <v-btn
                    :color="`${context.button2Color} darken-1`"
                    text
                    @click=context.button2Handler
                    >
                    {{ context.button2Text }}
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>

export default {
    name: 'dialog-confirmation',
    props: {
        active: {
            type: Boolean,
            required: true,
        },
        context: {
            type: Object,
            required: true,
        },
    },
};
</script>

<style scoped>
</style>