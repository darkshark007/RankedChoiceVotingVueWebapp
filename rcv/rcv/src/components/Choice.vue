<template>
    <div>
        <v-card
            class="ma-4"
            elevation=2
            v-if="isDisplay || isEdit"
        >
            <v-row align=center class="ma-2">

                <!-- Icon -->
                <v-col cols=1>
                    <template v-if="isDisplay && editable">
                            <v-btn
                                fab
                                small
                                color="light-green lighten-4"
                                @click="startEdit"
                            >
                                <v-icon color="indigo" class="ma-2">mdi-pencil-outline</v-icon>
                            </v-btn>
                    </template>
                    <v-icon v-if="isDisplay && !editable" color="indigo" class="ma-2">mdi-star-outline</v-icon>
                    <v-btn v-if="isEdit" icon color="indigo" @click="$emit('remove')">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>                
                </v-col>

                <v-spacer></v-spacer>
                <v-col cols=10 align=left>

                    <!-- Name -->
                    <div v-if="!isEdit && choice.name">
                        <b>{{ choice.name }}</b>
                    </div>
                    <v-text-field
                        v-if="isEdit" 
                        label="Name"
                        v-model="choice.name"
                    ></v-text-field>

                    <!-- Description -->
                    <div v-if="!isEdit && choice.description">
                        <span class="descriptionText">{{ choice.description }}</span>
                    </div>
                    <v-textarea
                        v-if="isEdit" 
                        label="Description"
                        v-model="choice.description"
                        rows="1"
                        auto-grow
                    ></v-textarea>

                </v-col>
            </v-row>
        </v-card>
        <div
            v-if="isPreview"
        >
            <v-row align=center>

                <!-- Icon -->
                <v-col cols=1>
                    <v-icon color="indigo" class="ma-2">mdi-star-outline</v-icon>
                </v-col>
                <v-col cols=9 align=left>
                    <!-- Name -->
                    <div v-if="choice.name">
                        <b>{{ choice.name }}</b>
                    </div>
                </v-col>
            </v-row>
        </div>
    </div>
</template>

<script>

export default {
    name: 'poll-choice',
    props: {
        choice: {
            type: Object,
            required: true,
        },
        propEdit: {
            type: Boolean,
            required: false,
            default: false,
        },
        preview: {
            type: Boolean,
            required: false,
            default: false,
        },
        editable: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    computed: {
        // Render Type
        isDisplay() {
            return !this.edit && !this.preview;
        },
        isEdit() {
            return this.edit && !this.preview && !this.choice.isDeleted;
        },
        isPreview() {
            return !this.edit && this.preview;
        },
    },
    methods: {
        startEdit() {
            this.edit = true;
            this.$emit('onEdit');
        },
    },
    created() {
        this.edit = this.propEdit;
    },
    mounted() {
        // Model definition
        if (!this.choice.name)
            this.choice.name = "";
        if (!this.choice.description)
            this.choice.description = "";
    },
    data: () => {
        return {
            'edit': false,
        }
    },
    watch: {
        choice() {
            this.edit = this.propEdit;
        }
    }
};
</script>

<style scoped>
</style>